import config
import json
import logging
import sys

from summarization.bartcnn import BartSummarizationModel
from twitter_api.twitter_api import TweetAPI
from topic_modeling.Bertopic import Bertopic

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Run as python app.py <search_keyword>")
    else:
        config.init()
        api = TweetAPI()
        bertopic = Bertopic()
        summarizer = BartSummarizationModel()

        data = api.get_conversations(search_keyword="Egypt", max_num_conv=100, max_num_pages=50,
                                    max_page_res=100,
                                    parse_func=api.parse_as_samsum_dataset)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

        if config.Config.TOPIC_PER_TWEET:
            conv_topic_probs, topics = bertopic.run_tweet_topic_modeling(data)
        else:
            conv_topic_probs, topics = bertopic.run_con_topic_modeling(data)

        with open('conv_topics.json', 'w') as outfile:
            json.dump(conv_topic_probs, outfile)

        with open('topics.json', 'w') as outfile:
            json.dump(topics, outfile)

        with open('summary.txt', 'w') as summary_file:
            summary = summarizer.run(list(data[0].values())[0])
            summary_file.write(summary)
