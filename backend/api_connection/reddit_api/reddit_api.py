import praw
import config as config
from enum import Enum
from summarization.models.samsum import Samsum, MessageThread
from api_connection.social_api import SocialAPI
from praw import models

class HTTPMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

class RedditAPI(SocialAPI):
    base_url = "https://www.reddit.com/"
    oauth_base_url = "https://oauth.reddit.com/"

    def __init__(self):
        self.client = praw.Reddit(
            client_id=config.Config.REDDIT_API_ID,
            client_secret=config.Config.REDDIT_API_SECRET,
            user_agent=config.Config.REDDIT_APP_NAME,
            username=config.Config.REDDIT_USERNAME,
            password=config.Config.REDDIT_PASSWORD
        )

    def get_conversations(self, query: str, limit=5, parse_func=None) -> Samsum:
        result = self.search(query, limit)
        return parse_func(result) if parse_func else self.parse_all_messages(result)
    
    def search(self, query: str, limit=5) -> list[MessageThread]:
        subreddit = self.client.subreddit("all")
        results = subreddit.search(query, limit=limit)

        print(results.params)

        for i in results:
            print(i.title)
            

        return self.parse_results(results)

    def parse_results(self, results: models.ListingGenerator) -> list[MessageThread]:
        message_threads = []
        for submission in results:
            message_thread = MessageThread(submission.title, submission.selftext)
            message_threads.append(message_thread)
        
        return message_threads
    
    def parse_message(self, messages: list, id: str) -> Samsum:
        dialogue = ""
        for message in messages:
            dialogue += f"{message.author}: {message.body}\n"
        
        return Samsum(id, "", dialogue)
                             