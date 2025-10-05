# Optimized Alpine-based Dockerfile for minimal image size
# Target: ~80-120MB (50MB is not achievable with Python + FastAPI + PostgreSQL stack)
#
# IMPORTANT: This is an experimental optimization. Use standard Dockerfile for production
# unless you've thoroughly tested this variant.

# ============================================================================
# Stage 1: Builder - Install dependencies
# ============================================================================
FROM python:3.11-alpine AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies for Alpine
# postgresql-dev: PostgreSQL client development files
# gcc, musl-dev: Required for compiling Python packages
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev

WORKDIR /app

# Copy dependency file
COPY pyproject.toml ./

# Install dependencies directly with pip (no Poetry - project uses PEP 621 format)
# Use psycopg2-binary instead of psycopg2 for pre-compiled wheels
RUN pip install --no-cache-dir \
    "fastapi>=0.118.0,<0.119.0" \
    "uvicorn>=0.37.0,<0.38.0" \
    "python-dotenv>=1.1.1,<2.0.0" \
    "sqlalchemy>=2.0.43,<3.0.0" \
    "pydantic-settings>=2.11.0,<3.0.0" \
    "psycopg2-binary>=2.9.10,<3.0.0" && \
    pip uninstall -y pip setuptools wheel

# ============================================================================
# Stage 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.11-alpine AS runtime

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    ENVIRONMENT=dev

# Install only runtime dependencies
RUN apk add --no-cache \
    libpq \
    libffi && \
    rm -rf /var/cache/apk/*

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder --chown=appuser:appuser /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder --chown=appuser:appuser /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy application source code
COPY --chown=appuser:appuser src /app/src

# Copy production environment configuration
COPY --chown=appuser:appuser .env.dev /app/.env.dev

# Compile Python files to bytecode and remove source files to save space
RUN python -m compileall -b /app/src && \
    find /app/src -name "*.py" -delete && \
    find /app/src -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Remove unnecessary files from site-packages
RUN find /usr/local/lib/python3.11/site-packages -name "*.pyc" -delete && \
    find /usr/local/lib/python3.11/site-packages -name "*.pyo" -delete && \
    find /usr/local/lib/python3.11/site-packages -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -name "tests" -type d -exec rm -rf {} + 2>/dev/null || true

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8080}/docs').read()" || exit 1

# Start application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1", "--log-level", "info", "--no-access-log"]
