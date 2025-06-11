# src/domain/use_cases/get_all_customers.py
from src.domain.entities.customer import Customer
from src.domain.repositories.customer_repository import CustomerRepository

class GetAllCustomersUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self) -> list[Customer]:
        return await self.customer_repository.get_all()
