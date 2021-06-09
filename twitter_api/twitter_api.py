import twarc
import twitter_api.fields as fields
import time
import logging
import config as config


class TweetAPI:

    def __init__(self):
        self.T = twarc.Twarc2(consumer_key=config.Config.CONSUMER_KEY, consumer_secret=config.Config.CONSUMER_SECRET)
        logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
        :: %(message)s', level=logging.INFO)
        self.log = logging.getLogger("TweetAPI")

    def __search(self, url, query, max_results=100, sleep_between=0):
        """
        Search for tweets by a query
        :param url: (str): url of the tweet search API.
        :param query: (str): The query string to be passed directly to the Twitter API.
        :param max_results: (int): The maximum number of results per request. Default max is 100.
        :param sleep_between: Time to sleep between two requests.
        :return: generator[dict]: a generator, dict for each paginated response.

        """
        params = {"tweet.fields": ",".join(fields.TWEET_FIELDS), "user.fields": ",".join(fields.USER_FIELDS),
                  "expansions": "author_id", "max_results": max_results, "query": query}
        made_call = time.monotonic()  # Time of the first call to tweet search API

        for response in self.T.get_paginated(url, params=params):
            # can return without 'data' if there are no results
            if 'data' in response:
                yield response

                # Calculate the amount of time to sleep, accounting for any
                # processing time used by the rest of the application.
                # This is to satisfy the 1 request / 1 second rate limit
                # on the search/all endpoint.
                time.sleep(
                    max(0, sleep_between - (time.monotonic() - made_call))
                )
                made_call = time.monotonic()
            else:
                self.log.info('no more results for search')

    def __search_recent(self, query, max_results=100):
        """
        Search Twitter for the given query in the last seven days
        :param query: (str): The query string to be passed directly to the Twitter API.
        :param max_results: (int): The maximum number of results per request. Default max is 100.
        :return: generator[dict]: a generator, dict for each paginated response.
        """
        url = "https://api.twitter.com/2/tweets/search/recent"
        return self.__search(url, query, max_results)

    def __collect_conversations_id(self, query, max_conv=10, max_pages=10, max_page_results=100):
        """
        Collect conversation ids from tweets returned from search API. A conversation id will be collected
        if it has at least one reply to the original tweet. The conversation id is the id the first (initiator) tweet.
        :param query: (str): The query string to be passed directly to the Twitter API.
        :param max_conv: (int): Maximum number of unique valid conversation IDs.
        :param max_pages: (int): Maximum number of pages returned from API.
        :param max_page_results: (int): The maximum number of results per request. Default max is 100.
        :return: set: a set of conversation ids.
        """
        conversations = set()
        page = 0
        for response_page in self.__search_recent(query, max_results=max_page_results):
            tweets = response_page["data"]
            page += 1

            for t in tweets:
                if t["public_metrics"]["reply_count"] > 0:  # Tweet has replies
                    conversations.add(t["conversation_id"])
                elif "referenced_tweets" in t:  # Tweet references another tweet
                    for ref in t["referenced_tweets"]:
                        if ref["type"] == "replied_to":  # Tweet is a reply to another tweet
                            conversations.add(t["conversation_id"])

            if (len(conversations) >= max_conv) or page > max_pages:
                break

        return conversations

    def __get_tweet(self, tweet_id):
        """
        Get a tweet object of a specific tweet id.
        :param tweet_id: (str): id of target tweet.
        :return: dict: the tweet object.
        """
        url = "https://api.twitter.com/2/tweets/" + tweet_id
        params = {"tweet.fields": ",".join(fields.TWEET_FIELDS), "user.fields": ",".join(fields.USER_FIELDS),
                  "expansions": "author_id"}

        resp = self.T.get(url, params=params)
        page = resp.json()

        # add username of the tweet's author to the data dict to return only the data dict.
        page["data"]["username"] = page["includes"]["users"][0]["username"]
        return page["data"]

    def __parse_response(self, response):
        """
        Add the tweet author username to the tweet data dict.
        :param response: (dict): the response holding the tweets of a specific conversation
        :return: generator[dict]: a generator, dict for each paginated response.
        """
        # map from user Id to username
        id_username_dict = {u["id"]: u["username"] for u in response["includes"]["users"]}
        tweets = response["data"]
        for t in tweets:  # for each tweet add its username of its author
            t["username"] = id_username_dict[t["author_id"]]

        return tweets

    def parse_as_conv_hierarchy(self, conv_id, tweets):
        """
        Reconstruct conversation threads based on the creation date and reply-to field.
        :param conv_id: (str): id of the conversation. The conversation id is the id the first (initiator) tweet.
        :param tweets: (generator[dict]): a generator, dict for each tweet.
        :return: dict: the conversation.
        """

        id_tweet_dict = {t["id"]: t for t in tweets}  # A map from tweet id to tweet object

        # nest tweets according to the conversation threads
        for t in tweets:
            if t["id"] == conv_id:  # root tweet has not parents.
                continue

            parent_tweet_id = None
            for ref in t["referenced_tweets"]:  # get parent tweet
                if ref["type"] == "replied_to":
                    parent_tweet_id = ref["id"]
                    break

            parent_tweet_obj = id_tweet_dict[parent_tweet_id]
            if "replies" not in parent_tweet_obj:
                parent_tweet_obj["replies"] = []

            # add this tweet in the replies list of its parent tweeet.
            parent_tweet_obj["replies"].append(id_tweet_dict[t["id"]])

        # for each thread sort by created date
        for t in tweets:
            if "replies" in t:
                t["replies"].sort(key=lambda x: x["created_at"])

        return {conv_id: id_tweet_dict[conv_id]}  # return original tweet that started the conversation

    def parse_as_samsum_dataset(self, conv_id, tweets):
        """
        Parse the conversation as in the SAMSum Dataset where each tweet is a line and preceeded by author name.
        E.g.,
        ""
            user1: Hello
            user2: hey
            user1: Goodbye
            user2: Bye
        ""

        :param tweets: (generator[dict]): a generator, dict for each tweet.
        :return: list: list of tweets constructing the conversation.
        """
        # sort tweets by creation date
        tweets.sort(key=lambda x: x["created_at"])
        res = []
        for t in tweets:
            res.append("{}:{}\n".format(t["username"], t["text"]))

        return {conv_id: res}

    def __get_conversation(self, conv_id, max_results=100, parse_func=parse_as_samsum_dataset):
        """
        Get tweets of a specific conversation.
        :param conv_id: (str): id of the target conversation
        :param max_results: (int): The maximum number of results per request. Default max is 100.
        :param parse_func: (func): parse the conversation and return a dict {conv_id: parsed_obj}.
        :return: dict: {conv_id: parsed object}.
        """
        # query for search API to get tweets corresponding to specific conversation id
        query = "conversation_id:" + conv_id

        tweets = [self.__get_tweet(conv_id)]  # get first (initiator) tweet
        for response_page in self.__search_recent(query, max_results=max_results):  # get all tweets in the conversation
            tweets += self.__parse_response(response_page)
            if len(response_page["data"]) < max_results:  # all tweets are fetched
                break

        return parse_func(conv_id, tweets)

    def get_conversations(self, search_keyword, max_num_conv=10, max_num_pages=10,
                          max_page_res=100, parse_func=parse_as_samsum_dataset):
        """
        Fetch all conversation of a specific search keyword
        :param search_keyword: (str): The query string to be passed directly to the Twitter API.
        :param max_num_conv: (int): Maximum number of unique valid conversation IDs.
        :param max_num_pages: (int): Maximum number of pages returned from API.
        :param max_page_res: (int): The maximum number of results per request. Default max is 100.
        :param parse_func: (func): parse the conversation and return a dict {conv_id: parsed_obj}. We have two parse
        functions: 1- parse_as_samsum_dataset(): parse conversation as in the SAMSum dataset.
                   2- parse_as_conv_hierarchy(): parse conversation as a hierarchy to capture the conversation threads.
        :return: list[dict]: list of all conversations dict. E.g., [{conv_id_1:parsed_obj_1}, {conv_id_2:parsed_obj_2}]
        """

        conv_list = self.__collect_conversations_id(search_keyword, max_conv=max_num_conv, max_pages=max_num_pages,
                                                    max_page_results=max_page_res)

        res = []
        for conv_id in conv_list:  # fetch tweets of each conversation
            res.append(self.__get_conversation(conv_id=conv_id, max_results=max_page_res, parse_func=parse_func))

        return res
