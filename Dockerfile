FROM python:3.12-slim AS python

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$PATH:$POETRY_HOME/bin"

FROM python AS builder

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && apt-get install -y libpq-dev \
    && apt-get install -y build-essential

WORKDIR /opt/pysetup
COPY pyproject.toml poetry.lock .mise.toml ./

RUN POETRY_VERSION=$(grep -h poetry .mise.toml | awk -F"'" '{print $2}') && \
    curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

COPY ./gig-tracker/ ./gig-tracker
RUN poetry install -n

FROM python AS runtime

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder /opt/pysetup /opt/pysetup

ENV PATH="$PATH:$POETRY_HOME/bin"
WORKDIR /opt/pysetup

ENTRYPOINT ["poetry", "run", "solara", "run", "gig-tracker/ui/pages/__init__.py", "--host=0.0.0.0", "--port=80"]