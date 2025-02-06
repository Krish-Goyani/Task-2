from fastapi import Request, Depends
from src.app.usecases.complaints_usecase import ComplaintsUseCases
from src.app.model.schemas.complaints_schemas import Complaint
from src.app.utils.gcs_upload import GoogleCloudStorage


class ComplaintsController:
    def __init__(self, complaints_usecases: ComplaintsUseCases = Depends(), google_cloud_storgae = Depends(GoogleCloudStorage)):
        self.complaints_usecases = complaints_usecases
        self.google_cloud_storgae = google_cloud_storgae

    async def file_complaint(self, complaint: Complaint):
        return await self.complaints_usecases.file_complaint(complaint)

    async def upload_file(self, file, file_name: str) -> str:
        # Upload the file via Google Cloud Storage and return the public URL.
        return self.google_cloud_storgae.upload_image(file.file, file_name)
