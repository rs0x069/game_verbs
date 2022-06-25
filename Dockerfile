# BUILD STAGE
FROM python:3.10-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip &&  \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r /app/requirements.txt

# RUN STAGE
FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --upgrade pip &&  \
    pip install --no-cache /wheels/*

COPY . .

ENTRYPOINT ["/app/docker-entrypoint.sh"]
