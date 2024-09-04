FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1
ENV STAGE=${STAGE}
ENV POETRY_VERSION=1.8.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN python3 -m venv "$POETRY_VENV" \
    && "$POETRY_VENV"/bin/pip install -U pip setuptools \
    && "$POETRY_VENV"/bin/pip install poetry==${POETRY_VERSION} \

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . .

# Install dependencies
RUN poetry check && poetry install $(if [ "$STAGE" = 'production' ]; then echo '--with prod --without dev'; fi)  \
    --no-interaction --no-cache --no-root

# Expose the port that the application will listen on
EXPOSE 8000
