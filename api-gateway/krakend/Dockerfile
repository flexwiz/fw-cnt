# syntax=docker/dockerfile:1

ARG KRAKEND_VERSION=2.9

###
### Stage 1: Base
FROM devopsfaith/krakend:${KRAKEND_VERSION} AS base

COPY ./config/krakend.json /etc/krakend/krakend.json

##
### Stage 2: Final
FROM base AS final

USER krakend
