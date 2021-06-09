import config
import json
from tweet_api.TweetAPI import TweetAPI

if __name__ == '__main__':
    config.init()
    api = TweetAPI()

    data = api.get_conversations(search_keyword="istanbulunfethi", max_num_conv=10000, max_num_pages=50,
                                 max_page_res=100,
                                 parse_func=api.parse_as_samsum_dataset)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
