FROM mongo:4.2.8 AS build
WORKDIR /opt
COPY db ./db

FROM build AS development
CMD ["mongorestore", "--uri", "mongodb://mongodb-headless:27017/demo&replicaSet=rs0&authSource=admin", "--drop", "db"]
