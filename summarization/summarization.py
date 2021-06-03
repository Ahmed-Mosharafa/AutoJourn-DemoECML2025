from abc import ABC, abstractmethod

class Summarization(ABC):

    @abstractmethod
    def preprocess(self, conversation):
        """
        Preprocess whole conversation by removing tags, links, etc.,
        :param conversation: String: single conversation text
        :return: String: processed conversation text.
        """
        pass

    @abstractmethod
    def summarize(self, conversation):
        """
        Summarize the conversation given in the input,
        :param conversation: String: conversation in Samsum format
        :return: String: summary of the input tweets
        """
        pass

    def run(self, tweets):
        merged_tweets = ''.join(tweets)
        preprocessed_tweets = self.preprocess(merged_tweets)

        return self.summarize(preprocessed_tweets)
