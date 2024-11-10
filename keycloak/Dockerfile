# syntax=docker/dockerfile:1

ARG MAVEN_VERSION=3.8.4-openjdk-11-slim
ARG KEYCLOAK_VERSION=25.0.4

FROM maven:${MAVEN_VERSION} AS build

COPY ./extension/confidentiality /build

WORKDIR /build

RUN mvn clean install

FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS production

COPY themes/ntdt                                           /opt/keycloak/themes/ntdt
COPY themes/base/login/confidentiality.ftl                 /opt/keycloak/themes/base/login

COPY --from=build /build/target/*.jar                      /opt/keycloak/providers

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]