#!/bin/bash

# Load variables from .env file
source ../../.env

echo "Dropping old demo data..."

docker exec -it $DB_CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/demo-data/demo-data-down.sql

if [ $? -ne 0 ]; then
    echo "Error dropping demo data"
    exit 1
fi

echo "Setting up new demo data..."

docker exec -it $DB_CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/demo-data/demo-data-up.sql

if [ $? -ne 0 ]; then
    echo "Error executing demo data"
    exit 1
fi

echo "Demo data setup complete."