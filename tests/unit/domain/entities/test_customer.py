# tests/unit/domain/entities/test_customer.py
import uuid
from src.domain.entities import Customer

def test_customer_creation_default_id():
    customer = Customer(name="Test Name", email="test@example.com")
    assert customer.name == "Test Name"
    assert customer.email == "test@example.com"
    assert isinstance(customer.id, uuid.UUID)

def test_customer_creation_with_id():
    custom_id = uuid.uuid4()
    customer = Customer(id=custom_id, name="Test Name", email="test@example.com")
    assert customer.id == custom_id
    assert customer.name == "Test Name"
    assert customer.email == "test@example.com"
