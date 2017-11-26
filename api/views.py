from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

import pickle

from classifier.models import ClassifierModel
from topic_modeling.lda import LDAModel

class DocumentClassifierView(APIView):
    """
    API for document classification
    """
    def get(self, request, version):
        data = dict(request.query_params.items())
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
            errors['text'] = 'Please provide the text to be classified'
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
    def get(self, request):
        """Handle API GET request"""
        data = dict(request.query_params.items())
        validation_details = self._validate_classification_params(data)
        if not validation_details['status']:
            return Response(
                validation_details['error_data'],
                status=status.HTTP_400_BAD_REQUEST
            )
