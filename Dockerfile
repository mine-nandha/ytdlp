# -------------------------
# 1) Builder stage
# -------------------------
FROM python:3.12-slim AS builder

WORKDIR /src

# Minimal deps to build wheels cleanly
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps into /install (so we copy only what we need)
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir --target=/install -r requirements.txt

# Copy project source
COPY . .

# -------------------------
# 2) Final stage (Distroless)
# -------------------------
FROM gcr.io/distroless/python3

# Copy installed dependencies + app code
COPY --from=builder /install /usr/local
COPY --from=builder /src /app

WORKDIR /app

# Default port
ENV PORT=8000

# Distroless runs as non-root (UID 65532) by default
USER 65532

# Run uvicorn via start.py (no shell in distroless)
CMD ["python", "/app/start.py"]