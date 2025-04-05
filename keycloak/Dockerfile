# syntax=docker/dockerfile:1

ARG MAVEN_VERSION=3.8.4-openjdk-11-slim
ARG KEYCLOAK_VERSION=26.1.4

###
### Stage 1: Build Keycloak extension
FROM maven:${MAVEN_VERSION} AS maven-build

# # Create user and group
# RUN groupadd -r maven && useradd --no-log-init -r -g maven maven

# # Set the active user
# USER maven

# Define extension directory
ENV HOME=/build

# Set working directory
WORKDIR $HOME

# Create application folder and assign rights to the node user
RUN mkdir -p $HOME

# Copy keycloak extension to the image at $HOME
COPY ./extension/confidentiality .

# Run maven install
RUN mvn clean install

###
### Stage 2: Keycloak base image
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS keycloak-build

# Set working directory
WORKDIR /opt/keycloak

# Copy Keycloak themes to the image
COPY --chown=keycloak:keycloak themes/base/login/confidentiality.ftl        ./themes/base/login
COPY --chown=keycloak:keycloak themes/ntdt                                  ./themes/ntdt

# Copy Keycloak extension from build stage to the image
COPY --chown=keycloak:keycloak --chmod=644 --from=maven-build /build/target/*.jar ./providers

# for demonstration purposes only, please make sure to use proper certificates in production instead
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore
RUN /opt/keycloak/bin/kc.sh build

###
### Stage 3: Keycloak base image
FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS keycloak-base

# Enable health and metrics support
# https://www.keycloak.org/server/containers
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Configure a database vendor
ENV KC_DB=postgres

# Set working directory
WORKDIR /opt/keycloak

# Copy Keycloak from build stage to the image
COPY --chown=keycloak:keycloak --from=keycloak-build /opt/keycloak/ .

###
### Stage 4: Keycloak development image
FROM keycloak-base AS development

# Set working directory
WORKDIR /opt/keycloak

# Copy local data to the image
COPY --chown=keycloak:keycloak import ./data/import
COPY --chown=keycloak:keycloak export ./data/export

# Set entrypoint
ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev", "--cache=local"]

###
### Stage 5: Keycloak production image
FROM keycloak-base AS production

# Set entrypoint
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
