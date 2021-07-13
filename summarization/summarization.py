from abc import ABC, abstractmethod

import random

class Summarization(ABC):

    @abstractmethod
    def preprocess(self, tweets):
        """
        Preprocess whole conversation by removing tags, links, etc.,
        :param tweets: List[String]: tweets in text format
        :return: String: processed conversation text.
        """
        pass

    @abstractmethod
    def summarize(self, tweets):
        """
        Summarize the conversation given in the input,
        :param tweets: List[String]: tweets in Samsum format
        :return: String: summary of the input tweets
        """
        pass

    def run(self, data):
        """
        Run text summarization model on tweet conversations in SAMSum format. It outputs a summary to each conversation.

        :param data: List[{conv_id:String -> tweets:[String]}]
        :return: conv_summary_dict: Dict{conv_id:String -> summary:String}
        """
        conv_summary_dict = {}
        for conv_dict in data:
            conv_id, tweets = next(iter(conv_dict.items()))  # each conv dictionary has one item {conv_id: [tweet]}
            preprocessed_tweets = [self.preprocess(tweet) for tweet in tweets]
            summary = self.summarize(preprocessed_tweets)
            conv_summary_dict[conv_id] = summary

        return conv_summary_dict

    def pick_random_tweets(self, tweets):
        # Max tweet size (characters) = 280
        # Max input tokens size (BPE encoding) = 1024
        # In order to fit in 1024 encoding size, let us choose < 1500 characters
        # (empirically chosen).
        # That would mean 6 tweets .
        # Hence, we randomly select 6 tweets.

        if len(tweets) <= self.num_random_samples:
            return tweets

        reservoir = [tweets[i] for i in range(self.num_random_samples)]

        for i in range(self.num_random_samples, len(tweets)):
            j = random.randrange(i + 1)
            if j < self.num_random_samples:
                reservoir[j] = tweets[i]

        idx_set = set([])
        while len(idx_set) < self.num_random_samples:
            rand_idx = random.randrange(len(tweets))
            if rand_idx not in idx_set:
                idx_set.add(rand_idx)

        idx_set = sorted(idx_set)
        reservoir = [tweets[k] for k in idx_set]

        return reservoir
