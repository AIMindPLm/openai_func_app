# OpenAI Function App

This project is a Python application built with FastAPI that leverages OpenAI's API to perform various tasks such as basic arithmetic operations and determining if a number is even or odd. The application includes endpoints for interacting with these functions via a chat-like interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)



## Installation

### Prerequisites
- Python 3.8+
- Poetry

## Steps
```
# Clone the repository
git clone https://github.com/yourusername/openai_func_app.git
```

```
# Navigate to the project directory

cd openai_func_app
```

```
# Install dependencies using Poetry
poetry install
```

```
# Activate the Poetry environment
poetry shell
```

```
# Run the application 
poetry run uvicorn openai_func_app.main:app --reload
```

## Usage
```
# Activate the Poetry environment
poetry shell

# Run the application
poetry run uvicorn openai_func_app.main:app --reload
```

# Features
- RESTful API built with FastAPI.
- Integration with OpenAI's API.
- Getting Top product selling by Quantity, Revenue , Profit , Profit Margin by %
- Getting Low product selling by Quantity , Revenue , Profit , Profit Margin by %
- Custom chat-based interface for interacting with functions.

# Configuration
## Environment Variables
- ENDPOINT_URL: The Azure OpenAI API endpoint.
- AZURE_OPENAI_KEY: The API key for Azure OpenAI.
- DEPLOYMENT_NAME: The name of the OpenAI model deployment.

# Example .env file
```
ENDPOINT_URL=https://example.azure.com/openai/deployments/your-deployment
AZURE_OPENAI_KEY=your-api-key
DEPLOYMENT_NAME=your-deployment-name
```

## Project Structure

```bash 

openai_func_app/
│
├── openai_func_app/         # Main application package
│   ├── utils/               # Utility modules for database connection, validation, etc.
│   │   ├── __init__.py
│   │   ├── db_connector.py  # Database connection logic
│   │   ├── validators.py    # Validation functions
│   │   ├── open_api.py      # Logic for interacting with OpenAI's API
│   │   ├── functions.py     # General functions for various tasks
│   │   ├── helpers.py       # Helper functions
│   ├── metric_map.py        # Mapping metrics to SQL queries
│   ├── main.py              # Entry point of the FastAPI application
│   ├── routes.py            # API route definitions
│   ├── config.py            # Configuration settings
│   ├── function_map.py      # Mapping functions and queries
│   ├── tools.py             # Miscellaneous helper functions
├── tests/                   # Unit and integration tests
│   ├── test_routes.py       # Tests for API routes
├── .env                     # Environment variables (not to be committed to VCS)
├── pyproject.toml           # Poetry configuration file
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules            
```
# API Endpoints
```
# API endpoint 
POST /chat
{
  "messages": [
    {"role": "user", "content": "Give me top 3 low profitable product quantity"}
  ]
}

```
## Example Response

```
{
  "role": "assistant",
  "content": "The top 3 low-profitable products based on quantity for the month of August 2024 are:\n1. Product-04 with a total profit of $7500.00\n2. Product 1 with a total profit of $27000.00\n3. Product 2 with a total profit of $50000.00" "
}
```
# Testing
## Running Tests

```
# Run tests with Poetry
poetry run pytest
```
