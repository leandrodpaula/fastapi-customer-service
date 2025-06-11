# src/domain/use_cases/create_customer.py
from src.domain.entities.customer import Customer
from src.domain.repositories.customer_repository import CustomerRepository

class CreateCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self, name: str, email: str) -> Customer:
        # Basic validation
        if not name or not email:
            raise ValueError("Name and email cannot be empty")
        # More complex validation (e.g., email format) could be added here

        existing_customer = await self.customer_repository.find_by_email(email)
        if existing_customer:
            raise ValueError(f"Customer with email {email} already exists.")

        customer = Customer(name=name, email=email)
        return await self.customer_repository.create(customer)
