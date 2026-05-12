import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service")

# URLs come from environment variables — never hardcoded
PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL")
DISCOUNT_SERVICE_URL = os.environ.get("DISCOUNT_SERVICE_URL")


def _check_config():
    """Fail fast with a clear message if env vars are missing."""
    missing = []
    if not PRODUCT_SERVICE_URL:
        missing.append("PRODUCT_SERVICE_URL")
    if not DISCOUNT_SERVICE_URL:
        missing.append("DISCOUNT_SERVICE_URL")
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Set them before starting the service."
        )


# Validate on startup so the error is obvious immediately
@app.on_event("startup")
def startup_check():
    _check_config()


class OrderRequest(BaseModel):
    product_id: str
    quantity: int
    promo_code: str | None = None


class OrderResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    discount_percent: float
    discount_amount: float
    total: float
    discount_reason: str


@app.post("/orders", response_model=OrderResponse)
def create_order(req: OrderRequest):
    if req.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    # Step 1: fetch product info
    try:
        product_resp = httpx.get(
            f"{PRODUCT_SERVICE_URL}/products/{req.product_id}", timeout=5.0
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach product-service: {exc}",
        )

    if product_resp.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"Product '{req.product_id}' not found"
        )
    if product_resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"product-service returned {product_resp.status_code}",
        )

    product = product_resp.json()
    unit_price: float = product["price"]
    product_name: str = product["name"]

    # Step 2: fetch discount
    try:
        discount_resp = httpx.post(
            f"{DISCOUNT_SERVICE_URL}/discounts/calculate",
            json={
                "product_id": req.product_id,
                "quantity": req.quantity,
                "unit_price": unit_price,
                "promo_code": req.promo_code,
            },
            timeout=5.0,
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach discount-service: {exc}",
        )

    if discount_resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"discount-service returned {discount_resp.status_code}",
        )

    discount = discount_resp.json()
    discount_percent: float = discount["discount_percent"]
    discount_reason: str = discount["reason"]

    # Step 3: calculate totals
    subtotal = round(unit_price * req.quantity, 2)
    discount_amount = round(subtotal * discount_percent / 100, 2)
    total = round(subtotal - discount_amount, 2)

    return OrderResponse(
        product_id=req.product_id,
        product_name=product_name,
        quantity=req.quantity,
        unit_price=unit_price,
        subtotal=subtotal,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        total=total,
        discount_reason=discount_reason,
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}
