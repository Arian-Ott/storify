FROM python:3.12-slim-bookworm


WORKDIR /app


RUN apt update && apt install -y --no-install-recommends \
    build-essential \
 && apt clean \
 && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml .
COPY README.md .  


RUN pip install . --no-cache-dir


COPY api ./api
COPY frontend ./frontend


EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--workers", "1"]
