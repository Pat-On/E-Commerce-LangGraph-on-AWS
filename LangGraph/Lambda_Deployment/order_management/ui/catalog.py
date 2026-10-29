# =============================================================
# Product catalog for the AnyCart Streamlit UI
# =============================================================

PRODUCTS = [
    {
        "product_id": "SHOE-001",
        "name": "Classic Running Shoes",
        "category": "Shoes",
        "price": 89.99,
        "description": "Lightweight and breathable running shoes for everyday training.",
    },
    {
        "product_id": "SHOE-002",
        "name": "Leather Casual Loafers",
        "category": "Shoes",
        "price": 129.99,
        "description": "Premium leather loafers for a polished casual look.",
    },
    {
        "product_id": "SHOE-003",
        "name": "Trail Hiking Boots",
        "category": "Shoes",
        "price": 149.99,
        "description": "Waterproof hiking boots with rugged grip for all terrains.",
    },
    {
        "product_id": "CLO-001",
        "name": "Cotton Crew-Neck Tee",
        "category": "Clothing",
        "price": 29.99,
        "description": "Soft 100% cotton t-shirt available in multiple colors.",
    },
    {
        "product_id": "CLO-002",
        "name": "Slim Fit Denim Jeans",
        "category": "Clothing",
        "price": 69.99,
        "description": "Modern slim-fit jeans with stretch comfort fabric.",
    },
    {
        "product_id": "CLO-003",
        "name": "Wool Blend Overcoat",
        "category": "Clothing",
        "price": 199.99,
        "description": "Elegant wool blend overcoat for cooler weather.",
    },
    {
        "product_id": "ACC-001",
        "name": "Leather Crossbody Bag",
        "category": "Accessories",
        "price": 79.99,
        "description": "Compact crossbody bag with adjustable strap.",
    },
    {
        "product_id": "ACC-002",
        "name": "Stainless Steel Watch",
        "category": "Accessories",
        "price": 159.99,
        "description": "Minimalist stainless steel watch with sapphire crystal.",
    },
    {
        "product_id": "ACC-003",
        "name": "Polarized Sunglasses",
        "category": "Accessories",
        "price": 49.99,
        "description": "UV400 polarized sunglasses with lightweight titanium frame.",
    },
]

FEATURED_PRODUCTS = [p for p in PRODUCTS if p["product_id"] in (
    "SHOE-001", "CLO-002", "ACC-002", "SHOE-003", "CLO-003", "ACC-001"
)]


def format_price(price: float) -> str:
    """Format a numeric price as a dollar string."""
    return f"${price:.2f}"


def all_categories() -> list[str]:
    """Return sorted unique category names."""
    return sorted(set(p["category"] for p in PRODUCTS))
