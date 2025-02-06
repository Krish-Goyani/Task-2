
class ComplaintsRepository:
    def __init__(self) -> None:
        pass
    
    async def insert_complaint(self,complaint, collection):
        
        return await collection.insert_one(complaint.dict())
