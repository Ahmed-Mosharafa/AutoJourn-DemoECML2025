### Imports
from sentence_transformers import SentenceTransformer, util

### Classes and functions

##==========================================================================================================
class SentTransfUtilities:
    ##==========================================================================================================
    """
    Definition of attributes
    """
    model = None
    __model_name = None
    ##==========================================================================================================
    """
    Function: __init__
    Arguments:
        - model_name:
            Options:
                - 'all-MiniLM-L6-v2
                - 'nq-distilbert-base-v1'
                - 'paraphrase-multilingual-MiniLM-L12-v2'
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.__model_name = model_name
        if self.model == None:
            print("Initializing the Sentence Transformer model")
            self.model = SentenceTransformer(self.__model_name)
    ##==========================================================================================================
    """
    Function: get_embeddings()
    """
    def get_embeddings(self, src_data):
        return self.model.encode(src_data, convert_to_tensor=True, device='cpu')
    ##==========================================================================================================
    """
    Function: compute_cosine_similarity(query_embeddings, passage_embeddings)
    """
    def compute_cosine_similarity(self, query_embeddings, passage_embeddings):
        #Compute cosine-similarities
        cosine_scores = util.cos_sim(query_embeddings, passage_embeddings)
        return cosine_scores
    ##==========================================================================================================
    """
    Function: compute_dot_similarity(query_embeddings, passage_embeddings)
    Arguments:
        - query_embeddings
        - passage_embeddings
    """
    def compute_dot_similarity(self, query_embeddings, passage_embeddings):
        #Compute dot-similarities
        dot_scores = util.dot_score(query_embeddings, passage_embeddings)
        return dot_scores
    ##==========================================================================================================
    """
    Function: compute_semantic_search(query_embeddings, corpus_embeddings)
    Arguments:
        - query_embeddings
        - corpus_embeddings
    """
    def compute_semantic_search(self, query_embeddings, corpus_embeddings):
        #Compute dot-similarities
        dot_scores = util.semantic_search(query_embeddings, corpus_embeddings)
        return dot_scores
    ##==========================================================================================================
    """
    Function: compute_sentences_similarity(sentence_1, sentence_2, sim_func)
    Arguments:
        - sentence_1
        - sentence_2
        - sim_func: { "cosine", "dot" }
    """
    def compute_sentences_similarity(self, sentence_1, sentence_2, sim_func="cosine"):
        embeddings_1 = self.get_embeddings(sentence_1)
        embeddings_2 = self.get_embeddings(sentence_2)

        scores = None
        if sim_func == "cosine":
            scores = self.compute_cosine_similarity(embeddings_1, embeddings_2)
        elif sim_func == "dot":
            scores = self.compute_dot_similarity(embeddings_1, embeddings_2)
        return scores
    ##==========================================================================================================

##==========================================================================================================
