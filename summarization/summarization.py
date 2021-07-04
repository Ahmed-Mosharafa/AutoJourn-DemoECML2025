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

    def run(self, data):
        """
        Run text summarization model on tweet conversations in SAMSum format. It outputs a summary to each conversation.

        :param data: List[{conv_id:String -> tweets:[String]}]
        :return: conv_summary_dict: Dict{conv_id:String -> summary:String}
        """
        conv_summary_dict = {}
        for conv_dict in data:
            conv_id, tweets = next(iter(conv_dict.items()))  # each conv dictionary has one item {conv_id: [tweet]}
            merged_tweets = ''.join(tweets)
            preprocessed_tweets = self.preprocess(merged_tweets)
            summary = self.summarize(preprocessed_tweets)
            conv_summary_dict[conv_id] = summary

        return conv_summary_dict
