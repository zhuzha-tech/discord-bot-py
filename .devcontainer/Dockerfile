# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.241.1/containers/python-3/.devcontainer/base.Dockerfile

ARG VARIANT="3.11-bookworm"
FROM mcr.microsoft.com/devcontainers/python:1-${VARIANT}

# Install poetry and use it to install requirements
ARG POETRY_VERSION="1.6.1"
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0
RUN pipx install poetry==${POETRY_VERSION}
COPY poetry.lock pyproject.toml /
RUN poetry install --no-dev --no-root --no-interaction --no-ansi

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1