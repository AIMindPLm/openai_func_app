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
- Basic arithmetic functions.
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
│   ├── __init__.py
│   ├── main.py          # Application entry point
│   ├── config.py        # Configuration settings
│   ├── models.py        # Data models (if any)
│   ├── routes.py        # API routes
│   └── utils/           # Utility functions and helpers
│       ├── __init__.py
│       ├── functions.py  # Arithmetic functions
│       ├── openai_api.py # OpenAI API interactions
│       ├── tools.py      # Tool definitions for OpenAI
│       └── function_map.py # Function map for executing functions
tests/                   # Unit and integration tests
├── pyproject.toml       # Poetry configuration file
├── README.md            # Project documentation
└── .env                 # Environment variables file (optional)
```
# API Endpoints
```
# API endpoint 
POST /chat
{
  "messages": [
    {"role": "user", "content": "Add 5 and 3"}
  ]
}

```
## Example Response

```
{
  "role": "assistant",
  "content": "The result of adding 5 and 3 is 8."
}
```
# Testing
## Running Tests

```
# Run tests with Poetry
poetry run pytest
```
