from transformers import pipeline
from summarization.summarization import Summarization

import re

class BartSummarizationModel(Summarization):
    def __init__(self):
        self.summarizer = pipeline("summarization", model="lidiya/bart-base-samsum")

    def preprocess(self, conversation):
        # Remove links
        conversation = re.sub(r"http\S+", "", conversation)
        # Remove tags
        conversation = re.sub(r"@\S+", "", conversation) #remove tags
        # Encode and decode in order to UTF-16 in order to process emojis.
        conversation = conversation.encode('UTF-16', 'surrogatepass').decode(encoding='UTF-16')
        return conversation

    def summarize(self, conversation):
        summary = ""
        for i in range(0, len(conversation), 600):
            part_summary = self.summarizer(conversation[i: min(i + 600, len(conversation))])[0]["summary_text"]
            summary += part_summary

        return summary
