# Базовый образ для всех сервисов
FROM python:3.9-slim as base
WORKDIR /app
RUN pip install --no-cache-dir setuptools

# Edge образ
FROM base as edge
COPY requirements/base.txt requirements/edge.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/edge.txt
COPY . .
RUN pip install -e .
CMD ["python", "-m", "src.edge.main"]

# AWS образ
FROM base as aws
COPY requirements/base.txt requirements/aws.txt ./requirements/
RUN pip install --no-cache-dir -r requirements/aws.txt
COPY . .
RUN pip install -e .
CMD ["python", "-m", "src.aws.main"] 