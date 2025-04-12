FROM bitnami/cypress:latest AS build

USER 0
RUN apt update && apt install dirmngr ca-certificates software-properties-common apt-transport-https wget -y
RUN wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | gpg --dearmor && tee /usr/share/keyrings/packages.mozilla.org.gpg > /dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/packages.mozilla.org.gpg] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
RUN apt update
RUN apt install firefox -y
RUN apt-get clean && rm -rf /var/lib/apt/lists /var/cache/apt/archives
USER 1001

FROM build AS development
