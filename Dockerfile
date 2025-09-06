# =========================
# 1. Builder stage
# =========================
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Prevent Python from writing pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required only for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a separate folder
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# 2. Runtime stage
# =========================
FROM python:3.11-slim-bullseye

WORKDIR /app

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy only the application code (keep it lean)
COPY . .

# Create necessary folders
RUN mkdir -p data models

# Cloud Run expects the container to listen on PORT (default 8080)
ENV PORT=8080
EXPOSE 8080

# Healthcheck (optional but useful)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Start the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
