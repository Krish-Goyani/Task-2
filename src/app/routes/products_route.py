from fastapi import APIRouter, Request, Depends
from src.app.controllers.products_controller import ProductsController
from src.app.utils.limiter import limiter
from src.app.utils.security import authorize
from src.app.model.schemas.product_schemas import Product
from fastapi.requests import Request
from src.app.model.schemas.user_schemas import User
from src.app.utils.security import get_current_user
from src.app.model.schemas.product_schemas import ProductUpdate
from fastapi import UploadFile

products_router = APIRouter(prefix="/products", tags=["Products"])



@products_router.post("/preload-products/")
@limiter.limit("10/minute")
async def preload_products(request: Request, products_controller = Depends(ProductsController)):
    result = await products_controller.preload_products()
    return {"message": result}

@products_router.post("/")
@authorize(role=["seller", "admin"])
async def add_product(request : Request, product : Product , current_user: User = Depends(get_current_user) ,  products_controller = Depends(ProductsController)):
    return await products_controller.add_product(product)

@products_router.get("/")
async def get_all_products(products_controller = Depends(ProductsController)):
    return await products_controller.fetch_all_products_controller()

@products_router.get("/{product_id}")
async def get_product_details(product_id : str  , products_controller = Depends(ProductsController)):
    return await products_controller.products_details_controller(product_id)

@products_router.post("/{product_id}")
@authorize(role=["seller"])
async def update_product_detaisl(request : Request, product_id : str, update_data: ProductUpdate, current_user: User = Depends(get_current_user),  products_controller = Depends(ProductsController)):
    return await products_controller.update_product_details_controller(product_id, update_data, current_user)

@products_router.delete("/{product_id}")
@authorize(role=["seller"])
async def delete_product(request: Request,  product_id : str, current_user: User = Depends(get_current_user),  products_controller = Depends(ProductsController)):
    return await products_controller.delete_product_controller(product_id, current_user)

@products_router.get("/download/{product_id}")
async def download_product_detail(product_id : str, products_controller = Depends(ProductsController)):
    return await products_controller.download_product_controller(product_id)


'''@products_router.post("/upload-pdf")
@authorize(role=["seller"])
async def upload_product_pdf(
    file: UploadFile,
    current_user = Depends(get_current_user),  # Ensure seller access
    controller: ProductsController = Depends()
):
    """
    Allows Sellers to upload a PDF containing product details.
    The PDF is processed using data loaders and an LLM to extract product details.
    """
    return await controller.upload_pdf(file, current_user)'''