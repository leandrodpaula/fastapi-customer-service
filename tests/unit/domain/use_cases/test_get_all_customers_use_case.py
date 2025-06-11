# tests/unit/domain/use_cases/test_get_all_customers_use_case.py
import pytest
import uuid
from src.domain.entities import Customer
from src.domain.use_cases import GetAllCustomersUseCase
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_all_customers_success(mock_customer_repo: AsyncMock):
    use_case = GetAllCustomersUseCase(customer_repository=mock_customer_repo)
    customers_list = [
        Customer(id=uuid.uuid4(), name="Customer 1", email="c1@example.com"),
        Customer(id=uuid.uuid4(), name="Customer 2", email="c2@example.com"),
    ]
    mock_customer_repo.get_all.return_value = customers_list

    result = await use_case.execute()

    assert result == customers_list
    mock_customer_repo.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_customers_empty(mock_customer_repo: AsyncMock):
    use_case = GetAllCustomersUseCase(customer_repository=mock_customer_repo)
    mock_customer_repo.get_all.return_value = []

    result = await use_case.execute()

    assert result == []
    mock_customer_repo.get_all.assert_called_once()
