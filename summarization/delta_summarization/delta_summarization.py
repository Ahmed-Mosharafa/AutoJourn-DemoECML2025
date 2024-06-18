from typing import Dict
import numpy as np
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt

summary1 = '''A Bugatti Chiron, powerd by its turbocharged 8 liter engine with 16 cylinder4s and 1600 horse- 
power, drove at record braking speeds of up to 417 
kilometers per hour on a german motorway. With
a top speed of 440 kilometers per hour, the sports
car is one of the fastest legal road vehicles.'''
summary2 = '''
German politicians demand a general speed limit
due to safety and environmental reasons after a
car legally drove at a very high speed on a public
road.
'''


class DeltaSummarization:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def find_cosine_similarity(self, summary1: str, summary2: str):
        embedding1 = self.model.encode(summary1, convert_to_tensor=True)
        embedding2 = self.model.encode(summary2, convert_to_tensor=True)
        cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
        return cosine_similarity

    def create_cosine_similarity_matrix(self, topic_summaries: Dict[str, str]):
        topics = list(topic_summaries.keys())
        topic_summaries = list(topic_summaries.items())
        summary_count = len(topic_summaries)
        cosine_similarity_matrix = np.zeros((summary_count, summary_count))
        for idx in range(summary_count):
            for jdx in range(summary_count):
                # Cosine similarity is 1 if the same topics are being compared.
                if idx == jdx:
                    cosine_similarity_matrix[idx][jdx] = 1.0
                else:
                    cosine_similarity = self.find_cosine_similarity(topic_summaries[idx][1], topic_summaries[jdx][1])
                    cosine_similarity_matrix[idx][jdx] = cosine_similarity

        plt.imshow(cosine_similarity_matrix, cmap='viridis')
        plt.colorbar(label='Matrix Values')
        n = len(topics)
        plt.xticks(np.arange(n), topics, rotation='vertical')
        plt.yticks(np.arange(n), topics)
        plt.xlabel('Topics')
        plt.ylabel('Topics')
        title = 'Cosine Similarity between Topics'
        plt.title(title)
        # Adjust the figure size and margins
        plt.gcf().set_size_inches(10, 8)
        plt.tight_layout()
        plt.show()
        return cosine_similarity_matrix

    def create_2d_scatter_plot(self):
        pass


delta = DeltaSummarization()
delta.find_cosine_similarity(summary1, summary2)
topic_summaries = {
    "0_you_to_it_the": "May is depressed and doesn't want to see anyone. Karen will call someone for advice.",
    "2_doctor_and_to_the": "Adam and Karen worry about her. Karen suggested she should see a specialist. Adam has a friend who is a psychologist. ",
    "7_the_is_ignorant_all": "Adam needs someone to call"}
delta.create_cosine_similarity_matrix(topic_summaries)
