#!/bin/bash

echo "Waiting for MongoDB to start..."
sleep 10

echo "Initializing MongoDB Replica Set..."
mongosh --host mongo:27017 <<EOF
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo:27017" },
  ]
})
EOF
