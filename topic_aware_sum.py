import ast
import numpy as np
import pandas as pd

import pickle

from src import preprocessing, nltk_utilities
from src.sentence_transformer_utilities import SentTransfUtilities

def get_emb_cluster_topic(sentTransfModelUtilsObj):

  df_latVectorRep = pd.read_csv('data/_20news_df_output_clusterId_label_words.csv')
  df_latVectorRep["sentence_from_words"] = df_latVectorRep["list_topic_words"].map(lambda x: " ".join(ast.literal_eval(x)))
  list_embeddings_cluster_sentences = list()

  for index, row in df_latVectorRep.iterrows():
      list_embeddings_cluster_sentences.append(sentTransfModelUtilsObj.get_embeddings(row["sentence_from_words"]))

  return list_embeddings_cluster_sentences, df_latVectorRep

def text_to_sentences(data):

  list_sentences = [*nltk_utilities.NltkSegmentizer().segment_into_sentences(data)]

  return list_sentences

def preprocess(list_sentences, sentTransfModelUtilsObj):

  list_sentences = [preprocessing.remove_patterns(x) for x in list_sentences]
  list_sentences_per_doc_embeddings = [sentTransfModelUtilsObj.get_embeddings(x) for x in list_sentences if len(x) > 0]
  return list_sentences_per_doc_embeddings, list_sentences


def compute_similarity_matrix(list_sentences_per_doc_embeddings, list_sentences, sentTransfModelUtilsObj):

  list_embeddings_cluster_sentences, df_latVectorRep = get_emb_cluster_topic(sentTransfModelUtilsObj)

  similarity_matrix = np.zeros((len(list_embeddings_cluster_sentences), len(list_sentences_per_doc_embeddings)))

  for i, cluster_embedding in enumerate(list_embeddings_cluster_sentences):
    for j, sentence_emebedding in enumerate(list_sentences_per_doc_embeddings):
        similarity_matrix[i][j] = sentTransfModelUtilsObj.compute_cosine_similarity(cluster_embedding, sentence_emebedding)

  list_index_topics_within_matrix = np.argmax(similarity_matrix, axis=0)

  dict_topic_sentences = dict()

  for index_sentence, index_id_topic in enumerate(list_index_topics_within_matrix):
      label_class = df_latVectorRep.iloc[index_id_topic]["label_class"]
      
      if label_class not in dict_topic_sentences.keys():
          dict_topic_sentences[label_class] = list()
      dict_topic_sentences[label_class].append(list_sentences[index_sentence])

  return dict_topic_sentences


def get_similarity_matrix(data) -> dict:
    print('1')
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    sentTransfModelUtilsObj = SentTransfUtilities(model_name=MODEL_NAME)
    print('12')
    data_sentences = text_to_sentences(data)
    print('13')
    data_embed, list_sentences = preprocess(data_sentences, sentTransfModelUtilsObj)
    print('14')
    return compute_similarity_matrix(data_embed, list_sentences, sentTransfModelUtilsObj)