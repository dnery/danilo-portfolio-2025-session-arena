ARG UV_VER=0.8
ARG PY_VER=3.13
FROM ghcr.io/astral-sh/uv:$UV_VER-python$PY_VER-trixie-slim AS base

# switch to unprivileged user
RUN useradd -m runner
USER runner
WORKDIR /code

# uv building stuff recommended for images
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PIP_DISABLE_PIP_VERSION_CHECK=1

# install deps only first (better layer caching)
COPY pyproject.toml uv.lock* .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# now move over the code and install project
COPY app ./app
COPY alembic ./alembic
COPY README.md alembic.ini .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked

# create entrypoint script
COPY --chmod=755 <<EOT entrypoint.sh
#!/usr/bin/bash
set -euxo pipefail
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
EOT
RUN sed -i 's/\r$//g' entrypoint.sh

# exporse port, run migrations, start app
EXPOSE 8000
CMD ["bash", "entrypoint.sh"]
