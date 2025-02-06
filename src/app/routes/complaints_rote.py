from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends, Request
from src.app.controllers.complaints_controller import ComplaintsController
from src.app.model.schemas.complaints_schemas import Complaint
from src.app.utils.security import get_current_user
import uuid
from src.app.utils.security import authorize

complaints_router = APIRouter()

@complaints_router.post("/complaints/")
@authorize(role=["buyer"])
async def file_complaint(
    user_id: str ,
    order_id: str ,
    product_id: str ,
    issue: str,
    file: UploadFile = None,
    controller: ComplaintsController = Depends(),
    current_user = Depends(get_current_user)
):
    """
    Allows Buyers to file a complaint (with an optional image).
    """
    file_url = ""
    if file:
        # Create a unique file name using uuid.
        file_ext = file.filename.split('.')[-1]
        file_name = f"complaints/{uuid.uuid4()}.{file_ext}"
        file_url = await controller.upload_file(file, file_name)

    complaint_data = Complaint(
        user_id=user_id,
        order_id=order_id,
        product_id=product_id,
        issue=issue,
        image_url=file_url,
        status="open"
    )
    return await controller.file_complaint(complaint_data)