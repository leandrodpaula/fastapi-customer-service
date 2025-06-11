# src/domain/use_cases/update_customer.py
import uuid
from typing import Optional
from src.domain.entities.customer import Customer
from src.domain.repositories.customer_repository import CustomerRepository

class UpdateCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def execute(self, customer_id: uuid.UUID, name: Optional[str] = None, email: Optional[str] = None) -> Optional[Customer]:
        customer = await self.customer_repository.find_by_id(customer_id)
        if not customer:
            return None

        if name is not None:
            customer.name = name
        if email is not None:
            # Basic validation
            if not email: # This will catch email == ""
                raise ValueError("Email cannot be empty if provided for update.")
            # Check if the new email already exists for another customer
            existing_customer_with_new_email = await self.customer_repository.find_by_email(email)
            if existing_customer_with_new_email and existing_customer_with_new_email.id != customer_id:
                raise ValueError(f"Another customer with email {email} already exists.")
            customer.email = email

        return await self.customer_repository.update(customer)
