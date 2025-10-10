FROM python:3.11-slim

WORKDIR /app

COPY packages/py-core /app/packages/py-core
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir /app/packages/py-core fastapi uvicorn[standard]

COPY re-po.config.yml /app/re-po.config.yml
COPY apps/api /app/apps/api

ENV RE_PO_CONFIG_PATH=/app/re-po.config.yml
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
