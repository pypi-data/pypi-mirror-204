from abc import ABC, abstractmethod
import logging
import psycopg2
import requests
from typing import TypedDict


class SourceType(TypedDict):
    pass


class DataSource(ABC):
    @abstractmethod
    def get(self):
        pass


class DataSourceAPI(DataSource):
    url: str = ""
    key: str = ""

    def get(self):
        reqURL = f"{self.url}{self.key}"
        resp = requests.get(reqURL)
        result = resp.json()
        logging.info(f"{len(result)} records retrieved")
        return result


class DataSourceDB(DataSource):
    user: str = ""
    password: str = ""
    host: str = ""
    database: str = ""
    query: str = ""
    columns: list[str] = []

    key: str = ""

    def _query(self):
        conn = psycopg2.connect(**{
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "database": self.database,
        })
        cur = conn.cursor()
        cur.execute(self.query)
        return cur.fetchall()

    def get(self):
        results = []
        for row in self._query():
            results.append(dict(zip(self.columns, row)))
        return results
