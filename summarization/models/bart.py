from transformers import pipeline, AutoTokenizer
from typing import List

from summarization.models.summarizer import SummarizationModel
import nltk
import re


class Bart(SummarizationModel):
    def __init__(self, model):
        self._tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = pipeline("summarization", model=model)
        nltk.download('punkt')

    def preprocess(self, tweet):
        # Remove links
        tweet = re.sub(r"http\S+", "", tweet)
        # Remove tags
        tweet = re.sub(r"@\S+", "", tweet)  # remove tags
        # Encode and decode in order to UTF-16 in order to process emojis.
        tweet = tweet.encode('UTF-16', 'surrogatepass').decode(encoding='UTF-16')
        # remove leading and trailing spaces.
        tweet = tweet.strip()
        return tweet

    def __chunk_conversation(self, conv_tweets_list: List[str]) -> List[str]:
        """
        Takes a conversation which is a list of tweets. Since the BART model has limit on the input size,
        therefore, we have divide the tweets into chucks where each chunk has length = model max input lengthIt.

        The chunk is the concatenation of tweets where the total length <= model max input length.

        :param conv_tweets_list: List[tweets:[String]]
        :return: chunks: [String]
        """
        chunks = []
        chunk = ''
        length = 0

        for tweet in conv_tweets_list:
            tokenized_tweet = self._tokenizer.encode(tweet, truncation=False, max_length=None, return_tensors='pt')[0]

            if len(tokenized_tweet) > self._tokenizer.model_max_length:
                continue

            length += len(tokenized_tweet)

            if length <= self._tokenizer.model_max_length:  # append to current chunk
                chunk += tweet + "\n"  # in SAMSum format each tweet (i.e., conversation turn) should be in a new line
            else:  # create new chunk
                chunks.append(chunk)
                chunk = tweet
                length = len(tokenized_tweet)

        if len(chunk) > 0:  # check last chunk
            chunks.append(chunk)

        return chunks

    def summarize(self, conv_tweets_list):
        conv_tweets_list = [self.preprocess(tweet) for tweet in conv_tweets_list]
        text_chunks = self.__chunk_conversation(conv_tweets_list)
        chunk_summaries = []

        for chunk in text_chunks:
            chunk_summary = self.model(chunk, min_length=int(0.1 * len(chunk)),
                                       max_length=int(0.5 * len(chunk)))
            chunk_summaries.append(chunk_summary)

        chunks_summaries = [chunk_summary[0]["summary_text"] for chunk_summary in chunk_summaries]
        summary = ''.join(chunks_summaries)
        return summary
