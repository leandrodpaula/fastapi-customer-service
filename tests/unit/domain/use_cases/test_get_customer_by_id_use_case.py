# tests/unit/domain/use_cases/test_get_customer_by_id_use_case.py
import pytest
import uuid
from src.domain.entities import Customer
from src.domain.use_cases import GetCustomerByIdUseCase
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_customer_by_id_found(mock_customer_repo: AsyncMock):
    use_case = GetCustomerByIdUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    expected_customer = Customer(id=customer_id, name="Found Customer", email="found@example.com")
    mock_customer_repo.find_by_id.return_value = expected_customer

    customer = await use_case.execute(customer_id)

    assert customer == expected_customer
    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)

@pytest.mark.asyncio
async def test_get_customer_by_id_not_found(mock_customer_repo: AsyncMock):
    use_case = GetCustomerByIdUseCase(customer_repository=mock_customer_repo)
    customer_id = uuid.uuid4()
    mock_customer_repo.find_by_id.return_value = None

    customer = await use_case.execute(customer_id)

    assert customer is None
    mock_customer_repo.find_by_id.assert_called_once_with(customer_id)
