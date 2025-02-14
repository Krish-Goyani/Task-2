from fastapi.exceptions import HTTPException
from typing import List, Optional
from bson import ObjectId

class ComplaintsRepository:
    def __init__(self) -> None:
        pass

    async def insert_complaint(self, complaint, collection):
        if not complaint:
            raise HTTPException(status_code=400, detail="Complaint data is required")

        # Insert the complaint document
        insert_result = await collection.insert_one(complaint.dict())
        if not insert_result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert complaint")
        
        return insert_result
    
    async def get_all_complaints(self, collection) -> List[dict]:
        complaints = []
        cursor = collection.find({})
        async for document in cursor:
            complaints.append(document)
        return complaints
    
    async def get_complaint_by_id(self, complaint_id: str, collection) -> Optional[dict]:
        try:
            oid = ObjectId(complaint_id)
        except Exception as e:
            return None

        complaint = await collection.find_one({"_id": oid})
        if complaint is None:
            return None
        return complaint
        