from fastapi.exceptions import HTTPException


class ComplaintsRepository:
    def __init__(self) -> None:
        pass

    async def insert_complaint(self, complaint, collection):
        if not complaint:
            raise HTTPException(status_code=400, detail="Complaint data is required")

        # Check if the collection is valid and operational
        if not collection:
            raise HTTPException(status_code=500, detail="Database collection is not available")

        # Insert the complaint document
        insert_result = await collection.insert_one(complaint.dict())
        if not insert_result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to insert complaint")
        
        return insert_result
