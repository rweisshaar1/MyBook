# this directive is used to identify the image from which we want to build the new image. I choose postgres:latest which is the official Docker Image with the tag latest that indicates the latest version
FROM postgres:latest

# Get variables from .env file
ARG POSTGRES_PASSWORD
ARG POSTGRES_USER
ARG POSTGRES_DB

# Set environment variables
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_DB=${POSTGRES_DB}

# used to copy the file specified create_fixtures.sql in a specific folder into the image created /docker-entrypoint-initb.d/ .
COPY 1_users_table.sql /docker-entrypoint-initdb.d/1_users_table.sql

# Copy the demo-data folder and its contents to the Docker image
COPY demo-data/ /docker-entrypoint-initdb.d/demo-data/