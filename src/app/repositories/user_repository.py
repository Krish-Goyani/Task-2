
from src.app.config.database import mongodb_database
from src.app.model.domain.user import User
from fastapi import Depends
from src.app.model.domain.products import Product
from bson import ObjectId
from src.app.model.domain.items import CartItem

from fastapi.exceptions import HTTPException


class UserRepository:
    def __init__(self) -> None:
        pass

    async def find_user_by_email(self, email: str, auth_collection):
        return await auth_collection.find_one({"email": email})

    async def insert_user(self, user_data, auth_collection):
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            password_hash=user_data["password_hash"],
            role=user_data["role"])

        return await auth_collection.insert_one(user.to_dict())

    async def insert_products(self, products, products_collection):
        return await products_collection.insert_many(products)

    async def insert_product(self, product, products_collection):
        product = Product(
            title=product.title,
            description=product.description,
            category=product.category,
            price=product.price,
            rating=product.rating,
            brand=product.brand,
            seller_id=product.seller_id
        )

        return await products_collection.insert_one(product.to_dict())

    async def fetch_all_products(self, products_collection):
        all_products = await products_collection.find().to_list()

        for product in all_products:
            product["_id"] = str(product["_id"]) if "_id" in product else None
        return all_products

    async def fetch_product_details(self, product_id, products_collection):

        details = await products_collection.find_one({"_id": ObjectId(product_id)})
        print(details)
        details["_id"] = str(details["_id"])
        return details

    async def update_product_details(self, product_id, update_data, produts_collection):
        return await produts_collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})

    async def delete_product(self, product_id, product_collection):
        deleted_result = await product_collection.delete_one(
            {"_id": ObjectId(product_id)}
        )
        if deleted_result.deleted_count == 0:
            raise HTTPException(status_code=404,
                                detail="user not found")

        return {"message": "product deleted successfully"}

    async def insert_cart_item(self, cart_item, cart_orders_collection):
        cart_item = CartItem(user_id=cart_item["user_id"],
                             product_id=cart_item["product_id"],
                             quantity=cart_item["quantity"],
                             price=cart_item["price"])
        return await cart_orders_collection.insert_one(cart_item.to_dict())
