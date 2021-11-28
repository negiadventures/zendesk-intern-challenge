import requests

from utils import constants


class Request:
    def __init__(self):
        self.login_id = constants.login_id
        self.token = constants.api_token

    def get(self, url):
        try:
            response = requests.get(url, auth=(self.login_id, self.token))
            if response.status_code != 200:
                if response.status_code == 401 or response.status_code == 403:
                    return response.status_code
                elif response.status_code == 404:
                    return response.status_code
                elif response.status_code == 503:
                    return response.status_code
                return 500
            return response.json()
        except requests.exceptions.RequestException as e:
            return 500
        except ConnectionError:
            return 500
        except Exception:
            return
