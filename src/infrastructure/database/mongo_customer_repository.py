# src/infrastructure/database/mongo_customer_repository.py
import uuid
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.domain.entities import Customer
from src.domain.repositories import CustomerRepository
from src.infrastructure.database.config import mongo_config

class MongoCustomerRepository(CustomerRepository):
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_config.MONGO_URI)
        self.db: AsyncIOMotorDatabase = self.client[mongo_config.MONGO_DB_NAME]
        self.collection = self.db["customers"]

    async def create(self, customer: Customer) -> Customer:
        customer_data = {
            "_id": customer.id,
            "name": customer.name,
            "email": customer.email,
        }
        await self.collection.insert_one(customer_data)
        return customer

    async def find_by_id(self, customer_id: uuid.UUID) -> Optional[Customer]:
        customer_data = await self.collection.find_one({"_id": customer_id})
        if customer_data:
            return Customer(
                id=customer_data["_id"],
                name=customer_data["name"],
                email=customer_data["email"],
            )
        return None

    async def find_by_email(self, email: str) -> Optional[Customer]:
        customer_data = await self.collection.find_one({"email": email})
        if customer_data:
            return Customer(
                id=customer_data["_id"],
                name=customer_data["name"],
                email=customer_data["email"],
            )
        return None

    async def get_all(self) -> List[Customer]:
        customers_data = await self.collection.find().to_list(length=None) # Retrieve all documents
        return [
            Customer(
                id=customer_data["_id"],
                name=customer_data["name"],
                email=customer_data["email"],
            )
            for customer_data in customers_data
        ]

    async def update(self, customer: Customer) -> Optional[Customer]:
        result = await self.collection.update_one(
            {"_id": customer.id},
            {"$set": {"name": customer.name, "email": customer.email}}
        )
        if result.modified_count > 0:
            return await self.find_by_id(customer.id)
        # If the document was found but nothing was changed, we can return the original customer
        # or if the update was to the same values.
        # For simplicity, if modified_count is 0 but matched_count is 1, it implies no actual change.
        # We still fetch to ensure consistency, or one might argue to return the input customer directly.
        elif result.matched_count > 0:
             return await self.find_by_id(customer.id)
        return None


    async def delete(self, customer_id: uuid.UUID) -> bool:
        result = await self.collection.delete_one({"_id": customer_id})
        return result.deleted_count > 0
