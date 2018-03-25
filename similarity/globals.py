from .document_similarity import DocumentSimilarityModel

__similarity_model = None


def init():
    global __similarity_model
    try:
        __similarity_model = DocumentSimilarityModel()
    except Exception:
        # sometimes when indices haven't been created, exception can be thrown
        pass


def get_similarity_model():
    return __similarity_model


def set_similarity_model():
    if not __similarity_model:
        init()
