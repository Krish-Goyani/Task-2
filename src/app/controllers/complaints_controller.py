from fastapi import Request, Depends, status
from src.app.usecases.complaints_usecase import ComplaintsUseCases
from src.app.model.schemas.complaints_schemas import Complaint
from src.app.utils.gcs_upload import GoogleCloudStorage
from typing import List
from src.app.model.schemas.complaints_schemas import ComplaintResponse
from fastapi.exceptions import HTTPException

class ComplaintsController:
    def __init__(self, complaints_usecases: ComplaintsUseCases = Depends(), google_cloud_storgae = Depends(GoogleCloudStorage)):
        self.complaints_usecases = complaints_usecases
        self.google_cloud_storgae = google_cloud_storgae

    async def file_complaint(self, complaint: Complaint):
        return await self.complaints_usecases.file_complaint(complaint)

    async def upload_file(self, file, file_name: str) -> str:
        # Upload the file via Google Cloud Storage and return the public URL.
        return self.google_cloud_storgae.upload_image(file.file, file_name)
    
    async def get_all_complaints(self) -> List[ComplaintResponse]:
        complaints_data = await self.complaints_usecases.get_all_complaints()
        return complaints_data
    
    
    async def get_complaint_by_id(self, complaint_id: str) -> ComplaintResponse:
        complaint = await self.complaints_usecases.get_complaint_by_id(complaint_id)
        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found"
            )
        return complaint
