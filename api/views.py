from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

import pickle

from core.models import ClassifierModel

class DocumentClassifierView(APIView):
    """
    API for document classification
    """
    def get(self, request):
        data = dict(request.query_params.items())
        validation_details = self._validate_classification_params(data)
        if not validation_details['status']:
            return Response(validation_details['error_data'], status=status.HTTP_400_BAD_REQUEST)
        classifier_model = ClassifierModel.objects.all().first() # TODO: select model from url/user data
        classifier = pickle.loads(classifier_model.data)
        classified = classifier.classify(data['text'])
        return Response({'status': True, 'classification': classified})

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
