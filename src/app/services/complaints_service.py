from src.app.repositories.complaints_repository import ComplaintsRepository
from src.app.utils.email_draft import EmailDraftUtil
from src.app.utils.gmail_api_util import GmailOAuthSender
from fastapi import Depends
from src.app.config.database import mongodb_database
from src.app.repositories.user_repository import UserRepository
from typing import List

class ComplaintsService:
    def __init__(self, complaints_repository= Depends(ComplaintsRepository), complaints_collection = Depends(mongodb_database.get_complaint_collection),
                 auth_collection = Depends(mongodb_database.get_auth_collection),
                 user_repository = Depends(UserRepository),
                 products_collection = Depends(mongodb_database.get_products_collection)):
        self.complaints_repository = complaints_repository 
        self.complaints_collection = complaints_collection
        self.auth_collection = auth_collection
        self.user_repository = user_repository
        self.products_collection = products_collection

    async def save_complaint(self,complaint):
        await self.complaints_repository.insert_complaint(complaint, self.complaints_collection)

    async def send_email_notifications(self, complaint):
        # Generate email subject and body, using the LLM to summarize the issue.
        subject, body = EmailDraftUtil().generate_email_content(complaint)
        recipients = await self.user_repository.get_admins_email(self.auth_collection)
        seller_email = await self.user_repository.get_seller_email(complaint.product_id, 
                                                                   self.products_collection,
                                                                   self.auth_collection)
        recipients.append(seller_email)
        
 
        # Instantiate the Gmail OAuth sender and send the email to each recipient.
        sender = GmailOAuthSender(
            credentials_path='src/app/utils/google_credentials/client_secret.json',
            token_path='src/app/utils/google_credentials/token.json'
        )
        for recipient in recipients:
            sender.send_email(recipient, subject, body)
            
    async def get_all_complaints(self) -> List[dict]:
        # Delegate the database query to the repository.
        return await self.complaints_repository.get_all_complaints(self.complaints_collection)
    
    async def get_complaint_by_id(self, complaint_id: str) -> dict:
        # Delegate to the repository. 
        return await self.complaints_repository.get_complaint_by_id(complaint_id, self.complaints_collection)
