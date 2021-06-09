from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class TopicModeling(ABC):

    @abstractmethod
    def get_topics(self, docs):
        """
        run topic modeling model to get the topics associated to each document in docs with optional
        topics assignments probabilities.

        :param docs: List[String]: list of documents input to the topic modeling model.
        :return:
        """
        pass

    @abstractmethod
    def preprocess(self, tweet):
        """
        Preprocess tweet by removing tags, links, etc.,
        :param tweet: String: single tweet text
        :return: String: processed tweet text.
        """
        pass

    def __merge_tweets(self, data):
        """
        Parse the tweets conversations in SAMSum format ot documents.
        Each processed conversation is treated as a document.

        :param data: List[{conv_id:String -> tweets:[String]}]
        :return: <List[document:String], Dict{document:String -> conv_id:String}>
        """

        doc_conv_dict = {}  # Map each processed document to its conversation
        docs = []
        for conv_dict in data:
            conv_id, conv = next(iter(conv_dict.items()))  # each conv dictionary has one item {conv_id: [tweets]}
            processed_conv = []
            for tweet in conv:
                processed_conv.append(self.preprocess(tweet))

            processed_doc = ''.join(processed_conv)  # flatten each conversation as one document

            # Some conversation after being processed may be similar. Since, we have to keep them unique to be able
            # to map them back to original conversations, therefore, we add a suffixed special characters.
            while processed_doc in doc_conv_dict:
                processed_doc += "."

            docs.append(processed_doc)

        return docs, doc_conv_dict

    def __flatten_tweets(self, data):
        """
        Parse the tweets conversations in SAMSum format ot documents. One processed tweet is treated as a document.
        :param data: List[{conv_id:String -> tweets:[String]}]
        :return: <List[document:String], Dict{tweet:String -> conv_id:String},
            Dict{processed_tweet:String -> origin_tweet:String}>.
        """
        tweet_conv_dict = {}  # Map each tweet to its conversation
        processed_origin_tweet_dict = {}  # map processed tweet to original one
        docs = []
        for conv_dict in data:
            conv_id, conv = next(iter(conv_dict.items()))  # each conv dictionary has one item {conv_id: [tweets]}
            for tweet in conv:
                tweet_conv_dict[tweet] = conv_id
                t_tweet = self.preprocess(tweet)

                # Some tweets after being processed will be similar. Since, we have to keep them unique to be able
                # to map them back to original tweets, therefore, we add a suffixed special characters.
                while t_tweet in processed_origin_tweet_dict:
                    t_tweet += "."

                processed_origin_tweet_dict[t_tweet] = tweet
                docs.append(t_tweet)

        return docs, tweet_conv_dict, processed_origin_tweet_dict

    def run_tweet_topic_modeling(self, data):
        """
        Run topic modeling model on tweet conversations in SAMSum format. It treats each tweet as a document and
        determine a topic for each tweet. Then, we average the probabilities for all tweets associated to a single
        conversation to get the topic probabilities for each conversation.

        :param data: List[{conv_id:String -> tweets:[String]}]
        :return: <conv_topic_probs_df: DataFrame, topics_df DataFrame>:
            1- conv_topic_probs_df: each row is for a conversation and each column represent a topic probability.
            2- topics_df: each row is a topic and its assigned name based on tf-idf (i.e., top terms
                indicating the topic)
        """

        docs, tweet_conv_dict, processed_origin_tweet_dict = self.__flatten_tweets(data)  # each tweet is a document
        topics_df, probs = self.get_topics(data)

        conv_tweet_topic_prob = {}
        for idx, tweet in enumerate(docs):
            t_probs = probs[idx]
            t_conv = tweet_conv_dict[processed_origin_tweet_dict[tweet]]

            if t_conv not in conv_tweet_topic_prob:
                conv_tweet_topic_prob[t_conv] = []

            conv_tweet_topic_prob[t_conv].append(t_probs)

        conv_topic_probs = {}
        for conv_id, tweets_tprobs in conv_tweet_topic_prob.items():
            mat = np.stack(tweets_tprobs, axis=0)  # create np matrix from list[np array] for faster computations
            conv_tprobs = np.average(mat, axis=0)  # compute average <tweet, topic> probability for each topic
            conv_topic_probs[conv_id] = conv_tprobs

        # transpose to make the rows for conversations and columns are topics probabilities
        conv_topic_probs_df = pd.DataFrame(conv_topic_probs).transpose()
        conv_topic_probs_df = conv_topic_probs_df.reset_index().rename(columns={"index": "conv_id"})

        return conv_topic_probs_df, topics_df

    def run_con_topic_modeling(self, data):
        """
        Run topic modeling model on tweet conversations in SAMSum format. It treats each conversation as a document and
        determine a topic for each conversation.

        :param data: List[{conv_id:String -> tweets:[String]}]
        :return: <conv_topic_probs_df: DataFrame, topics_df DataFrame>:
            1- conv_topic_probs_df: each row is for a conversation and each column represent a topic probability.
            2- topics_df: each row is a topic and its assigned name based on tf-idf (i.e., top terms
                indicating the topic)
        """

        docs, doc_conv_dict = self.__merge_tweets(data)  # each conversation is a document
        topics_df, probs = self.get_topics(data)

        conv_topic_probs = {}
        for idx, d in enumerate(docs):
            conv_id = doc_conv_dict[d]
            conv_topic_probs[conv_id] = probs[idx]

        # transpose to make the rows for conversations and columns are topics probabilities
        conv_topic_probs_df = pd.DataFrame(conv_topic_probs).transpose()
        conv_topic_probs_df = conv_topic_probs_df.reset_index().rename(columns={"index": "conv_id"})

        return conv_topic_probs_df, topics_df
