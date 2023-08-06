import os
import json
import requests


class Environment(object):
    """
    This class is used to get the environment variables
        -LOG_API_TOKEN
        -LOG_API_BASE_URL
        -API_BASE_URL
        -REMOTE_TOKEN

    """

    def __init__(self):
        self.LOG_API_TOKEN = os.environ['LOG_API_TOKEN']
        self.LOG_API_BASE_URL = os.environ['LOG_API_BASE_URL']
        self.API_BASE_URL = os.environ['API_BASE_URL']
        self.REMOTE_TOKEN = os.environ['REMOTE_TOKEN']

    def env(self, key: str, bucket: str = "main"):
        """
        This function is used to get the environment variables
        """
        url = f"{self.LOG_API_BASE_URL}/logger/env/"
        headers = {
            "Authorization": f"Bearer {self.LOG_API_TOKEN}"
        }
        body = {
            "key": key,
            "bucket": bucket
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            data = response.text
            return data
        else:
            return None

    def set_env(self, key: str, value: str, bucket: str = "main"):
        """
        This function is used to set the environment variables
        """
        url = f"{self.LOG_API_BASE_URL}/logger/env/"
        headers = {
            "Authorization": f"Bearer {self.LOG_API_TOKEN}"
        }
        body = {
            "key": key,
            "bucket": bucket,
            "value": value,
        }
        response = requests.put(url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def get_envirement():
        return Environment()
