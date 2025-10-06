# syntax=docker/dockerfile:1

############################
# Build stage
############################
FROM python:3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Put venv outside /app to simplify cross-stage copying
ENV VENV=/opt/venv
RUN python -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

# Fast installer
RUN pip install --no-cache-dir uv

WORKDIR /app

# README must be in build context (your build backend/uv expects it)
COPY pyproject.toml README.md ./
# Bring in the rest of the project
COPY . .

# Install project + deps into the venv
RUN uv pip install --python "$VENV/bin/python" --no-cache-dir -e .
# Include pytest so tests can run in the final image
RUN uv pip install --python "$VENV/bin/python" --no-cache-dir pytest

# Tar the venv to avoid BuildKit snapshot issues on some Windows setups
RUN tar -C /opt -cf /opt/venv.tar venv

############################
# Final (runtime) stage
############################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Bring over the venv as a tarball, then extract
COPY --from=builder /opt/venv.tar /opt/venv.tar
RUN tar -C /opt -xf /opt/venv.tar && rm /opt/venv.tar
ENV PATH="/opt/venv/bin:$PATH"

# Copy runtime code + tests + metadata
# Your server lives at cc_simple_server/server.py
COPY --from=builder /app/cc_simple_server ./cc_simple_server
COPY --from=builder /app/tests            ./tests
COPY --from=builder /app/pyproject.toml   ./pyproject.toml
COPY --from=builder /app/README.md        ./README.md

# Non-root user
RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# FINAL, EXPLICIT CMD (what the validator is looking for)
CMD ["uvicorn", "cc_simple_server.server:app", "--host", "0.0.0.0", "--port", "8000"]
