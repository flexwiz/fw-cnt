# syntax=docker/dockerfile:1

ARG VERSION=0.54.3.1

###
### Stage 1: Base
FROM metabase/metabase:v${VERSION} AS base

# Environment configuration
ENV MB_DB_TYPE=postgres
ENV MB_DB_PORT=5432
ENV JAVA_OPTS="-Xmx2g -Xms1g"

# Copy custom plugins if needed
COPY plugins/ /plugins/

##
### Stage 2: Final
FROM base AS final

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

USER metabase
