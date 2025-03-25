FROM python:3.13.2-slim as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

ARG POETRY_VERSION=2.1.1
RUN curl -sSL -o /tmp/install-poetry.py https://install.python-poetry.org \
    && python3 /tmp/install-poetry.py --version ${POETRY_VERSION} \
    && rm /tmp/install-poetry.py

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only=main --no-root --no-ansi  # No dev dependencies

FROM python:3.13.2-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

WORKDIR /app
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN useradd -m appuser && chown -R appuser /app
USER appuser

WORKDIR /app/dogs
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]