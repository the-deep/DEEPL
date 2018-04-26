from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from similarity.globals import get_similarity_model
from similarity.helpers import get_similar_docs
from classifier.models import ClassifiedDocument
from clustering.models import ClusteringModel


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
                document = ClassifiedDocument.objects.get(id=docid)
            except ClassifiedDocument.DoesNotExist:
                return Response({'error': 'Document not found for given id'},
                                status=status.HTTP_404_NOT_FOUND)
            group_id = document.group_id
        elif doc:
            group_id = data['group_id']
        else:
            return Response(
                {'error': 'something went wrong. try later'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # try to get clsutering model
        try:
            clustering_model = ClusteringModel.objects.get(
                group_id=group_id
            )
        except ClusteringModel.DoesNotExist:
            return Response(
                {'error': 'Cannot find clustering model for the group id'},
                status=status.HTTP_404_NOT_FOUND
            )
        if docid:
            similar_docs = clustering_model.get_similar_docs(docid)
        elif doc:
            model = clustering_model.model
            features = model.vectorizer.fit_transform([doc])[0]
            label = model.model.predict(features)
            similar_docs = clustering_model.get_similar_docs_for_label(label)
        return Response({'similar_docs': [int(x) for x in similar_docs]})

    def _validation(self, data):
        errors = {}
        doc = data.get('doc')
        docid = data.get('doc_id')
        group_id = data.get('group_id')
        if (not doc or not doc.strip()) and (not docid or not docid.strip()):
            errors['doc_id'] = "Either doc_id or doc should be present"
            errors['doc'] = "Either doc_id or doc should be present"
        elif doc and doc.strip():
            if not group_id:
                errors['group_id'] = "group_id should be present if doc only is provided"
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
