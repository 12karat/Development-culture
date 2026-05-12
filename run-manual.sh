#!/usr/bin/env bash
# Manual docker run equivalent of docker-compose.yml
# Run from the root of the project: bash run-manual.sh

set -e

NETWORK=order-net

echo "==> Creating shared network '$NETWORK' (if not exists)"
docker network create "$NETWORK" 2>/dev/null || echo "    Network already exists, skipping."

echo "==> Building images"
docker build -t order-system/product-service  ./product-service
docker build -t order-system/discount-service ./discount-service
docker build -t order-system/order-service    ./order-service

echo "==> Starting product-service"
docker run -d \
  --name product-service \
  --network "$NETWORK" \
  -p 8001:8000 \
  order-system/product-service

echo "==> Starting discount-service"
docker run -d \
  --name discount-service \
  --network "$NETWORK" \
  -p 8003:8000 \
  order-system/discount-service

echo "==> Starting order-service"
docker run -d \
  --name order-service \
  --network "$NETWORK" \
  -p 8002:8000 \
  -e PRODUCT_SERVICE_URL=http://product-service:8000 \
  -e DISCOUNT_SERVICE_URL=http://discount-service:8000 \
  order-system/order-service

echo ""
echo "==> System is up."
echo "    order-service   -> http://127.0.0.1:8002"
echo "    product-service -> http://127.0.0.1:8001  (debug)"
echo "    discount-service-> http://127.0.0.1:8003  (debug)"
echo ""
echo "Try:"
echo '  curl -X POST http://127.0.0.1:8002/orders \'
echo '       -H "Content-Type: application/json" \'
echo '       -d '"'"'{"product_id":"laptop","quantity":15,"promo_code":"STUDENT10"}'"'"
echo ""
echo "To stop and clean up: bash stop-manual.sh"
