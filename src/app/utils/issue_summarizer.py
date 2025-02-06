from langchain_google_genai import GoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from src.app.config.settings import settings

class IssueSummarizer:
    def __init__(self):
        # Initialize Gemini Pro model
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",  
            google_api_key=settings.GEMINI_API_KEY
        )

    def summarize_issue(self, complaint_text: str) -> str:
        prompt_template = """You are a professional customer support assistant.
        Summarize the customer's complaint into a concise, actionable summary.

        Complaint: {complaint}

        Summary:"""
        prompt = PromptTemplate.from_template(prompt_template)
        formatted_prompt = prompt.format(complaint=complaint_text)

        response = self.llm.invoke(formatted_prompt)  
        return response.strip() if response else "Summary not available"