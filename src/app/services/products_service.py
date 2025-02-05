import aiohttp
from src.app.config.settings import settings
class ProductsService:
    async def fetch_products(self) -> dict:

        async with aiohttp.ClientSession() as session:
            async with session.get(settings.PRODUCTS_URL) as response:
                # Await and return the JSON response
                response_data = await response.json()
                return response_data

