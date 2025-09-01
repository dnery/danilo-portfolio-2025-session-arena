FROM python:3.13.7-slim-trixie AS base

# uv building stuff recommended for images
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PIP_DISABLE_PIP_VERSION_CHECK=1

# install uv (see https://docs.astral.sh/uv/guides/integration/docker)
ADD --chmod=755 https://astral.sh/uv/install.sh /uv-install.sh
RUN /uv-install.sh && rm /uv-install.sh
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /code

# install deps only first (better layer caching)
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev

# now move over the code and install project
COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

# expose/greet with non-root
RUN useradd -m runner
USER runner
EXPOSE 8000

# exporse port, run migrations, start API
CMD uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
