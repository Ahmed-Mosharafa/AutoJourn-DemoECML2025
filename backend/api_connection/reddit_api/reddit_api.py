import praw
import config as config
from enum import Enum
from summarization.models.samsum import Samsum, MessageThread
from api_connection.social_api import SocialAPI
from praw import models


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
        return parse_func(result) if parse_func else self.parse_all_messages_json(result)

    def search(self, query: str, limit=5) -> list[MessageThread]:
        subreddit = self.client.subreddit("all")
        results = subreddit.search(query, limit=limit)

        return self.parse_results(results)

    def get_message_threads(self, results) -> list[MessageThread]:
        message_threads = []
        for submission in results:
            comments = self.extract_comments(submission)

            message_thread = MessageThread(
                submission.author, submission.title)
            message_threads.append(message_thread)

        return message_threads

    def parse_results(self, results) -> list[MessageThread]:
        message_threads = []
        for submission in results:
            message_thread = MessageThread(
                submission.author, submission.title)
            message_threads.append(message_thread)

        return message_threads

    def extract_comments(self, submission: models.Submission) -> MessageThread:
        submission.comments.replace_more(limit=None)
        return MessageThread(submission.author, submission.comments.list())

    def parse_message_json(self, messages: list, id: str) -> dict:
        return self.parse_message(messages, id).to_json()

    def parse_message(self, messages: list, id: str) -> Samsum:
        dialogue = ""
        for message in messages:
            dialogue += f"{message.author}: {message.body}\n"

        return Samsum(id, "", dialogue)
