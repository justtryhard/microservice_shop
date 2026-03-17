from src.data import products, users, orders


async def get_products_from_db():
    return products

async def get_orders_from_db():
    return orders

async def get_users_from_db():
    return users