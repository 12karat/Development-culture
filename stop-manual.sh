#!/usr/bin/env bash
# Stops and removes all containers and the shared network

set -e

echo "==> Stopping containers"
docker stop order-service product-service discount-service 2>/dev/null || true

echo "==> Removing containers"
docker rm order-service product-service discount-service 2>/dev/null || true

echo "==> Removing network"
docker network rm order-net 2>/dev/null || true

echo "Done."
