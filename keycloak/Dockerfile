FROM maven:3.8.4-openjdk-11-slim AS build

COPY ./extension/confidentiality /build

WORKDIR /build

RUN mvn clean install

FROM quay.io/keycloak/keycloak:25.0.4 AS production

COPY themes/ntdt                                           /opt/keycloak/themes/ntdt
COPY themes/base/login/confidentiality.ftl                 /opt/keycloak/themes/base/login

COPY --from=build /build/target/confidentiality.jar        /opt/keycloak/providers

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]