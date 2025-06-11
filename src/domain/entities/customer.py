# src/domain/entities/customer.py
import uuid
from dataclasses import dataclass, field

@dataclass
class Customer:
    name: str
    email: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
