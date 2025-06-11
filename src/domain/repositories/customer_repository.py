# src/domain/repositories/customer_repository.py
from abc import ABC, abstractmethod
from typing import Optional
import uuid
from src.domain.entities.customer import Customer

class CustomerRepository(ABC):
    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    async def find_by_id(self, customer_id: uuid.UUID) -> Optional[Customer]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Customer]:
        pass

    @abstractmethod
    async def update(self, customer: Customer) -> Optional[Customer]:
        pass

    @abstractmethod
    async def delete(self, customer_id: uuid.UUID) -> bool:
        pass
