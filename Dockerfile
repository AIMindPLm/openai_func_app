# Use the official slim Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install curl and other necessary dependencies
RUN apt-get update && apt-get install -y curl

# Install Poetry using the official installer script
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to the PATH environment variable
ENV PATH="/root/.local/bin:${PATH}"

# Verify Poetry installation
RUN poetry --version

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install project dependencies without creating a virtual environment
RUN poetry install --no-root --no-dev

# Copy the entire project code inside the openai_func_app folder
COPY . .

# Copy the .env file
COPY .env .env

# Expose the application's port
EXPOSE 8080

# Start the application using the proper path to the main module
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
