"""
This module abstracts the Database layer with a Repository pattern.
"""
import abc
from typing import TypeVar

from market.domain.models import BaseEntity, StockInformation

T = TypeVar("T", bound=BaseEntity)


class ReadOnlyRepository(abc.ABC):
    """
    Abstract base class for read-only repository implementations.
    """

    @abc.abstractmethod
    def find_all(self, *args, **kwargs) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, *args, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError


class WriteOnlyRepository(abc.ABC):
    """
    Abstract base class for write-only repository implementations.
    """

    @abc.abstractmethod
    def save(self, entity: T, *args, **kwargs) -> None:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: T, *args, **kwargs) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        raise NotImplementedError


class AsyncReadOnlyRepository(abc.ABC):
    """
    Abstract base class for asynchronous read-only repository implementations.
    """

    @abc.abstractmethod
    async def find_all(self, *args, **kwargs) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        raise NotImplementedError

    @abc.abstractmethod
    async def find_by(self, *args, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError


class AsyncWriteOnlyRepository(abc.ABC):
    """
    Abstract base class for asynchronous write-only repository implementations.
    """

    @abc.abstractmethod
    async def save(self, entity: T, *args, **kwargs) -> T:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, entity: T, *args, **kwargs) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        raise NotImplementedError


class AsyncRepository(AsyncWriteOnlyRepository, AsyncReadOnlyRepository, abc.ABC):
    """
    Abstract base class for asynchronous repository implementations.
    """
    pass


class StockMarketRepository(AsyncReadOnlyRepository, abc.ABC):
    """
    Abstract base class for StockMarketRepository implementations.
    """

    async def get_daily_time_series(self, symbol: str, *args, **kwargs) -> list[StockInformation]:
        """
        Gets time series data from the repository.

        Args:
            symbol (str): The stock symbol to get time series data for.

        Returns:
            list[StockInformation] : A list of time series stock market information.

        """
        raise NotImplementedError
