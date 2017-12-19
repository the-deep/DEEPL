from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

import pickle

from classifier.models import ClassifierModel
from topic_modeling.lda import LDAModel, get_topics_and_subtopics
from topic_modeling.keywords_extraction import get_key_ngrams

class DocumentClassifierView(APIView):
    """
    API for document classification
    """
    def post(self, request, version):
        data = dict(request.data.items())
        validation_details = self._validate_classification_params(data)
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
        # strip 'v' at the beginning
        version = version[1:]
        classifier_model = get_object_or_404(ClassifierModel, version=version)
        classifier = pickle.loads(classifier_model.data)
        classified = classifier.classify_as_label_probs(data['text'].split())
        classified.sort(key=lambda x: x[1], reverse=True)
        # classified = classifier.classify(data['text'].split())
        return Response({'status': True, 'tags': classified})

    def _validate_classification_params(self, params):
        """Validator for params"""
        errors = {}
        if not params.get('text'):
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
