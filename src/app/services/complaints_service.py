from src.app.repositories.complaints_repository import ComplaintsRepository
from src.app.utils.email_draft import EmailDraftUtil
from src.app.utils.gmail_api_util import GmailOAuthSender
from fastapi import Depends
from src.app.config.database import mongodb_database


class ComplaintsService:
    def __init__(self, complaints_repository= Depends(ComplaintsRepository), complaints_colleection = Depends(mongodb_database.get_complaint_collection)):
        self.complaints_repository = complaints_repository 
        self.complaints_colleection = complaints_colleection

    async def save_complaint(self,complaint):
        await self.complaints_repository.insert_complaint(complaint, self.complaints_colleection)

    async def send_email_notifications(self, complaint):
        # Generate email subject and body, using the LLM to summarize the issue.
        subject, body = EmailDraftUtil().generate_email_content(complaint)
        # Define multiple recipients (e.g., Admin and Seller).
        recipients = ["krishgoyani1137@gmail.com", "seller@example.com"]
        # Instantiate the Gmail OAuth sender and send the email to each recipient.
        sender = GmailOAuthSender(
            credentials_path='src/app/utils/google_credentials/client_secret.json',
            token_path='src/app/utils/google_credentials/token.json'
        )
        for recipient in recipients:
            sender.send_email(recipient, subject, body)
