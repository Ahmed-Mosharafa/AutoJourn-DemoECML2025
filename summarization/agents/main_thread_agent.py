from typing import Dict, List

from summarization.agents.agent import Agent
from summarization.models.summarizer import SummarizationModel


class MainThreadAgent(Agent):
    def __init__(self, summarizer_model: SummarizationModel):
        super(MainThreadAgent, self).__init__(summarizer_model)

    @staticmethod
    def get_main_thread(conv_root: Dict) -> List[Dict]:
        main_thread = [conv_root]

        # no replies to head tweet. The conversation is only one tweet
        if "replies" not in conv_root or ("replies" in conv_root and len(conv_root["replies"]) == 0):
            return main_thread

        # Iterate over replies of head tweet and add it to the main thread
        for reply in conv_root["replies"]:
            main_thread.append(reply)

        return main_thread

    def run_conv(self, conv_root: Dict) -> str:
        print(8)
        #main_thread = self.get_main_thread(conv_root)
        print("conv type:",type(conv_root))
        conv_root_list = conv_root.split("\n")
        #tweets_list = [tweet["username"] + ":" + tweet["text"] for tweet in main_thread]
        print(conv_root_list)
        summary = self.summarizer_model.summarize(conv_root_list)
        print(11)
        return summary
    
    def topic_based_summarize(self, conv_tweets_list):
        # 1. Topic Extraction
        topics = self.extract_topics(conv_tweets_list)

        # 2. Assign Tweets to Topics
        tweets_by_topic = self.assign_tweets_to_topics(conv_tweets_list, topics)

        # 3. Generate Topic-Based Summaries
        topic_summaries = {}
        for topic, tweets in tweets_by_topic.items():
            topic_summary = self.summarize(tweets)  # Use your existing summarization function
            topic_summaries[topic] = topic_summary

        return topic_summaries
