# Order System — три микросервиса в Docker

## Структура

```
order-system/
├── product-service/      # хранит товары и цены
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── discount-service/     # считает скидки
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── order-service/        # координирует создание заказа
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── run-manual.sh         # ручной запуск через docker run
├── stop-manual.sh        # остановка ручного запуска
└── NETWORKING_NOTES.md   # объяснение сетевых кейсов
```

## Запуск через Docker Compose (рекомендуется)

```bash
docker compose up --build
```

Сервисы:
- `order-service`   → http://127.0.0.1:8002
- `product-service` → http://127.0.0.1:8001  (отладка)
- `discount-service`→ http://127.0.0.1:8003  (отладка)

## Ручной запуск через docker run

```bash
bash run-manual.sh
# ...
bash stop-manual.sh   # остановить и удалить
```

## Создать заказ

```bash
curl -X POST http://127.0.0.1:8002/orders \
     -H "Content-Type: application/json" \
     -d '{"product_id": "laptop", "quantity": 15, "promo_code": "STUDENT10"}'
```

Пример ответа:
```json
{
  "product_id": "laptop",
  "product_name": "Laptop Pro 15",
  "quantity": 15,
  "unit_price": 1200.00,
  "subtotal": 18000.00,
  "discount_percent": 10.0,
  "discount_amount": 1800.00,
  "total": 16200.00,
  "discount_reason": "Promo code 'STUDENT10' applied: 10% discount"
}
```

## Промокоды

| Код | Скидка |
|---|---|
| `STUDENT10` | 10% |
| `SALE20` | 20% |
| `VIP30` | 30% |
| `WELCOME5` | 5% |

## Оптовые скидки (без промокода)

| Количество | Скидка |
|---|---|
| ≥ 50 | 15% |
| ≥ 20 | 10% |
| ≥ 10 | 5% |

## Доступные товары

`laptop`, `mouse`, `keyboard`, `monitor`, `headphones`

Список: `GET http://127.0.0.1:8001/products`

## Переменные окружения order-service

| Переменная | Значение внутри Docker |
|---|---|
| `PRODUCT_SERVICE_URL` | `http://product-service:8000` |
| `DISCOUNT_SERVICE_URL` | `http://discount-service:8000` |

Значения передаются через переменные окружения и **не зашиты в код**.
