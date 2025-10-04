# ============================================
# Stage 1: Builder - Install dependencies and compile packages
# ============================================
FROM python:3.13-slim AS builder

# Set working directory for builder stage
WORKDIR /app

# Install build dependencies
# gcc, python3-dev: Required to compile Python packages from source
# libpq-dev: PostgreSQL client library headers for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy project metadata
COPY pyproject.toml ./

# Create a virtual environment in the builder stage
# This allows us to copy only the installed packages to the final stage
RUN python -m venv /opt/venv

# Activate virtual environment and install dependencies
# Using virtual environment ensures clean separation of packages
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "fastapi>=0.118.0,<0.119.0" \
    "uvicorn>=0.37.0,<0.38.0" \
    "python-dotenv>=1.1.1,<2.0.0" \
    "sqlalchemy>=2.0.43,<3.0.0" \
    "pydantic-settings>=2.11.0,<3.0.0" \
    "psycopg2>=2.9.10,<3.0.0"

# ============================================
# Stage 2: Runtime - Final minimal image
# ============================================
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies (not build tools)
# libpq5: PostgreSQL client library (runtime only, smaller than libpq-dev)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
# This includes all installed Python packages without build dependencies
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY src/ ./src/

# Activate virtual environment for runtime
ENV PATH="/opt/venv/bin:$PATH"

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Start the FastAPI application with uvicorn server
# --host 0.0.0.0: listen on all network interfaces (required for Docker)
# --port 8000: listen on port 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
