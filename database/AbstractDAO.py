import abc
from typing import List, Optional

class AbstractDAO(abc.ABC):
    """Abstract Base Class for Data Access Objects."""

    @abc.abstractmethod
    def insert(self, data: dict) -> None:
        """Insert a new record into the database."""
        pass

    @abc.abstractmethod
    def fetch_all(self) -> List[dict]:
        """Retrieve all records from the database."""
        pass

    @abc.abstractmethod
    def fetch_one(self, record_id: int) -> Optional[dict]:
        """Retrieve a single record by ID."""
        pass

    # @abc.abstractmethod
    # def update(self, record_id: int, data: dict) -> None:
    #     """Update an existing record."""
    #     pass

    # @abc.abstractmethod
    # def delete(self, record_id: int) -> None:
    #     """Delete a record from the database."""
    #     pass
