from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

import pickle

from api.helpers import classify_text, classify_lead_excerpts

from classifier.models import (
    ClassifierModel,
    ClassifiedDocument,
    ClassifiedExcerpt,
    Recommendation,
)
from classifier.serializers import ClassifiedDocumentSerializer, ClassifiedExcerptSerializer
from topic_modeling.lda import LDAModel, get_topics_and_subtopics
from topic_modeling.keywords_extraction import get_key_ngrams
from NER.ner import get_ner_tagging

class DocumentClassifierView(APIView):
    """
    API for document classification
    """
    classifiers = {'v'+str(x.version) : {
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
                classified_doc = ClassifiedDocument.objects.get(id=data['doc_id'])
                return_data = ClassifiedDocumentSerializer(classified_doc).data
                return_data['excerpts_classification'] = ClassifiedExcerptSerializer(
                    classified_doc.excerpts, many=True
                ).data
                return Response(return_data)
            except ClassifiedDocument.DoesNotExist:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Resposne({
                    'status': False,
                    'message': 'Invalid doc_id'
                }, status=status.HTTP_400_BAD_REQUEST)
        classifier = DocumentClassifierView.classifiers.get(version)

        if not classifier:
            return Response({'status': False, 'message': 'Classifier not found'},
                status.HTTP_404_NOT_FOUND
            )
        text = data['text']
        classified = classify_text(classifier['classifier'], text)

        if not data.get('deeper'):
            return Response({'classification': classified})

        # Create classified Document
        grp_id = data.get('group_id')

        doc = ClassifiedDocument.objects.create(
            text = text,
            classifier = classifier['classifier_model'],
            confidence = classified[0][1],
            classification_label = classified[0][0],
            classification_probabilities = classified,
            group_id = grp_id
        )
        classified_excerpts = classify_lead_excerpts(classifier['classifier'], text)

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
        ldamodel = LDAModel()
        lda_output = get_topics_and_subtopics(
            params['documents'],
            params['number_of_topics'],
            params['keywords_per_topic'],
            depth=5 if params['depth'] > 5 else params['depth']
        )
        return Response(lda_output)
        ldamodel.create_model(params['documents'], params['number_of_topics'])
        topics_and_keywords = ldamodel.get_topics_and_keywords(
            params['keywords_per_topic']
        )
        return Response({'Topic {}'.format(i+1): v for i,v in enumerate(topics_and_keywords)})

    def _validate_topic_modeling_params(self, queryparams):
        """Validator for params"""
        errors = {}
        params = {}
        if not queryparams.getlist('documents', []):
            errors['documents'] = 'Missing documents on which modeling is to be done'
        elif not type(queryparams.getlist('documents')) == list:
            errors['documents'] = 'documents should be list'
        else:
            # this is a list
            params['documents'] = queryparams.getlist('documents')
            # params['documents'] = queryparams.getlist('documents')
        try:
            num_topics = int(queryparams.get('number_of_topics'))
        except:
            errors['number_of_topics'] = 'Missing/invalid number of topics. Should be present as a positive integer'
        else:
            params['number_of_topics'] = num_topics
        try:
            kw_per_topic = int(queryparams.get('keywords_per_topic'))
        except:
            errors['keywords_per_topic'] = 'Missing/invalid number of keywords per topic. Should be present as a positive integer'
        else:
            params['keywords_per_topic'] =  kw_per_topic
        try:
            depth = int(queryparams.get('depth'))
        except:
            errors['depth'] = 'Missing/invalid depth of subtopics. Should be present as a positive integer'
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
        validation_details = self._validate_keywords_extraction_params(request.data)
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
        params = validation_details['params']
        doc = params['document']
        args = (doc, params['max_grams']) if params['max_grams'] else (doc,)
        key_ngrams = get_key_ngrams(*args)
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
            except:
                errors['max_grams'] = 'max_grams, if present, should be a positive integer'
        else:
            params['max_grams'] = None
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
        return Response({"versions":versions})

class RecommendationView(APIView):
    def post(self, request, version):
        data = dict(request.data.items())
        validation_details = self._validate_recommendation_params(data)
        if not validation_details['status']:
            return Response(validation_details, status=status.HTTP_400_BAD_REQUEST)

        classifier = DocumentClassifierView.classifiers.get(version)
        if not classifier:
            return Response (
                {'message': 'Classifier not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        # create a Recommendation object
        recomm = Recommendation.objects.create (
            classifier=classifier['classifier_model'],
            text=data['text'],
            classification_label=data['classification_label'],
            useful=True if data['classification_label'].lower() == 'true' else False
        )
        return Response({'message': 'Recommendation added successfully.'})

    def _validate_recommendation_params(self, data):
        errors = {}
        if not data.get('text'):
            errors['text'] = 'text for recommendation is missing'
        if not data.get('classification_label'):
            errors['classification_label'] = 'classissification_label is missing'
        if not data.get('useful'):
            errors['useful'] = 'Missing value for usefulness of the recommendation'
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {'status': True}

class NERView(APIView):
    def post(self, request):
        data = dict(request.data.items())
        validation_details = self._validate_ner_params(data)
        if not validation_details['status']:
            return Response(validation_details, status=status.HTTP_400_BAD_REQUEST)
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
