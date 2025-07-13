FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy only pyproject.toml and optional lock file first
COPY pyproject.toml ./

# Install dependencies with uv (lock file if available)
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r pyproject.toml

# Copy the rest of the code
COPY . .

# Activate the venv and run the app
CMD ["uv","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
