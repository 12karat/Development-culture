import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Discount Service")

# Promo codes: code -> discount percentage
PROMO_CODES = {
    "STUDENT10": 10.0,
    "SALE20": 20.0,
    "VIP30": 30.0,
    "WELCOME5": 5.0,
}

# Bulk discount rules: min_quantity -> discount percentage
BULK_RULES = [
    (50, 15.0),
    (20, 10.0),
    (10, 5.0),
]


class DiscountRequest(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    promo_code: str | None = None


class DiscountResponse(BaseModel):
    discount_percent: float
    reason: str


@app.post("/discounts/calculate", response_model=DiscountResponse)
def calculate_discount(req: DiscountRequest):
    # Check promo code first (highest priority)
    if req.promo_code:
        code = req.promo_code.strip().upper()
        if code in PROMO_CODES:
            pct = PROMO_CODES[code]
            return DiscountResponse(
                discount_percent=pct,
                reason=f"Promo code '{code}' applied: {pct}% discount",
            )
        else:
            # Invalid promo code — fall through to bulk check
            pass

    # Check bulk discount
    for min_qty, pct in BULK_RULES:
        if req.quantity >= min_qty:
            return DiscountResponse(
                discount_percent=pct,
                reason=f"Bulk discount: {pct}% for {req.quantity} units (≥{min_qty})",
            )

    return DiscountResponse(
        discount_percent=0.0,
        reason="No applicable discount rules",
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "discount-service"}
