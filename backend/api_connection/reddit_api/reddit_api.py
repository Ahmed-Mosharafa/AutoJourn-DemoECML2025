import os
import requests
import config as config
from enum import Enum

class HTTPMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

class RedditAPI:
    base_url = "https://www.reddit.com/"
    oauth_base_url = "https://oauth.reddit.com"

    def __init__(self):
        self.reddit_username = config.Config.REDDIT_USERNAME
        self.reddit_password = config.Config.REDDIT_PASSWORD
        self.reddit_api_id = config.Config.REDDIT_API_ID
        self.reddit_api_secret = config.Config.REDDIT_API_SECRET
        self.reddit_app_name = config.Config.REDDIT_APP_NAME
        self.authentication_token = self.login_reddit()

    def login_reddit(self):
        data = {'grant_type': 'password', 'username': self.reddit_username, 'password': self.reddit_password}
        auth = requests.auth.HTTPBasicAuth(self.reddit_api_id, self.reddit_api_secret)
        headers = {'User-Agent': '{} by {}'.format(self.reddit_app_name, self.reddit_username)}

        r = RedditAPI.make_request(self.base_url + 'api/v1/access_token',
                    HTTPMethod.POST,
                    auth=auth,
                    headers=headers,
                    body=data)
        
        return r.json()

    def make_oath_request(self, request_endpoint: str, method: HTTPMethod):
        headers = {'Authorization': self.authentication_token, 'User-Agent': '{} by {}'.format(self.reddit_app_name, self.reddit_username)}
        return RedditAPI.make_request(request_endpoint, method, headers=headers)
        
    
    @staticmethod
    def make_request(request_endpoint: str, method: HTTPMethod, auth = None, headers = None, body = None, params = None):
        if method == HTTPMethod.GET:
            return requests.get(request_endpoint, headers=headers, auth=auth, params=params)
        elif method == HTTPMethod.POST:
            return requests.post(request_endpoint, headers=headers, auth=auth, body=body, params=params)
        elif method == HTTPMethod.PUT:
            return requests.put(request_endpoint, headers=headers, auth=auth, body=body, params=params)
        elif method == HTTPMethod.DELETE:
            return requests.delete(request_endpoint, headers=headers, auth=auth, params=params)
    
    def search(self, query: str, limit=5):
        params = {'q': query, 'limit': limit}
        return self.make_oath_request(request_endpoint=self.base_url + "/subreddits/search", method=HTTPMethod.GET, params=params)
                     