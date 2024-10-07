FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 5001

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5001"]