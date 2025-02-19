FROM python:3.13-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-cache --without dev
COPY . .
CMD poetry run alembic upgrade head && \
    poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
