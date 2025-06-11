# tests/unit/application/services/test_customer_service.py
import pytest
import uuid
from src.domain.entities import Customer
from src.application.services import CustomerService
from src.domain.repositories import CustomerRepository # For typing mock
from unittest.mock import AsyncMock, MagicMock # Added MagicMock

@pytest.fixture
def mock_customer_repo_for_service() -> AsyncMock: # Renamed to avoid conflict if run with domain tests
    # Re-using the domain conftest mock is also an option if structure allows
    mock = AsyncMock(spec=CustomerRepository)
    mock.create = AsyncMock()
    mock.find_by_id = AsyncMock()
    mock.find_by_email = AsyncMock()
    mock.get_all = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_service_create_customer(mock_customer_repo_for_service: AsyncMock):
    service = CustomerService(customer_repository=mock_customer_repo_for_service)
    name, email = "Service Test", "service@example.com"

    # Expected customer that the repository's create method will return
    expected_customer_from_repo = Customer(id=uuid.uuid4(), name=name, email=email)
    mock_customer_repo_for_service.find_by_email.return_value = None # No existing customer with this email
    mock_customer_repo_for_service.create.return_value = expected_customer_from_repo

    created_customer = await service.create_customer(name, email)

    assert created_customer == expected_customer_from_repo
    mock_customer_repo_for_service.find_by_email.assert_called_once_with(email)
    # Check that repo's create method was called with a Customer object
    args, _ = mock_customer_repo_for_service.create.call_args
    assert isinstance(args[0], Customer)
    assert args[0].name == name
    assert args[0].email == email


@pytest.mark.asyncio
async def test_service_create_customer_already_exists_raises_value_error(mock_customer_repo_for_service: AsyncMock):
    service = CustomerService(customer_repository=mock_customer_repo_for_service)
    name, email = "Service Test", "existing@example.com"

    existing_customer = Customer(id=uuid.uuid4(), name="Old Name", email=email)
    mock_customer_repo_for_service.find_by_email.return_value = existing_customer # Simulate email exists

    with pytest.raises(ValueError, match=f"Customer with email {email} already exists."):
        await service.create_customer(name, email)

    mock_customer_repo_for_service.find_by_email.assert_called_once_with(email)
    mock_customer_repo_for_service.create.assert_not_called()


@pytest.mark.asyncio
async def test_service_get_customer_by_id(mock_customer_repo_for_service: AsyncMock):
    service = CustomerService(customer_repository=mock_customer_repo_for_service)
    customer_id = uuid.uuid4()
    expected_customer = Customer(id=customer_id, name="Service Find", email="find@svc.com")
    mock_customer_repo_for_service.find_by_id.return_value = expected_customer

    customer = await service.get_customer_by_id(customer_id)

    assert customer == expected_customer
    mock_customer_repo_for_service.find_by_id.assert_called_once_with(customer_id)

@pytest.mark.asyncio
async def test_service_get_all_customers(mock_customer_repo_for_service: AsyncMock):
    service = CustomerService(customer_repository=mock_customer_repo_for_service)
    customers_list = [Customer(id=uuid.uuid4(), name="Svc C1", email="sc1@example.com")]
    mock_customer_repo_for_service.get_all.return_value = customers_list

    result = await service.get_all_customers()

    assert result == customers_list
    mock_customer_repo_for_service.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_service_update_customer(mock_customer_repo_for_service: AsyncMock):
    service = CustomerService(customer_repository=mock_customer_repo_for_service)
    customer_id = uuid.uuid4()
    original_customer = Customer(id=customer_id, name="Original Svc", email="orig.svc@example.com")
    updated_name = "Updated Svc"

    mock_customer_repo_for_service.find_by_id.return_value = original_customer
    # Assume the updated customer is returned by the repo's update method
    # The repo's update method is expected to return the full customer object after update
    updated_customer_from_repo = Customer(id=customer_id, name=updated_name, email=original_customer.email)
    mock_customer_repo_for_service.update.return_value = updated_customer_from_repo
    # If email is being updated, find_by_email should be mocked too. Here only name is updated.
    mock_customer_repo_for_service.find_by_email.return_value = None

    result = await service.update_customer(customer_id, name=updated_name)

    assert result is not None
    assert result.name == updated_name
    mock_customer_repo_for_service.find_by_id.assert_called_once_with(customer_id)
    # Check that repo's update method was called with a Customer object that has the new name
    args, _ = mock_customer_repo_for_service.update.call_args
    assert isinstance(args[0], Customer)
    assert args[0].name == updated_name
    assert args[0].email == original_customer.email # Email not changed in this test case

@pytest.mark.asyncio
async def test_service_delete_customer(mock_customer_repo_for_service: AsyncMock):
    service = CustomerService(customer_repository=mock_customer_repo_for_service)
    customer_id = uuid.uuid4()

    # find_by_id should return a customer for delete to proceed
    mock_customer_repo_for_service.find_by_id.return_value = Customer(id=customer_id, name="ToDelete", email="del@svc.com")
    mock_customer_repo_for_service.delete.return_value = True # Repo confirms deletion

    result = await service.delete_customer(customer_id)

    assert result is True
    mock_customer_repo_for_service.find_by_id.assert_called_once_with(customer_id)
    mock_customer_repo_for_service.delete.assert_called_once_with(customer_id)
