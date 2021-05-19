import config
import json
from tweet_api.TweetAPI import TweetAPI

if __name__ == '__main__':
    config.init()
    api = TweetAPI()

    data = api.get_conversations(search_keyword="Liverpool", max_num_conv=1, max_num_pages=10, max_page_res=20,
                                 parse_func=api.parse_as_samsum_dataset)

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
