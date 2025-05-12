#!/bin/bash

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
sleep 5

BOOTSTRAP_SERVER="${KAFKA_HOST:-kafka:9092}"

TOPICS=(
  "asset_daily.created"
)

for TOPIC in "${TOPICS[@]}"
do
  echo "Creating topic: $TOPIC"
  kafka-topics.sh --create \
    --if-not-exists \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --replication-factor 1 \
    --partitions 1 \
    --topic "$TOPIC"
done

echo "Kafka topics created."
