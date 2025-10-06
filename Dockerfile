# syntax=docker/dockerfile:1

############################
# Build stage
############################
FROM python:3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Put the runtime venv outside /app to simplify copies between stages
ENV VENV=/opt/venv
RUN python -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

# Fast installer
RUN pip install --no-cache-dir uv

WORKDIR /app

# README must be present for uv/hatch builds
COPY pyproject.toml README.md ./
# Bring in the rest of the source
COPY . .

# Install project + deps into the venv
RUN uv pip install --python "$VENV/bin/python" --no-cache-dir -e .
# Include pytest for in-image tests
RUN uv pip install --python "$VENV/bin/python" --no-cache-dir pytest

############################
# Final (runtime) stage
############################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy just what's needed (avoid copying the entire /app tree)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Your package contains server.py: cc_simple_server/server.py
COPY --from=builder /app/cc_simple_server ./cc_simple_server
# Tests must be present in final image per assignment
COPY --from=builder /app/tests ./tests
# Keep metadata that some tools expect
COPY --from=builder /app/pyproject.toml ./pyproject.toml
COPY --from=builder /app/README.md ./README.md

# Non-root user
RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
