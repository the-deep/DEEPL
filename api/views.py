from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import pickle

from api.helpers import (
    classify_text,
    classify_lead_excerpts,
)

from helpers.google import get_location_info

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
from topic_modeling.lda import get_topics_and_subtopics
from topic_modeling.keywords_extraction import get_key_ngrams
from NER.ner import get_ner_tagging

from correlation.models import Correlation
from correlation.tasks import get_documents_correlation

import traceback
import logging
logger = logging.getLogger(__name__)


class DocumentClassifierView(APIView):
    """
    API for document classification
    """
    classifiers = {'v'+str(x.version): {
        'classifier': pickle.loads(x.data),
        'classifier_model': x
        }
            for x in ClassifierModel.objects.all()
    }

    def __init__(self):
        # load all the classifiers
        pass

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
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({
                    'status': False,
                    'message': 'Invalid doc_id'
                }, status=status.HTTP_400_BAD_REQUEST)
        classifier = DocumentClassifierView.classifiers.get(version)

        if not classifier:
            return Response(
                {'status': False, 'message': 'Classifier not found'},
                status.HTTP_404_NOT_FOUND
            )
        text = data['text']
        classified = classify_text(classifier['classifier'], text)

        if not data.get('deeper'):
            return Response({'classification': classified})

        # Create classified Document
        grp_id = data.get('group_id')

        doc = ClassifiedDocument.objects.create(
            text=text,
            classifier=classifier['classifier_model'],
            confidence=classified[0][1],
            classification_label=classified[0][0],
            classification_probabilities=classified,
            group_id=grp_id
        )
        classified_excerpts = classify_lead_excerpts(
            classifier['classifier'],
            text,
        )

        # create excerpts
        for x in classified_excerpts:
            ClassifiedExcerpt.objects.create(
                classified_document=doc,
                start_pos=x['start_pos'],
                end_pos=x['end_pos'],
                classification_label=x['classification'][0][0],
                confidence=x['classification'][0][1],
                classification_probabilities=x['classification']
            )
        ret = ClassifiedDocumentSerializer(doc).data
        ret['excerpts_classification'] = classified_excerpts
        return Response(ret)

    def _validate_classification_params(self, params):
        """Validator for params"""
        errors = {}
        deeper = params.get('deeper', '')
        doc_id = params.get('doc_id')

        if not deeper and not params.get('text'):
            errors['text'] = 'text to be classified is missing.'
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status': True,
        }


class TopicModelingView(APIView):
    """API for topic modeling"""
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

        # ldamodel = LDAModel()
        # ldamodel.create_model(params['documents'],
        #                       params['number_of_topics'])
        # topics_and_keywords = ldamodel.get_topics_and_keywords(
        #     params['keywords_per_topic']
        # )
        # return Response({
        #     'Topic {}'.format(i+1): v
        #     for i, v in enumerate(topics_and_keywords)
        # })

    def _validate_topic_modeling_params(self, queryparams):
        """Validator for params"""
        errors = {}
        params = {}
        if not queryparams.get('documents', []):
            if not queryparams.get('doc_ids', []):
                errors['documents'] = (
                    'Missing documents on which modeling is to be done'
                )
            else:
                params['doc_ids'] = queryparams.get('doc_ids')
        elif not type(queryparams.get('documents')) == list:
            errors['documents'] = 'documents should be list'
        else:
            # this is a list
            params['documents'] = queryparams.get('documents')
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
        key_ngrams = get_key_ngrams(*args, include_numbers=params.get('include_numbers', False))
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

        if queryparams.get('include_numbers'):
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
        return Response({"versions": versions})


class RecommendationView(APIView):
    def post(self, request, version):
        data = dict(request.data.items())
        validation_details = self._validate_recommendation_params(data)
        if not validation_details['status']:
            return Response(validation_details,
                            status=status.HTTP_400_BAD_REQUEST)

        classifier = DocumentClassifierView.classifiers.get(version)
        if not classifier:
            return Response(
                {'message': 'Classifier not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        extra = self._get_extra_info(data)
        # create a Recommendation object
        recomm = Recommendation.objects.create(
            classifier=classifier['classifier_model'],
            text=data['text'],
            classification_label=data['classification_label'],
            useful=True
                if data['useful'].lower() == 'true'
                else False,
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
            return Response(validation_details,
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
        data = dict(request.data.items())
        validation_details = self._validate_ner_params(data)
        if not validation_details['status']:
            return Response(validation_details,
                            status=status.HTTP_400_BAD_REQUEST)

        documents = ClassifiedDocument.objects.filter(
            id__in=data.get('doc_ids', [])
        )
        text = [doc.text for doc in documents]
        text = ' '.join(text)

        ner_tagged = get_ner_tagging(text)
        locations = []
        for ner in ner_tagged:
            if ner.get('entity') == 'LOCATION':
                try:
                    start = ner['start']
                    end = start + ner['length']
                    location = text[start:end]

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
        if not data.get('doc_ids'):
            errors['doc_ids'] = "Missing doc_ids to be NER tagged"
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
    def post(self, request, entity):
        validation_details = self._validate_params(request.data)
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
        params = validation_details['params']
        classified_docs = ClassifiedDocument.objects.filter(
            id__in=params['doc_ids']
        )
        try:
            correlated_data = get_documents_correlation(classified_docs)
        except Exception:
            logger.warning(traceback.format_exc())
            return Response(
                {"error": "Something went wrong. Try later"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(correlated_data)

    def _validate_params(self, params):
        errors = {}
        doc_ids = params.get('doc_ids', [])
        if not doc_ids or type(doc_ids) != list:
            errors['doc_ids'] = 'Provide doc_ids. It should be a list of integers.'
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
