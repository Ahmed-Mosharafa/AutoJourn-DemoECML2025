import ast
import numpy as np
import pandas as pd
import torch
from src import preprocessing, nltk_utilities
from src.sentence_transformer_utilities import SentTransfUtilities


class TopicAwareSummarization:
    def __init__(self):
        self.sentence_transformer_model = "paraphrase-multilingual-MiniLM-L12-v2"

    def get_emb_cluster_topic(self, sentTransfModelUtilsObj):
        df_latVectorRep = pd.read_csv('../../data/_20news_df_output_clusterId_label_words.csv')
        df_latVectorRep["sentence_from_words"] = df_latVectorRep["list_topic_words"].map(
            lambda x: " ".join(ast.literal_eval(x)))
        list_embeddings_cluster_sentences = list()

        for index, row in df_latVectorRep.iterrows():
            list_embeddings_cluster_sentences.append(sentTransfModelUtilsObj.get_embeddings(row["sentence_from_words"]))

        return list_embeddings_cluster_sentences, df_latVectorRep

    def text_to_sentences(self, data):
        list_sentences = [*nltk_utilities.NltkSegmentizer().segment_into_sentences(data)]
        return list_sentences

    def preprocess(self, list_sentences, sentTransfModelUtilsObj):

        list_sentences = [preprocessing.remove_patterns(x) for x in list_sentences]
        list_sentences_per_doc_embeddings = [sentTransfModelUtilsObj.get_embeddings(x) for x in list_sentences if
                                             len(x) > 0]
        return list_sentences_per_doc_embeddings, list_sentences

    def compute_similarity_matrix(self, list_sentences_per_doc_embeddings, list_sentences, sentTransfModelUtilsObj,
                                  topic_embeddings, topics_df):

        # list_embeddings_cluster_sentences, df_latVectorRep = get_emb_cluster_topic(sentTransfModelUtilsObj)

        similarity_matrix = np.zeros((len(topic_embeddings), len(list_sentences_per_doc_embeddings)))

        for i, cluster_embedding in enumerate(topic_embeddings):
            cluster_embedding = torch.from_numpy(cluster_embedding)
            for j, sentence_embedding in enumerate(list_sentences_per_doc_embeddings):
                sentence_embedding = sentence_embedding.to(torch.float64)
                similarity_matrix[i][j] = sentTransfModelUtilsObj.compute_cosine_similarity(cluster_embedding,
                                                                                            sentence_embedding)

        list_index_topics_within_matrix = np.argmax(similarity_matrix, axis=0)

        dict_topic_sentences = dict()
        topic_labels = topics_df["Name"].values.tolist()
        for index_sentence, index_id_topic in enumerate(list_index_topics_within_matrix):
            label_class = topic_labels[index_id_topic]
            if label_class not in dict_topic_sentences.keys():
                dict_topic_sentences[label_class] = list()
            dict_topic_sentences[label_class].append(list_sentences[index_sentence])

        return dict_topic_sentences

    def get_similarity_matrix(self, data) -> dict:
        sent_transf_model_utils_obj = SentTransfUtilities(model_name=self.sentence_transformer_model)
        data_sentences = self.text_to_sentences(data)
        data_embed, list_sentences = self.preprocess(data_sentences, sent_transf_model_utils_obj)
        return self.compute_similarity_matrix(data_embed, list_sentences, sent_transf_model_utils_obj)

    def extract_topic_sentences(self, conv_docs, topics_df, topic_embeddings):
        sent_transf_model_utils_obj = SentTransfUtilities(model_name=self.sentence_transformer_model)
        # Topic sentence matrix for each conversation.
        topic_sentence_matrices = []
        for conv in conv_docs:
            data_sentences = self.text_to_sentences(conv['dialogue'])
            sentence_embed, list_sentences = self.preprocess(data_sentences, sent_transf_model_utils_obj)
            dict_topic_sentences = self.compute_similarity_matrix(sentence_embed, list_sentences,
                                                                  sent_transf_model_utils_obj, topic_embeddings,
                                                                  topics_df)
            dict_topic_sentences['id'] = conv['id']
            topic_sentence_matrices.append(dict_topic_sentences)
        return topic_sentence_matrices
