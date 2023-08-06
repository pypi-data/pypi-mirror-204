from abc import ABC, abstractmethod
import logging
import psycopg2
import requests
from typing import TypedDict


class SourceType(TypedDict):
    ...


def records_count(method):
    """
    Decorator to count the number of records that are returned by the source.
    """
    def internal(cls, *args, **kwargs):
        result = method(cls, *args, **kwargs)
        logging.info(
            f"{len(result)} records retrieved from {cls.__class__.__name__}"
        )
        return result
    return internal


class DataSource(ABC):
    """
    Abstract method to ensure the get() method is defined for each child
    data source classes.
    """

    @abstractmethod
    def get(self):
        ...


class DataSourceAPI(DataSource):

    @property
    @abstractmethod
    def url(self) -> str:
        ...

    @records_count
    def get(self):
        resp = requests.get(self.url)
        result = resp.json()
        return result


class DataSourcePostgres(DataSource):

    @property
    @abstractmethod
    def user(self) -> str:
        ...

    @property
    @abstractmethod
    def password(self) -> str:
        ...

    @property
    @abstractmethod
    def host(self) -> str:
        ...

    @property
    @abstractmethod
    def database(self) -> str:
        ...

    @property
    @abstractmethod
    def query(self) -> str:
        ...

    @property
    @abstractmethod
    def columns(self) -> list[str]:
        """
        Sets the database query dataset column names. Names are applied
        sequentially.
        """

    def _query(self) -> list[tuple]:
        """
        Query the PostgreSQL database using the given database attributes.
        """
        conn = psycopg2.connect(**{
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "database": self.database,
        })
        cur = conn.cursor()
        cur.execute(self.query)
        return cur.fetchall()

    @records_count
    def get(self) -> list[dict]:
        """
        Query the PostgreSQL database, and convert the list[tuple] type into
        list[dict] type, using the given columns attribute.
        """
        results = []
        for row in self._query():
            results.append(dict(zip(self.columns, row)))
        return results
