# tests/unit/domain/use_cases/test_update_customer_use_case.py
import pytest
import uuid
from src.domain.entities import Customer
from src.domain.use_cases import UpdateCustomerUseCase
from unittest.mock import AsyncMock, call # Import call

@pytest.mark.asyncio
async def test_update_customer_success(mock_customer_repo: AsyncMock):
    use_case = UpdateCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    original_customer = Customer(id=customer_id, name="Original Name", email="original@example.com")

    mock_customer_repo.find_by_id.return_value = original_customer
    # Mock find_by_email to simulate new email is not taken by another user
    mock_customer_repo.find_by_email.return_value = None

    updated_name = "Updated Name"
    updated_email = "updated@example.com"

    # The update method in the repo should return the updated customer
    async def mock_update(customer: Customer):
        return customer # Assume it returns the object passed to it after "persisting"

    mock_customer_repo.update.side_effect = mock_update

    updated_customer = await use_case.execute(customer_id, name=updated_name, email=updated_email)

    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)
    # Check find_by_email was called for the new email
    mock_customer_repo.find_by_email.assert_called_once_with(updated_email)

    # Assert that update was called with a customer object having updated fields
    args, _ = mock_customer_repo.update.call_args
    assert isinstance(args[0], Customer)
    assert args[0].id == customer_id
    assert args[0].name == updated_name
    assert args[0].email == updated_email

    assert updated_customer is not None
    assert updated_customer.name == updated_name
    assert updated_customer.email == updated_email

@pytest.mark.asyncio
async def test_update_customer_not_found(mock_customer_repo: AsyncMock):
    use_case = UpdateCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    mock_customer_repo.find_by_id.return_value = None

    result = await use_case.execute(customer_id, name="Any Name")

    assert result is None
    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)
    mock_customer_repo.update.assert_not_called()

@pytest.mark.asyncio
async def test_update_customer_email_already_exists_for_another_customer(mock_customer_repo: AsyncMock):
    use_case = UpdateCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id_to_update = uuid.uuid4()
    another_customer_id = uuid.uuid4()

    customer_to_update = Customer(id=customer_id_to_update, name="User One", email="user1@example.com")
    customer_with_target_email = Customer(id=another_customer_id, name="User Two", email="user2_new_email@example.com")

    mock_customer_repo.find_by_id.return_value = customer_to_update
    # Simulate that the new email 'user2_new_email@example.com' is already taken by 'customer_with_target_email'
    mock_customer_repo.find_by_email.return_value = customer_with_target_email

    with pytest.raises(ValueError, match=f"Another customer with email {customer_with_target_email.email} already exists."):
        await use_case.execute(customer_id_to_update, email=customer_with_target_email.email)

    mock_customer_repo.find_by_id.assert_called_once_with(customer_id_to_update)
    mock_customer_repo.find_by_email.assert_called_once_with(customer_with_target_email.email)
    mock_customer_repo.update.assert_not_called()

@pytest.mark.asyncio
async def test_update_customer_email_not_changed_or_changed_to_own(mock_customer_repo: AsyncMock):
    use_case = UpdateCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    original_email = "original@example.com"
    customer = Customer(id=customer_id, name="Original Name", email=original_email)

    mock_customer_repo.find_by_id.return_value = customer
    # Simulate find_by_email returns the customer itself if email is unchanged or set to its own current email
    mock_customer_repo.find_by_email.return_value = customer

    async def mock_update(cust: Customer): return cust
    mock_customer_repo.update.side_effect = mock_update

    # Test updating only name
    updated_customer_name_only = await use_case.execute(customer_id, name="New Name")
    assert updated_customer_name_only.name == "New Name"
    assert updated_customer_name_only.email == original_email
    # find_by_email should not be called if email is None in input
    assert mock_customer_repo.find_by_email.call_count == 0

    # Reset find_by_email mock for next call if needed or ensure it behaves correctly for multiple calls
    mock_customer_repo.find_by_email.reset_mock()
    mock_customer_repo.find_by_email.return_value = customer # Re-assign after reset

    # Test updating email to its current value
    updated_customer_same_email = await use_case.execute(customer_id, email=original_email)
    assert updated_customer_same_email.email == original_email
    # find_by_email should be called
    mock_customer_repo.find_by_email.assert_called_once_with(original_email)


@pytest.mark.asyncio
async def test_update_customer_empty_email_string(mock_customer_repo: AsyncMock):
    use_case = UpdateCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    original_customer = Customer(id=customer_id, name="Original Name", email="original@example.com")
    mock_customer_repo.find_by_id.return_value = original_customer

    with pytest.raises(ValueError, match="Email cannot be empty if provided for update."):
        await use_case.execute(customer_id, email="")

    mock_customer_repo.update.assert_not_called()
