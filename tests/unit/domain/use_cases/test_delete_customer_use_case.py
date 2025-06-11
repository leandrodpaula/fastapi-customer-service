# tests/unit/domain/use_cases/test_delete_customer_use_case.py
import pytest
import uuid
from src.domain.entities import Customer
from src.domain.use_cases import DeleteCustomerUseCase
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_delete_customer_success(mock_customer_repo: AsyncMock):
    use_case = DeleteCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    # Need find_by_id to return a customer for deletion to proceed
    mock_customer_repo.find_by_id.return_value = Customer(id=customer_id, name="Test", email="test@del.com")
    mock_customer_repo.delete.return_value = True # Simulate successful deletion

    result = await use_case.execute(customer_id)

    assert result is True
    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)
    mock_customer_repo.delete.assert_called_once_with(customer_id)

@pytest.mark.asyncio
async def test_delete_customer_not_found(mock_customer_repo: AsyncMock):
    use_case = DeleteCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    mock_customer_repo.find_by_id.return_value = None # Simulate customer not found

    result = await use_case.execute(customer_id)

    assert result is False # Use case returns False if customer not found
    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)
    mock_customer_repo.delete.assert_not_called() # Delete should not be called if customer not found

@pytest.mark.asyncio
async def test_delete_customer_repo_fails_deletion(mock_customer_repo: AsyncMock):
    use_case = DeleteCustomerUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    mock_customer_repo.find_by_id.return_value = Customer(id=customer_id, name="Test", email="test@del.com")
    mock_customer_repo.delete.return_value = False # Simulate repository failed to delete

    result = await use_case.execute(customer_id)

    assert result is False
    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)
    mock_customer_repo.delete.assert_called_once_with(customer_id)
