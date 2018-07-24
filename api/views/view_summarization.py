from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from gensim.summarization import summarize as summarize_text

from helpers.common import text_to_sentences
from classifier.models import ClassifiedDocument


class SummarizationView(APIView):
    """
    API for text summarization
    """
    def get(self, request):
        data = dict(request.query_params.items())
        validation = validate_summarization_data(data)
        if not validation['status']:
            return Response(
                validation['errors'],
                status=status.HTTP_400_BAD_REQUEST
            )
        if data.get('doc_id'):
            qs = ClassifiedDocument.objects.filter(id=data['doc_id'])
            if not qs.exists():
                return Response(
                    {'message': 'Document corresponding to doc_id does not exist'},  # noqa
                    status=status.HTTP_404_NOT_FOUND
                )
            text = qs[0].text
        else:
            text = data.get('text')
        return Response(
            {'summary': summarize_text(text)}
        )


def validate_summarization_data(data):
    errors = {}
    doc_id = data.get('doc_id')
    text = data.get('text')
    if not doc_id and not text:
        errors['doc_id'] = 'Either doc_id or text should be present'
        errors['text'] = 'Either text or doc_id should be present'
    elif not doc_id:
        # check if text is too short
        sentences = text_to_sentences(text.strip())
        if not len(sentences) >= 4:
            errors['text'] = 'text is too short'
    if errors:
        return {
            'status': False,
            'errors': errors
        }
    return {
        'status': True,
        'data': data
    }
