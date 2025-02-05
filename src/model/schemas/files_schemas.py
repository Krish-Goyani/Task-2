from pydantic import BaseModel
from typing import List, Literal
from bson import ObjectId


class FileUpload(BaseModel):
    user_id: ObjectId
    file_url: str
    file_type: Literal["product", "complaint"]