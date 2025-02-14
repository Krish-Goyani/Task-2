import time
import json
import httpx
from groq import Groq
from src.app.config.settings import settings

class ProductsDetailExtractor:
    def __init__(self, api_key: str = settings.GROQ_API_KEY, model_name: str = "llama-3.3-70b-versatile", max_retries: int = 3, retry_delay: int = 2):
        self.client = Groq(api_key=api_key, http_client=httpx.Client(verify=False))
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def extract_details(self, schema, md_text):
        attempt = 0
        while attempt < self.max_retries:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a highly accurate information extractor. You will be given a products details, "
                                "and your task is to extract relevant details strictly following the provided JSON schema. "
                                "Ensure the JSON is valid and adheres exactly to the specified structure, without adding explanations or extra text.\n\n"
                                f"JSON response format:\n```json\n{json.dumps(schema.model_json_schema(), indent=2)}\n```"
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Extract the details from the following products details:\n\n{md_text}"
                        },
                        {
                            "role": "assistant",
                            "content": "```json\n"
                        }
                    ],
                    model=self.model_name,
                    stop="```"
                )
                response  = chat_completion.choices[0].message.content
                parsed_response = json.loads(response)
                product_data = parsed_response["properties"]
                return schema.model_validate(product_data)
            
            except Exception as e:
                attempt += 1
                print(f"Error encountered: {e}. Retrying {attempt}/{self.max_retries}...")
                if attempt >= self.max_retries:
                    raise Exception("Max retries exceeded, unable to validate the response.")
                time.sleep(self.retry_delay)
