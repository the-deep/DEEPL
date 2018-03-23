from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from similarity.globals import get_similarity_model
from similarity.helpers import get_similar_docs
from classifier.models import ClassifiedDocument


class DocsSimilarityView(APIView):
    """
    API for finding out similarity between two input texts
    """
    def post(self, request):
        data = dict(request.data.items())
        validation_details = self._validation(data)
        if not validation_details['status']:
            return Response(validation_details['error_data'],
                            status=status.HTTP_400_BAD_REQUEST)
        doc1 = data['doc1']
        doc2 = data['doc2']
        similarity_model = get_similarity_model()
        similarity = similarity_model.documents_similarity(doc1, doc2)
        return Response(
            {'similarity': similarity}
        )

    def _validation(self, data):
        errors = {}
        doc1 = data.get('doc1')
        doc2 = data.get('doc2')
        if not doc1 or not doc1.strip():
            errors['doc1'] = 'doc1 not present'
        if not doc2 or not doc2.strip():
            errors['doc2'] = 'doc2 not present'
        if errors:
            return {
                'status': False,
                'error_data': errors
            }
        return {
            'status':  True,
            'error_data': {},
            'data': data
        }


class SimilarDocsView(APIView):
    """
    API for returning similar docs, given a doc id
    """
    def post(self, request):
        data = dict(request.data.items())
        validation_details = self._validation(data)
        if not validation_details['status']:
            return Response(validation_details['error_data'],
                            status=status.HTTP_400_BAD_REQUEST)
        docid = data.get('doc_id')
        doc = data.get('doc')
        if docid:
            # get classified doc and extract text
            try:
                doc = ClassifiedDocument.objects.get(id=docid).text
            except ClassifiedDocument.DoesNotExist:
                return Response({'error': 'Document not found for given id'},
                                status=status.HTTP_404_NOT_FOUND)
        similarity_model = get_similarity_model()
        similar_docs = get_similar_docs(doc, similarity_model)
        return Response({'similar_docs': similar_docs})

    def _validation(self, data):
        errors = {}
        doc = data.get('doc')
        docid = data.get('doc_id')
        if (not doc or not doc.strip()) and (not docid or not docid.strip()):
            errors['doc_id'] = "Either doc_id or doc should be present"
            errors['doc'] = "Either doc_id or doc should be present"
        elif docid:
            try:
                docid = int(docid)
                if docid < 0:
                    raise ValueError()
            except (ValueError, TypeError):  # typeerror for None value
                errors['doc_id'] = 'doc_id should be positive integer'

        if not errors:
            return {
                'status': True,
                'data': data,
                'error_data': errors
            }
        return {
            'status': False,
            'error_data': errors
        }
