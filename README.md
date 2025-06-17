# Clean Architecture Customer API with FastAPI, GraphQL, and MongoDB

This project implements a Customer management API using FastAPI, GraphQL (Strawberry), and MongoDB, following Clean Architecture principles. It includes unit tests, Docker containerization, and Terraform scripts for deployment to Google Cloud Run.

## Table of Contents

-   [Project Architecture](#project-architecture)
-   [Directory Structure](#directory-structure)
-   [Prerequisites](#prerequisites)
-   [Setup and Installation](#setup-and-installation)
    -   [1. Clone the Repository](#1-clone-the-repository)
    -   [2. Set up Environment Variables](#2-set-up-environment-variables)
    -   [3. Create Virtual Environment and Install Dependencies](#3-create-virtual-environment-and-install-dependencies)
-   [Running the Application Locally](#running-the-application-locally)
-   [API Endpoints](#api-endpoints)
-   [Running Unit Tests](#running-unit-tests)
-   [Building the Docker Image](#building-the-docker-image)
-   [Deployment to Google Cloud Run](#deployment-to-google-cloud-run)

## Project Architecture

This project adheres to Clean Architecture principles, separating concerns into distinct layers:

-   **Domain Layer (`src/domain`)**: Contains business entities, repository interfaces, and use cases (application-specific business rules). It is the core of the application and has no dependencies on other layers.
-   **Application Layer (`src/application`)**: Contains application services that orchestrate the flow of data from the interfaces to the domain and vice-versa. It may also include mappers or DTOs. It depends on the Domain layer.
-   **Infrastructure Layer (`src/infrastructure`)**: Contains implementations of interfaces defined in the Domain layer, such as database repositories (MongoDB implementation) and external service integrations. It depends on the Domain layer.
-   **Interfaces Layer (`src/interfaces`)**: Contains adapters to the outside world, such as the FastAPI web server, GraphQL resolvers, and potentially other UI or CLI components. It depends on the Application and Domain layers for its operations.

This separation helps in creating a system that is:
-   Independent of Frameworks.
-   Testable.
-   Independent of UI.
-   Independent of Database.
-   Independent of any external agency.

## Directory Structure

```
.
├── .dockerignore         # Specifies intentionally untracked files that Docker should ignore
├── Dockerfile            # For containerizing the application
├── pyproject.toml        # Configuration for tools like mutmut (mutation testing)
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── src                   # Source code
│   ├── application       # Application layer (services, mappers)
│   │   ├── __init__.py
│   │   ├── mappers
│   │   └── services
│   ├── domain            # Domain layer (entities, repositories, use cases)
│   │   ├── __init__.py
│   │   ├── entities
│   │   ├── repositories
│   │   └── use_cases
│   ├── infrastructure    # Infrastructure layer (database implementations, external services)
│   │   ├── __init__.py
│   │   └── database
│   └── interfaces        # Interfaces layer (API controllers, GraphQL resolvers)
│       ├── __init__.py
│       ├── api
│       └── graphql_resolvers
├── terraform             # Terraform scripts for GCP deployment
│   ├── main.tf
│   ├── outputs.tf
│   ├── README.md         # Terraform specific README
│   ├── variables.tf
│   └── versions.tf
└── tests                 # Automated tests
    ├── __init__.py
    ├── mutation          # Mutation tests (setup attempted)
    └── unit              # Unit tests for domain and application layers
        ├── __init__.py
        ├── application
        └── domain
```

## Prerequisites

-   Python 3.10+
-   Pip (Python package installer)
-   MongoDB instance (local or remote, e.g., MongoDB Atlas)
-   Docker (for containerization)
-   Google Cloud SDK (gcloud) (for deployment)
-   Terraform (for deployment)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Environment Variables

The application and MongoDB repository require environment variables for configuration. Copy the example `.env.example` file to `.env` and update it with your MongoDB details:

```bash
cp .env.example .env
```

Edit `.env` and set your `MONGO_URI` and `MONGO_DB_NAME`:
```env
# .env
MONGO_URI=mongodb://localhost:27017 # Or your MongoDB Atlas connection string
MONGO_DB_NAME=clean_arch_db
```
The application loads these variables at runtime.

### 3. Create Virtual Environment and Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```
This will install all necessary packages, including FastAPI, Strawberry (for GraphQL), Motor (for MongoDB), Pydantic with email validation support (`pydantic[email]`), and testing tools.

## Running the Application Locally

Once the setup is complete, you can run the FastAPI application using Uvicorn:

```bash
uvicorn src.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be accessible at `http://localhost:8000`.
The GraphQL interface (Strawberry) will be available at `http://localhost:8000/graphql`.
The REST API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

You can interact with it using tools like Postman, Insomnia, or directly through your browser for GraphQL.

## API Endpoints

This project exposes functionality through both GraphQL and RESTful HTTP endpoints.

### GraphQL API

-   **Endpoint**: `/graphql`
-   **Interface**: Interactive GraphQL interface (Strawberry/GraphiQL) available in browser.
-   **Operations**:
    -   **Queries**: `customers`, `customer(id)`
    -   **Mutations**: `createCustomer`, `updateCustomer`, `deleteCustomer`

    Refer to the GraphQL schema (accessible via the interactive interface) for detailed request and response structures.

### RESTful API

FastAPI automatically generates OpenAPI (Swagger) documentation for REST endpoints.

-   **OpenAPI Docs**: `/docs` (Swagger UI)
-   **OpenAPI Spec**: `/openapi.json`

#### Create Customer

-   **Endpoint**: `POST /customers/`
-   **Description**: Creates a new customer.
-   **Request Body**: JSON object with the following fields:
    -   `name` (string, required): Name of the customer.
    -   `email` (string, required, valid email format): Email address of the customer.
    Example:
    ```json
    {
      "name": "Jane Doe",
      "email": "jane.doe@example.com"
    }
    ```
-   **Success Response (201 CREATED)**: JSON object representing the created customer, including its `id`.
    Example:
    ```json
    {
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "id": "generated-uuid-string"
    }
    ```
-   **Error Responses**:
    -   `400 Bad Request`: If a customer with the given email already exists, or other validation errors from the service layer.
    -   `422 Unprocessable Entity`: If the request body fails Pydantic validation (e.g., invalid email format, missing fields).
    -   `500 Internal Server Error`: For unexpected errors.

## Running Unit Tests

Unit tests are written using `pytest`. To run them:

```bash
pytest tests/unit
```

This command will discover and run all unit tests in the `tests/unit` directory.

## Building the Docker Image

A `Dockerfile` is provided to containerize the application.

1.  **Ensure Docker is running.**
2.  **Build the image:**
    Replace `your-image-name` with a name for your image (e.g., `customer-api`).
    ```bash
    docker build -t your-image-name:latest .
    ```
3.  **Run the container (optional, for local testing):**
    This example maps port 8000 on your host to port 80 in the container (as defined by `ENV PORT 80` in Dockerfile and used by Uvicorn).
    You'll also need to pass the MongoDB environment variables.
    ```bash
    docker run -p 8000:80 -e MONGO_URI="your-mongo-uri" -e MONGO_DB_NAME="your-db-name" your-image-name:latest
    ```
    The application inside the container will then be accessible at `http://localhost:8000`.

## Deployment to Google Cloud Run

The application is configured for deployment to Google Cloud Run using Terraform.
Detailed instructions for provisioning the infrastructure and deploying the application can be found in the `terraform/README.md` file.

This involves:
1.  Building the Docker image (as above).
2.  Pushing the image to Google Artifact Registry.
3.  Using Terraform to provision the Cloud Run service and other necessary GCP resources.

---

This README provides a comprehensive guide to understanding, running, and deploying the Clean Architecture Customer API.
