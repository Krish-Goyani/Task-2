from src.app.services.complaints_service import ComplaintsService
from fastapi import Depends

class ComplaintsUseCases:
    def __init__(self, complaints_service = Depends(ComplaintsService)):
        self.complaints_service = complaints_service
        
    async def file_complaint(self, complaint):
        # Save the complaint to the database.
        await self.complaints_service.save_complaint(complaint)
        # Send notifications (email) with the complaint details.
        await self.complaints_service.send_email_notifications(complaint)
        return {"message": "Complaint filed and notifications sent successfully"}
