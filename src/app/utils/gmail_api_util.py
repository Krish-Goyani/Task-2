import os
import base64
from email.message import EmailMessage
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailOAuthSender:
    def __init__(self, credentials_path='src/app/utils/google_credentials/client_secret.json', 
                 token_path='src/app/utils/google_credentials/token.json'):
        """
        Initialize Gmail sender with OAuth2 authentication.
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.SCOPES = [
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.readonly'
        ]
        self.creds = None
        # Ensure the credentials directory exists.
        os.makedirs(os.path.dirname(self.token_path), exist_ok=True)

    def authenticate(self):
        """Handle OAuth2 authentication flow."""
        try:
            if os.path.exists(self.token_path) and os.path.getsize(self.token_path) > 0:
                try:
                    self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
                except json.JSONDecodeError:
                    print("Invalid token file. Running new authentication flow.")
                    self.creds = None
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    print("Refreshing expired credentials...")
                    self.creds.refresh(Request())
                else:
                    print("Running OAuth2 authentication flow...")
                    if not os.path.exists(self.credentials_path):
                        raise FileNotFoundError(
                            f"Client secrets file not found at {self.credentials_path}. Please download it from Google Cloud Console."
                        )
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                with open(self.token_path, 'w') as token:
                    token.write(self.creds.to_json())
                print(f"Credentials saved to {self.token_path}")
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            raise

    def send_email(self, to: str, subject: str, body: str):
        """Send email to a single recipient using OAuth2 authenticated Gmail API."""
        try:
            if not self.creds:
                self.authenticate()
            service = build('gmail', 'v1', credentials=self.creds)
            message = EmailMessage()
            message.set_content(body)
            message["To"] = to
            # Set the sender using the authenticated user's profile.
            user_info = service.users().getProfile(userId='me').execute()
            message["From"] = user_info['emailAddress']
            message["Subject"] = subject
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}
            send_message = service.users().messages().send(userId="me", body=create_message).execute()
            print(f'Message sent successfully! Message Id: {send_message["id"]}')
            return send_message
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise
