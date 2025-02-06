from src.app.config.database import mongodb_database
from src.app.model.domain.user import User
from fastapi import Depends, HTTPException
from src.app.model.domain.products import Product
from bson import ObjectId
from src.app.model.domain.items import CartItem
from src.app.model.schemas.user_schemas import UserOut
from typing import List


class UserRepository:
    def __init__(self) -> None:
        pass

    async def find_user_by_email(self, email: str, auth_collection):
        return await auth_collection.find_one({"email": email})

    async def insert_user(self, user_data, auth_collection):
        if await auth_collection.find_one({"email": user_data["email"]}):
            raise HTTPException(status_code=400, detail="User with this email already exists")

        user = User(
            name=user_data["name"],
            email=user_data["email"],
            password_hash=user_data["password_hash"],
            role=user_data["role"]
        )
        return await auth_collection.insert_one(user.to_dict())

    async def insert_products(self, products, products_collection):
        if not products:
            raise HTTPException(status_code=400, detail="Products list is empty")
        return await products_collection.insert_many(products)

    async def insert_product(self, product, products_collection):
        if not product:
            raise HTTPException(status_code=400, detail="Product data is required")

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
        if not all_products:
            raise HTTPException(status_code=404, detail="No products found")

        for product in all_products:
            product["_id"] = str(product["_id"]) if "_id" in product else None
        return all_products

    async def fetch_product_details(self, product_id, products_collection):
        try:
            product_id = ObjectId(product_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        details = await products_collection.find_one({"_id": product_id})
        if not details:
            raise HTTPException(status_code=404, detail="Product not found")

        details["_id"] = str(details["_id"])
        return details

    async def update_product_details(self, product_id, update_data, produts_collection):
        try:
            product_id = ObjectId(product_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        update_result = await produts_collection.update_one({"_id": product_id}, {"$set": update_data})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found or update failed")
        return {"message": "Product updated successfully"}

    async def delete_product(self, product_id, product_collection):
        try:
            product_id = ObjectId(product_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        deleted_result = await product_collection.delete_one({"_id": product_id})
        if deleted_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product deleted successfully"}

    async def insert_cart_item(self, cart_item, cart_orders_collection):
        if not cart_item:
            raise HTTPException(status_code=400, detail="Cart item data is required")

        cart_item = CartItem(
            user_id=cart_item["user_id"],
            product_id=cart_item["product_id"],
            quantity=cart_item["quantity"],
            price=cart_item["price"]
        )
        return await cart_orders_collection.insert_one(cart_item.to_dict())

    async def get_all_users(self, collection) -> List[UserOut]:
        users = await collection.find().to_list()
        if not users:
            raise HTTPException(status_code=404, detail="No users found")

        user_list = []
        for user in users:
            user["_id"] = str(user["_id"])
            user_list.append(UserOut(**user))

        return user_list

    async def update_user_role(self, user_id: str, new_role: str, collection):
        try:
            oid = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        update_result = await collection.update_one({"_id": oid}, {"$set": {"role": new_role}})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or role update failed")

        return {"message": "User role updated successfully"}

    async def get_admins_email(self, collection):
        admins_cursor = await collection.find({"role": "admin"}, {"email": 1, "_id": 0})

        admin_emails = [admin["email"] for admin in await admins_cursor.to_list(length=None)]

        # Handle empty result scenario
        if not admin_emails:
            raise HTTPException(status_code=404, detail="No admin users found")

        return admin_emails
        
    async def get_seller_email(self, product_id, products_collection,auth_collection ):
        product_detail = await self.fetch_product_details(product_id, products_collection)
        seller_id = product_detail["seller_id"]
        seller_details = await auth_collection.find({"_id" : ObjectId(seller_id)})
        seller_email = seller_details["email"]
        return seller_email