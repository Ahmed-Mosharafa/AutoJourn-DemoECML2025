import config
import json
from twitter_api.twitter_api import TweetAPI
from topic_modeling.Bertopic import Bertopic

if __name__ == '__main__':
    config.init()
    api = TweetAPI()
    bertopic = Bertopic()

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


