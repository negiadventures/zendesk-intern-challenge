import requests

from utils import conf


class Request:
    def __init__(self, login_id=None, api_token=None):
        self.login_id = login_id
        self.token = api_token
        if login_id is None:
            self.login_id = conf.login_id
        if api_token is None:
            self.token = conf.api_token

    def get(self, url):
        try:
            response = requests.get(url, auth=(self.login_id, self.token))
            if response.status_code != 200:
                # gives reponse and does not throw error so, we need to check status codes
                if response.status_code in (401, 403, 404, 503):
                    return response.status_code
                return 500
            return response.json()
        except requests.exceptions.RequestException:
            return 500
