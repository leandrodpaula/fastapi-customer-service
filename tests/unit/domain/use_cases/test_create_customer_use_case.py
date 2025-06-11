# tests/unit/domain/use_cases/test_create_customer_use_case.py
import pytest
import uuid
from src.domain.entities import Customer
from src.domain.use_cases import CreateCustomerUseCase
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_customer_success(mock_customer_repo: AsyncMock):
    use_case = CreateCustomerUseCase(customer_repository=mock_customer_repo)
    mock_customer_repo.find_by_email.return_value = None

    # Configure the mock 'create' method to return a Customer instance
    # It should return the customer passed to it, or a new one with an ID
    async def mock_create_customer(customer: Customer):
        # If the customer doesn't have an ID, assign one (though dataclass default_factory handles this)
        if not customer.id:
            customer.id = uuid.uuid4()
        return customer
    mock_customer_repo.create.side_effect = mock_create_customer

    name, email = "New Customer", "new@example.com"
    created_customer = await use_case.execute(name, email)

    assert created_customer is not None
    assert created_customer.name == name
    assert created_customer.email == email
    assert isinstance(created_customer.id, uuid.UUID)
    mock_customer_repo.find_by_email.assert_called_once_with(email)
    # Check that create was called with a Customer instance, matching name and email
    args, _ = mock_customer_repo.create.call_args
    assert isinstance(args[0], Customer)
    assert args[0].name == name
    assert args[0].email == email


@pytest.mark.asyncio
async def test_create_customer_already_exists(mock_customer_repo: AsyncMock):
    use_case = CreateCustomerUseCase(customer_repository=mock_customer_repo)
    existing_customer = Customer(id=uuid.uuid4(), name="Existing User", email="exists@example.com")
    mock_customer_repo.find_by_email.return_value = existing_customer

    with pytest.raises(ValueError, match="Customer with email exists@example.com already exists."):
        await use_case.execute("Any Name", "exists@example.com")

    mock_customer_repo.find_by_email.assert_called_once_with("exists@example.com")
    mock_customer_repo.create.assert_not_called()

@pytest.mark.asyncio
@pytest.mark.parametrize("name, email", [("", "test@example.com"), ("Test", "")])
async def test_create_customer_empty_fields(mock_customer_repo: AsyncMock, name: str, email: str):
    use_case = CreateCustomerUseCase(customer_repository=mock_customer_repo)
    with pytest.raises(ValueError, match="Name and email cannot be empty"):
        await use_case.execute(name, email)
    mock_customer_repo.create.assert_not_called()
