import requests
from .environment import Environment
from typing import List


class Db(object):
    def __init__(self, db_name: str, env: Environment):
        self.db = db_name
        self.env = env

    def insert(self, data: dict) -> bool | None:
        url = f"{self.env.LOG_API_BASE_URL}/remote-cache/db"
        headers = {
            "Authorization": f"Bearer {self.env.LOG_API_TOKEN}"
        }
        body = {
            "meta":
            {
                "id_field": "id",
                "db_name": self.db
            },
            "data": data
        }
        response = requests.post(url, headers=headers, data=body)
        print(f"response: {response.status_code}")
        if response.status_code == 200:
            return True
        else:
            return None

    def find(self, filters: dict) -> List[dict] | None:
        url = f"{self.env.LOG_API_BASE_URL}/remote-cache/db"
        headers = {
            "Authorization": f"Bearer {self.env.LOG_API_TOKEN}"
        }
        body = {
            "db_name": self.db,
            "filters": filters
        }
        response = requests.put(url, headers=headers, data=body)
        if response.status_code == 200:
            return response.json()
        else:
            return None
