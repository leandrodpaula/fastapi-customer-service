# tests/unit/domain/use_cases/conftest.py
import pytest
from unittest.mock import AsyncMock
from src.domain.repositories import CustomerRepository

@pytest.fixture
def mock_customer_repo() -> AsyncMock:
    mock = AsyncMock(spec=CustomerRepository)
    mock.create = AsyncMock()
    mock.find_by_id = AsyncMock()
    mock.find_by_email = AsyncMock()
    mock.get_all = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock
