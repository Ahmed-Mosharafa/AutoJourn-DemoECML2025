from transformers import pipeline
from summarization.summarization import Summarization

import re

class BartSummarizationModel(Summarization):
    def __init__(self, num_random_samples):
        self.summarizer = pipeline("summarization", model="lidiya/bart-base-samsum")
        self.num_random_samples = num_random_samples

    def preprocess(self, conversation):
        # Remove links
        conversation = re.sub(r"http\S+", "", conversation)
        # Remove tags
        conversation = re.sub(r"@\S+", "", conversation) #remove tags
        # Encode and decode in order to UTF-16 in order to process emojis.
        conversation = conversation.encode('UTF-16', 'surrogatepass').decode(encoding='UTF-16')
        return conversation

    def summarize(self, tweets):
        random_tweets = self.pick_random_tweets(tweets)
        summary = self.summarizer("".join(random_tweets))[0]["summary_text"]
        return summary
