from src.app.services.complaints_service import ComplaintsService
from fastapi import Depends, status
from typing import List, Optional
from src.app.model.schemas.complaints_schemas import ComplaintResponse
from fastapi.exceptions import HTTPException


class ComplaintsUseCases:
    def __init__(self, complaints_service = Depends(ComplaintsService)):
        self.complaints_service = complaints_service
        
    async def file_complaint(self, complaint):
        # Save the complaint to the database.
        await self.complaints_service.save_complaint(complaint)
        # Send notifications (email) with the complaint details.
        await self.complaints_service.send_email_notifications(complaint)
        return {"message": "Complaint filed and notifications sent successfully"}
    
    
    async def get_all_complaints(self) -> List[ComplaintResponse]:
        # Retrieve complaints from the service layer.
        complaints = await self.complaints_service.get_all_complaints()
        result = []
        for comp in complaints:
            # Ensure that ObjectIds are converted to strings.
            comp["id"] = str(comp.get("_id"))
            comp["user_id"] = str(comp.get("user_id"))
            comp["order_id"] = str(comp.get("order_id"))
            comp["product_id"] = str(comp.get("product_id"))
            result.append(ComplaintResponse(**comp))
        return result
    
    async def get_complaint_by_id(self, complaint_id: str) -> Optional[ComplaintResponse]:
        complaint_doc = await self.complaints_service.get_complaint_by_id(complaint_id)
        if not complaint_doc:
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found"
            )
        # Convert ObjectId fields to strings
        complaint_doc["id"] = str(complaint_doc.get("_id"))
        complaint_doc["user_id"] = str(complaint_doc.get("user_id"))
        complaint_doc["order_id"] = str(complaint_doc.get("order_id"))
        complaint_doc["product_id"] = str(complaint_doc.get("product_id"))
        return ComplaintResponse(**complaint_doc)


