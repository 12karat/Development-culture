from fastapi import FastAPI, HTTPException

app = FastAPI(title="Product Service")

PRODUCTS = {
    "laptop": {"name": "Laptop Pro 15", "price": 1200.00, "category": "electronics"},
    "mouse": {"name": "Wireless Mouse", "price": 29.99, "category": "accessories"},
    "keyboard": {"name": "Mechanical Keyboard", "price": 89.99, "category": "accessories"},
    "monitor": {"name": '27" 4K Monitor', "price": 499.00, "category": "electronics"},
    "headphones": {"name": "Noise-Cancelling Headphones", "price": 249.00, "category": "audio"},
}


@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")
    return {"product_id": product_id, **product}


@app.get("/products")
def list_products():
    return [{"product_id": pid, **info} for pid, info in PRODUCTS.items()]


@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}
