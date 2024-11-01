FROM mongo:4.2.8

WORKDIR /opt
COPY db ./db

CMD ["mongorestore", "--uri", "mongodb://mongodb-headless:27017/demo&replicaSet=rs0&authSource=admin", "--drop", "db"]