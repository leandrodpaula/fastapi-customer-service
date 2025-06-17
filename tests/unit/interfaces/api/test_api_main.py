# tests/unit/interfaces/api/test_api_main.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch # Import patch
import uuid

# We need to setup the app with mocked dependencies for testing the API layer in isolation.
# This is a common pattern for testing FastAPI endpoints.

# Mock the CustomerService dependency
@pytest.fixture
def mock_customer_service() -> AsyncMock:
    service_mock = AsyncMock()
    service_mock.create_customer = AsyncMock()
    # Add other methods if testing other endpoints that use them
    return service_mock

@pytest.fixture
def client(mock_customer_service: AsyncMock):
    # This import must be here, inside the fixture,
    # to allow dependencies to be patched before the app is imported.
    from src.interfaces.api.main import app, get_customer_service

    # Override the dependency with our mock
    app.dependency_overrides[get_customer_service] = lambda: mock_customer_service

    with TestClient(app) as test_client:
        yield test_client

    # Clean up overrides after tests
    app.dependency_overrides = {}


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Customer API. Visit /graphql for GraphQL or /docs for REST API documentation."}

@pytest.mark.asyncio # Test itself is not async, but what it calls is
def test_create_customer_rest_success(client: TestClient, mock_customer_service: AsyncMock):
    customer_id = uuid.uuid4()
    request_data = {"name": "Test REST User", "email": "rest_user@example.com"}

    # Configure the mock service's create_customer method
    # It should return an object that can be serialized into CustomerResponse
    # For simplicity, let's assume it returns a dictionary-like object or a simple class instance
    # that matches the fields of DomainCustomer, which then gets converted.
    # Or, more accurately, it returns a DomainCustomer instance.
    from src.domain.entities import Customer as DomainCustomer
    mock_customer_service.create_customer.return_value = DomainCustomer(
        id=customer_id,
        name=request_data["name"],
        email=request_data["email"]
    )

    response = client.post("/customers/", json=request_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == request_data["name"]
    assert response_data["email"] == request_data["email"]
    assert "id" in response_data
    assert response_data["id"] == str(customer_id) # UUIDs are returned as strings in JSON

    # Verify that the service method was called correctly
    mock_customer_service.create_customer.assert_called_once_with(
        name=request_data["name"],
        email=request_data["email"]
    )

@pytest.mark.asyncio
def test_create_customer_rest_already_exists(client: TestClient, mock_customer_service: AsyncMock):
    request_data = {"name": "Existing User", "email": "existing@example.com"}

    # Configure mock service to raise ValueError (simulating user already exists)
    mock_customer_service.create_customer.side_effect = ValueError("Customer with email existing@example.com already exists.")

    response = client.post("/customers/", json=request_data)

    assert response.status_code == 400 # Bad Request
    assert "Customer with email existing@example.com already exists." in response.json()["detail"]

    mock_customer_service.create_customer.assert_called_once_with(
        name=request_data["name"],
        email=request_data["email"]
    )

@pytest.mark.asyncio
def test_create_customer_rest_invalid_email(client: TestClient, mock_customer_service: AsyncMock):
    request_data = {"name": "Invalid Email User", "email": "not-an-email"}
    # Pydantic validation happens before our endpoint handler is called,
    # so the service mock won't even be hit for this type of validation error.

    response = client.post("/customers/", json=request_data)

    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation errors
    # Check for some detail from Pydantic's error response
    assert "value is not a valid email address" in response.text # Check raw text for Pydantic error structure

    mock_customer_service.create_customer.assert_not_called()


@pytest.mark.asyncio
def test_create_customer_rest_missing_name(client: TestClient, mock_customer_service: AsyncMock):
    request_data = {"email": "noname@example.com"} # Missing 'name' field

    response = client.post("/customers/", json=request_data)

    assert response.status_code == 422 # Unprocessable Entity
    assert "field required" in response.text # Pydantic error

    mock_customer_service.create_customer.assert_not_called()

@pytest.mark.asyncio
def test_create_customer_rest_internal_server_error(client: TestClient, mock_customer_service: AsyncMock):
    request_data = {"name": "Error User", "email": "error@example.com"}

    # Configure mock service to raise a generic Exception
    mock_customer_service.create_customer.side_effect = Exception("Some unexpected internal error.")

    response = client.post("/customers/", json=request_data)

    assert response.status_code == 500 # Internal Server Error
    assert response.json()["detail"] == "An unexpected error occurred."

    mock_customer_service.create_customer.assert_called_once_with(
        name=request_data["name"],
        email=request_data["email"]
    )
