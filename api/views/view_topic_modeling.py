from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from topic_modeling.lda import LDAModel
from topic_modeling.tasks import get_topics_and_subtopics_task
from topic_modeling.models import TopicModelingModel
from classifier.models import ClassifiedDocument
from api.helpers import check_if_test


class TopicModelingView(APIView):
    """API for topic modeling"""
    def get(self, request, version=None):
        version = request.version
        if version == 'v2':
            validation_details = validate_get_topic_modeling(
                request.query_params
            )
            if not validation_details['status']:
                return Response(
                    validation_details['error_data'],
                    status=status.HTTP_400_BAD_REQUEST
                )
            params = validation_details['params']
            group_id = params['group_id']
            num_topics = params['number_of_topics']
            kws_per_topic = params['keywords_per_topic']
            depth = params['depth']
            try:
                model = TopicModelingModel.objects.get(
                    group_id=group_id,
                    keywords_per_topic=kws_per_topic,
                    depth=depth,
                    number_of_topics=num_topics
                )
            except TopicModelingModel.DoesNotExist:
                return Response(
                    {'message': 'Model does not exist. Please create model first by calling POST method.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                if not model.ready:
                    return Response(
                        {'message': 'Model is being created. Try later'},
                        status=status.HTTP_202_ACCEPTED
                    )
                return Response(model.data)
        else:
            return Response(
                {'error': 'Invalid version. GET available from v2 only.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @check_if_test('topic_modeling')
    def post(self, request, version=None):
        """Handle API POST request"""
        version = request.version
        if version == 'v1' or version is None:
            return v1_topic_modeling_handler(request)
        elif version == 'v2':
            return v2_topic_modeling_handler(request)
        else:
            return Response(
                {'error': 'Invalid version.'},
                status=status.HTTP_400_BAD_REQUEST
            )


def basic_validate(queryparams):
    errors = {}
    params = {}
    try:
        num_topics = int(queryparams.get('number_of_topics'))
    except Exception as e:
        errors['number_of_topics'] = (
            'Missing/invalid number of topics. '
            'Should be present as a positive integer'
        )
    else:
        params['number_of_topics'] = num_topics
    try:
        kw_per_topic = int(queryparams.get('keywords_per_topic'))
    except Exception as e:
        errors['keywords_per_topic'] = (
            'Missing/invalid number of keywords per topic. '
            'Should be present as a positive integer'
        )
    else:
        params['keywords_per_topic'] = kw_per_topic
    try:
        depth = int(queryparams.get('depth'))
    except Exception as e:
        errors['depth'] = (
            'Missing/invalid depth of subtopics. '
            'Should be present as a positive integer'
        )
    else:
        params['depth'] = depth
    if errors:
        return {
            'status': False,
            'error_data': errors
        }
    return {
        'status': True,
        'params': params
    }


def validate_v1_topic_modeling_params(queryparams):
    """Validator for params"""
    errors = {}
    basic_validation = basic_validate(queryparams)

    if not basic_validation['status']:
        return basic_validation

    params = basic_validation['params']
    # Convert to dict and list is retained,
    # else in querydict only first element is retained
    dictparams = dict(queryparams)
    if not queryparams.get('documents', []):
        if not dictparams.get('doc_ids', []):
            errors['documents'] = (
                'Missing documents on which modeling is to be done'
            )
        else:
            params['doc_ids'] = dictparams.get('doc_ids')
    elif not type(dictparams.get('documents')) == list:
        errors['documents'] = 'documents should be list'
    else:
        # this is a list
        params['documents'] = dictparams.get('documents')
        # params['documents'] = queryparams.getlist('documents')
    if errors:
        return {
            'status': False,
            'error_data': errors
        }
    return {
        'status': True,
        'params': params
    }


def validate_v2_topic_modeling_params(params):
    errors = {}
    basic_validation = basic_validate(params)

    if not basic_validation['status']:
        return basic_validation

    if not params.get('group_id'):
        errors['group_id'] = 'group_id should be present'
    if errors:
        return {
            'status': False,
            'error_data': errors
        }
    return {
        'status': True,
        'params': params
    }


def validate_get_topic_modeling(params):
    errors = {}
    basic_validation = basic_validate(params)
    if not basic_validation['status']:
        return basic_validation
    if not params.get('group_id'):
        errors['group_id'] = 'group_id is not present'
    if errors:
        return {
            'status': False,
            'error_data': errors
        }
    return {
        'status': True,
        'params': params
    }


def v1_topic_modeling_handler(request):
    validation_details = validate_v1_topic_modeling_params(
        request.data
    )
    if not validation_details['status']:
        return Response(
            validation_details['error_data'],
            status=status.HTTP_400_BAD_REQUEST
        )

    params = validation_details['params']
    if params.get('doc_ids'):
        documents = ClassifiedDocument.objects.filter(
            id__in=params.get('doc_ids')
        )
        if not documents:
            return Response(
                {"error": "doc_ids not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        params['documents'] = [
            doc.text for doc in documents
        ]

    lda = LDAModel()
    lda_output = lda.get_topics_and_subtopics(
        params['documents'],
        params['number_of_topics'],
        params['keywords_per_topic'],
        depth=5 if params['depth'] > 5 else params['depth']
    )
    return Response(lda_output)


def v2_topic_modeling_handler(request):
    # get group_id and send it to background for  topic_modeling computation
    validation_details = validate_v2_topic_modeling_params(
        request.data
    )
    if not validation_details['status']:
        return Response(
            validation_details['error_data'],
            status=status.HTTP_400_BAD_REQUEST
        )
    params = validation_details['params']

    docs_qs = ClassifiedDocument.objects.filter(group_id=params['group_id'])
    if docs_qs.count() == 0:
        return Response(
            {'message': 'No docs with given group_id found'},
            status=status.HTTP_404_NOT_FOUND
        )
    grp_id = params['group_id']
    # Check if model exists or not, if not, create one
    # If exists, check if ready or not, if ready, do not call task
    try:
        topic_model = TopicModelingModel.objects.get(group_id=grp_id)
        if topic_model.ready:
            return Response(
                {'message': 'Topic model is created, call GET method'},
                status=status.HTTP_201_CREATED
            )
    except TopicModelingModel.DoesNotExist:
        TopicModelingModel.objects.create(
            group_id=grp_id,
            number_of_topics=params['number_of_topics'],
            keywords_per_topic=params['keywords_per_topic'],
            depth=params['depth']
        )
        # send to background
        get_topics_and_subtopics_task.delay(
            params['group_id'], params['number_of_topics'],
            params['keywords_per_topic'], params['depth']
        )
    return Response(
        {'message': 'Topic modeling model is being created'},
        status=status.HTTP_202_ACCEPTED
    )
