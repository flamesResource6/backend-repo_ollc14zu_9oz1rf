import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from database import db, create_document, get_documents
from schemas import CafeMenuItem, Order

app = FastAPI(title="GAYO Café API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def seed_menu_if_empty():
    try:
        if db is None:
            return
        count = db["cafemenuitem"].count_documents({})
        if count == 0:
            seed_items = [
                {"name": "黑咖啡", "category": "coffee", "description": "現磨純粹咖啡", "size": None, "price": 40, "available": True},
                {"name": "鮮奶咖啡", "category": "coffee", "description": "順口牛奶與咖啡的經典比例", "size": None, "price": 55, "available": True},
                {"name": "特調咖啡", "category": "signature", "description": "店家特調風味", "size": None, "price": 45, "available": True},
                {"name": "掛耳包", "category": "pack", "description": "單包12g 濃郁風味", "size": "pack", "price": 26, "available": True},
                {"name": "烏梅汁(小)", "category": "seasonal", "description": "夏日限定", "size": "small", "price": 40, "available": True},
                {"name": "烏梅汁(大)", "category": "seasonal", "description": "夏日限定", "size": "large", "price": 50, "available": True},
                {"name": "烏梅汁(600cc)", "category": "seasonal", "description": "寶特瓶裝", "size": "bottle", "price": 70, "available": True},
            ]
            for it in seed_items:
                create_document("cafemenuitem", it)
    except Exception:
        # Avoid failing startup if seeding fails
        pass


@app.get("/")
def read_root():
    return {"message": "GAYO Café backend is running"}


@app.get("/api/menu", response_model=List[CafeMenuItem])
def get_menu():
    try:
        docs = get_documents("cafemenuitem", {}, None)
        items = []
        for d in docs:
            items.append({
                "name": d.get("name"),
                "category": d.get("category"),
                "description": d.get("description"),
                "size": d.get("size"),
                "price": int(d.get("price", 0)),
                "available": bool(d.get("available", True)),
            })
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/order")
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"status": "ok", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
