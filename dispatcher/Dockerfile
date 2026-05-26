# Image used by HF Spaces (Docker SDK) to run the dispatcher.
#
# Built from the dispatcher/ directory:
#   docker build -t jobs-actions-dispatcher dispatcher/
#
# For local dev:
#   docker run --rm -p 7860:7860 \
#     --env-file .env jobs-actions-dispatcher
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=7860

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the dispatcher package itself
COPY . /app/dispatcher
# The package expects to be imported as `dispatcher.*`
ENV PYTHONPATH=/app

# HF Spaces requires the server to listen on $PORT (default 7860).
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS "http://localhost:${PORT}/healthz" || exit 1

CMD ["sh", "-c", "uvicorn dispatcher.app:app --host 0.0.0.0 --port ${PORT}"]
