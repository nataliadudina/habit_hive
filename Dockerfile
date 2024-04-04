# Using a basic Python image
FROM python:3.11

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /code

# Copy the pyproject.toml file to the working directory
COPY pyproject.toml poetry.lock ./


# Set dependancies in the container via Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the project files
COPY . .
