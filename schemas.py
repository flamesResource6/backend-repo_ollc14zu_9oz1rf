"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

# Cafe-specific schemas

class CafeMenuItem(BaseModel):
    """
    Cafe menu item schema
    Collection name: "cafemenuitem"
    """
    name: str = Field(..., description="Menu item name")
    category: Literal["coffee", "drip", "signature", "seasonal", "pack", "other"] = Field(
        ..., description="Menu category"
    )
    description: Optional[str] = Field(None, description="Short description or tasting notes")
    size: Optional[Literal["small", "large", "bottle", "pack"]] = Field(
        None, description="Serving size if applicable"
    )
    price: int = Field(..., ge=0, description="Price in TWD")
    available: bool = Field(True, description="Whether the item is currently available")


class OrderItem(BaseModel):
    item_name: str
    quantity: int = Field(1, ge=1)
    notes: Optional[str] = None


class Order(BaseModel):
    """
    Customer order / pre-order inquiry
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    phone: str = Field(..., description="Contact phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    preferred_method: Literal["pickup", "delivery"] = Field(
        "pickup", description="Pickup at store or delivery"
    )
    items: List[OrderItem] = Field(..., description="Ordered items")
    pickup_time: Optional[str] = Field(None, description="Preferred pickup time, e.g., 09:30")
    address: Optional[str] = Field(None, description="Delivery address if delivery selected")
    remarks: Optional[str] = Field(None, description="Additional notes")


# Example generic schemas kept for reference
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")


class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
