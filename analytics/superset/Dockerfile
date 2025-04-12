ARG VER=4.0.1

FROM apache/superset:${VER} AS base

WORKDIR /app

# ADD logo
COPY --chown=superset:superset assets/images/logo.png /app/superset/static/assets/images/logo.png

# Switching to root to install the required packages
USER root

RUN pip install sqlalchemy-bigquery

# Requiered for SECRET_KEY (it's defined in the superset_config.py)
RUN pip install Flask-OAuthlib Authlib

COPY --chown=superset:superset requirements/database-drivers.txt requirements/
RUN --mount=type=cache,target=/root/.cache/pip \
   pip install --upgrade setuptools pip && \
   pip install -r requirements/database-drivers.txt

# Switching back to using the `superset` user
USER superset

###
### Stage 2: Development
FROM base AS development

# https://www.restack.io/docs/superset-knowledge-apache-superset-config-guide
# https://superset.apache.org/docs/configuration/configuring-superset
ENV SUPERSET_CUSTOM_PATH="/app/superset/custom" \
    SUPERSET_CONFIG_PATH="/app/superset/custom/superset_config.py"

RUN mkdir -p ${SUPERSET_CUSTOM_PATH}
COPY --chown=superset:superset conf/superset_config_dev.py ${SUPERSET_CUSTOM_PATH}/superset_config.py


###
### Stage 2: Production
FROM base AS production

# https://www.restack.io/docs/superset-knowledge-apache-superset-config-guide
# https://superset.apache.org/docs/configuration/configuring-superset
ENV SUPERSET_CUSTOM_PATH="/app/superset/custom" \
    SUPERSET_CONFIG_PATH="/app/superset/custom/superset_config.py"

RUN mkdir -p ${SUPERSET_CUSTOM_PATH}
COPY --chown=superset:superset conf/superset_config.py ${SUPERSET_CUSTOM_PATH}/superset_config.py

