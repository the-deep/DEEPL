from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from topic_modeling.lda import get_topics_and_subtopics
from classifier.models import ClassifiedDocument
from api.helpers import check_if_test


class TopicModelingView(APIView):
    """API for topic modeling"""
    @check_if_test('topic_modeling')
    def post(self, request):
        """Handle API POST request"""
        # data = dict(request.query_params.items())
        validation_details = self._validate_topic_modeling_params(request.data)
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

        lda_output = get_topics_and_subtopics(
            params['documents'],
            params['number_of_topics'],
            params['keywords_per_topic'],
            depth=5 if params['depth'] > 5 else params['depth']
        )
        return Response(lda_output)

    def _validate_topic_modeling_params(self, queryparams):
        """Validator for params"""
        errors = {}
        params = {}
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
