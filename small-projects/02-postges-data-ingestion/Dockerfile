FROM python:3.10-bookworm
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
# 'uv sync' creates a virtualenv at /app/.venv by default.
# By adding it to PATH, typing 'python' automatically uses the venv version.
ENV PATH="/app/.venv/bin:$PATH"
COPY ./main.py .
CMD ["/bin/bash"]
