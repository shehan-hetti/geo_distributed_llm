# NOTE: will also work with other cassandra version tags
#FROM cassandra:5.0.3
FROM bitnami/cassandra:5.0.3

# Copy the CQL script into the container
COPY init.cql /docker-entrypoint-initdb.d/
