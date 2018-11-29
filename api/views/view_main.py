import langdetect
from googletrans import Translator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.transaction import atomic

from api.helpers import (
    classify_text,
    classify_lead_excerpts,
    check_if_test
)

from helpers.google import get_location_info
from helpers.common import classification_confidence

from classifier.models import (
    ClassifierModel,
    ClassifiedDocument,
    ClassifiedExcerpt,
    Recommendation,
)

from classifier.serializers import (
    ClassifiedDocumentSerializer,
    ClassifiedExcerptSerializer,
)
from topic_modeling.keywords_extraction import get_key_ngrams
from topic_modeling.models import TopicModelingModel
from topic_modeling.tasks import get_topics_and_subtopics_task
from NER.ner import get_ner_tagging, get_ner_tagging_doc
from classifier.globals import get_classifiers

from correlation.tasks import get_documents_correlation
from clustering.tasks import assign_cluster_to_doc

import traceback
import logging
logger = logging.getLogger('django')


class DocumentClassifierView(APIView):
    """
    API for document classification
    """
    def __init__(self):
        # load all the classifiers
        self.classifiers = get_classifiers()
        self.translator = Translator()

    def post(self, request, version):
        data = dict(request.data.items())
        validation_details = self._validate_classification_params(data)
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
        # check if deeper and doc_id present
        deeper = True if data.get('deeper') else False
        if deeper and data.get('doc_id'):
            # get already classified data
            try:
                classified_doc = ClassifiedDocument.objects.get(
                    id=data['doc_id']
                )
                return_data = ClassifiedDocumentSerializer(classified_doc).data
                return_data['excerpts_classification'] = \
                    ClassifiedExcerptSerializer(
                        classified_doc.excerpts, many=True
                    ).data
                return Response(return_data)
            except ClassifiedDocument.DoesNotExist:
                return Response(
                    {'error': 'Classified Document not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response({
                    'status': False,
                    'message': 'Invalid doc_id'
                }, status=status.HTTP_400_BAD_REQUEST)
        classifier = self.classifiers.get(version)

        if not classifier:
            return Response(
                {'status': False, 'message': 'Classifier not found'},
                status.HTTP_404_NOT_FOUND
            )
        text = data['text']

        # get language
        language = langdetect.detect(text)
        original = None
        try:
            if language != 'en':
                original = text
                logger.info("not english language")
                translation = self.translator.translate(text)
                translated = translation.text
                text = translated
                logger.info("Translated text: {}".format(translated))
        except Exception as e:
            logger.warn("Exception while translating text. {}".format(e))

        classified = classify_text(classifier['classifier'], text)

        if not data.get('deeper'):
            return Response({
                'classification': classified,
                'classification_confidence': classification_confidence(
                    classified
                )
            })

        # Create classified Document
        grp_id = data.get('group_id')

        extra_info = {"language": language}
        if original:
            extra_info['original'] = original

        doc = ClassifiedDocument.objects.create(
            text=text,
            classifier=classifier['classifier_model'],
            confidence=classified[0][1],
            classification_label=classified[0][0],
            classification_probabilities=classified,
            group_id=grp_id,
            extra_info=extra_info
        )

        # now add the doc to a cluster, only if new doc is present
        if not data.get('doc_id'):
            # doc id is send for already present doc
            # we want to cluster new document
            assign_cluster_to_doc.delay(doc.id)

        classified_excerpts = classify_lead_excerpts(
            classifier['classifier'],
            text,
        )
        # create excerpts
        excerpts = []
        for x in classified_excerpts:
            excerpts.append(
                ClassifiedExcerpt.objects.create(
                    classified_document=doc,
                    start_pos=x['start_pos'],
                    end_pos=x['end_pos'],
                    classification_label=x['classification'][0][0],
                    confidence=x['classification'][0][1],
                    classification_probabilities=x['classification']
                )
            )
        ret = ClassifiedDocumentSerializer(doc).data
        ret['excerpts_classification'] = ClassifiedExcerptSerializer(
            excerpts, many=True
        ).data
        return Response(ret)

    def _validate_classification_params(self, params):
        """Validator for params"""
        errors = {}
        deeper = params.get('deeper', '')
        # doc_id = params.get('doc_id')

        if not deeper and not params.get('text'):
            errors['text'] = 'text to be classified is missing.'
        elif deeper and not params.get('text') and not params.get('doc_id'):
            errors['text'] = 'Either text or doc_id should be present'
            errors['doc_id'] = 'Either text or doc_id should be present'
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status': True,
        }


class ClassifiedDocumentView(APIView):
    def put(self, request):
        data = dict(request.data.items())
        validation_details = self._validate_post_data(data)
        if not validation_details['status']:
            return Response(
                validation_details['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        data = validation_details['data']  # validated data
        with atomic():
            for x in data['items']:
                did = x['doc_id']
                gid = x['group_id']
                try:
                    obj = ClassifiedDocument.objects.get(id=did)
                    obj.group_id = gid
                    obj.save()
                except ClassifiedDocument.DoesNotExist:
                    logger.info(
                        "UpdateDocIdView: non existent doc id {}".
                        format(did)
                    )
            return Response({"message": "Successful update"})

    def _validate_post_data(self, data):
        errors = {}
        items = data.get('items')
        if not items:
            errors['items'] = 'items should be present'
        elif not isinstance(items, list):
            errors['items'] = 'items should be list of {group_id: <>, doc_id: <>}'
        else:
            for x in items:
                if 'group_id' not in x:
                    errors['group_id'] = 'group_id should be present in all data'
                if 'doc_id' not in x:
                    errors['doc_id'] = 'doc_id should be present in all data'
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        return {
            'status': True,
            'data': data
        }


class KeywordsExtractionView(APIView):
    def post(self, request):
        """Handle API POST request"""
        # data = dict(request.query_params.items())
        validation_details = self._validate_keywords_extraction_params(
            request.data
        )
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
        params = validation_details['params']
        doc = params['document']
        args = (doc, params['max_grams']) if params['max_grams'] else (doc,)
        key_ngrams = get_key_ngrams(
            *args,
            include_numbers=params.get('include_numbers', False)
        )
        return Response(key_ngrams)

    def _validate_keywords_extraction_params(self, queryparams):
        """Validator for params"""
        errors = {}
        params = {}
        if not queryparams.get('document'):
            errors['document'] = "document should be present"
        else:
            params['document'] = queryparams['document']
        if queryparams.get('max_grams'):
            try:
                params['max_grams'] = int(queryparams['max_grams'])
                if params['max_grams'] < 1:
                    raise Exception
            except Exception as e:
                errors['max_grams'] = (
                    'max_grams, if present, should be a positive integer'
                )
        else:
            params['max_grams'] = None

        inc_numbers = queryparams.get('include_numbers')
        if inc_numbers and (inc_numbers == 'true' or inc_numbers == '1'):
            params['include_numbers'] = True

        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status': True,
            'params': params
        }


class ApiVersionsView(APIView):
    def get(self, request):
        versions = ClassifierModel.objects.values("version", "accuracy")
        return Response({"versions": list(versions)})


class RecommendationView(APIView):
    def post(self, request, version):
        data = dict(request.data.items())
        validation_details = self._validate_recommendation_params(data)
        if not validation_details['status']:
            return Response(validation_details,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Strip off 'v' from 'vX' in version
            classifier_model = ClassifierModel.objects.get(version=version[1:])
        except ClassifierModel.DoesNotExist:
            return Response(
                {'message': 'Classifier not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        extra = self._get_extra_info(data)
        # create a Recommendation object
        Recommendation.objects.create(
            classifier=classifier_model,
            text=data['text'],
            classification_label=data['classification_label'],
            useful=True if data['useful'].lower() == 'true' else False,
            extra_info=extra
        )
        return Response({'message': 'Recommendation added successfully.'})

    def _validate_recommendation_params(self, data):
        errors = {}
        if not data.get('text'):
            errors['text'] = 'text for recommendation is missing'
        if not data.get('classification_label'):
            errors['classification_label'] = (
                'classissification_label is missing'
            )
        if not data.get('useful'):
            errors['useful'] = (
                'Missing value for usefulness of the recommendation'
            )
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {'status': True}

    def _get_extra_info(self, data):
        extra = {}
        if 'user_id' in data and len(str(data['user_id'])) <= 12:
            extra['user_id'] = data['user_id']
        if 'lead_id' in data and len(str(data['lead_id'])) <= 12:
            extra['lead_id'] = data['lead_id']
        if 'entry_id' in data and len(str(data['entry_id'])) <= 12:
            extra['entry_id'] = data['entry_id']
        if 'date_captured' in data and len(str(data['date_captured'])) <= 20:
            extra['date_captured'] = data['date_captured']
        return extra


class NERView(APIView):
    def post(self, request):
        data = dict(request.data.items())
        validation_details = self._validate_ner_params(data)
        if not validation_details['status']:
            return Response(validation_details['error_data'],
                            status=status.HTTP_400_BAD_REQUEST)
        ner_tagged = get_ner_tagging(data['text'])
        return Response(ner_tagged)

    def _validate_ner_params(self, data):
        errors = {}
        if not data.get('text'):
            errors['text'] = "Missing text to be NER tagged"
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status': True,
            'error_data': {}
        }


class NERWithDocIdView(APIView):
    def post(self, request):
        data = dict(request.data)
        validation_details = self._validate_ner_params(data)
        if not validation_details['status']:
            return Response(validation_details['error_data'],
                            status=status.HTTP_400_BAD_REQUEST)

        doc_ids = data.get('doc_ids', [])
        documents = ClassifiedDocument.objects.filter(id__in=doc_ids)
        # if no documents found, return 404
        if not documents:
            return Response(
                {'error': 'No documents found for NER tagging.'},
                status=status.HTTP_404_NOT_FOUND
            )
        texts = [x.text for x in documents]
        ner_tagged = []
        for docid in doc_ids:
            tags, cached = get_ner_tagging_doc(docid)
            ner_tagged.extend(tags)

        locations = []
        for i, ner in enumerate(ner_tagged):
            if ner.get('entity') == 'LOCATION':
                try:
                    start = ner['start']
                    end = start + ner['length']
                    location = texts[i][start:end]

                    if location not in locations:
                        locations.append(location)
                except (IndexError, KeyError):
                    pass

        response = []
        # only process 25 location for now
        for location in locations[:25]:
            response.append({
                'name': location,
                'info': get_location_info(location),
            })

        return Response({'locations': response})

    def _validate_ner_params(self, data):
        errors = {}
        doc_ids = data.get('doc_ids')
        if not doc_ids:
            errors['doc_ids'] = "Missing doc_ids to be NER tagged"
        elif not type(doc_ids) == list:
            errors['doc_ids'] = "doc_ids should be a list"
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status': True,
            'error_data': {}
        }


class CorrelationView(APIView):
    @check_if_test('correlation')
    def post(self, request, entity):
        validation_details = self._validate_params(request.data)
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
        params = validation_details['params']
        if params.get('doc_ids'):
            classified_docs = ClassifiedDocument.objects.filter(
                id__in=params['doc_ids']
            )
            classified_docs = [
                (x.classification_label, x.text)
                for x in classified_docs
            ]
        if entity == 'topics':
            return self.get_topic_correlation(params)
        elif entity == 'subtopics':
            try:
                correlated_data = get_documents_correlation(classified_docs)
            except Exception:
                logger.warning(traceback.format_exc())
                return Response(
                    {"error": "Something went wrong. Try later"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif entity == 'keywords':
            from static_responses.correlation import keywords_data
            correlated_data = keywords_data
        else:
            correlated_data = {}
        return Response(correlated_data)

    def get_topic_correlation(self, params):
        gid = params.get('group_id')
        if not gid:
            return Response(
                {'group_id': 'group_id should be present'},
                status=status.HTTP_400_BAD_REQUEST
            )
        model = TopicModelingModel.objects.filter(group_id=gid).first()
        if not model or not model.ready:
            # Send request to create model
            if not model:
                get_topics_and_subtopics_task.delay(gid)
            return Response(
                {'message': 'Correlation is being calculated'},
                status=status.HTTP_202_ACCEPTED
            )
        else:
            # Data ready
            return Response(
                {'topics_correlation': model.extra_info['topics_correlation']}
            )

    def _validate_params(self, params):
        errors = {}
        doc_ids = params.get('doc_ids', [])
        group_id = params.get('group_id')
        if not group_id and (not doc_ids or type(doc_ids) != list):
            errors['doc_ids'] = 'Provide doc_ids. It should be a list of integers. Or provide group_id.'
            errors['group_id'] = 'Provide group_id. Or provide doc_ids.'
        for x in doc_ids:
            try:
                int(x)
            except ValueError:
                errors['doc_ids'] = 'Invlid doc_id value "{}". Provide integer value.'
                break
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status': True,
            'params': params
        }
