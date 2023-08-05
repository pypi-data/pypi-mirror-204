import aiohttp

from typing import List, Union

from klu.api.constants import API_KEY, API_ENDPOINT


class APIClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.headers = {"Authorization": f"Bearer {API_KEY}"}

    async def get(self, path: str, params: dict = None) -> Union[dict, List[dict]]:
        url = f"{API_ENDPOINT}{path}"
        async with self.session.get(
            url, params=params, headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def post(self, path: str, json_data: dict) -> dict:
        url = f"{API_ENDPOINT}{path}"
        async with self.session.post(
            url, json=json_data, headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def put(self, path: str, json_data: dict) -> dict:
        url = f"{API_ENDPOINT}{path}"
        async with self.session.put(
            url, json=json_data, headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def delete(self, path: str) -> dict:
        url = f"{API_ENDPOINT}{path}"
        async with self.session.delete(url, headers=self.headers) as response:
            response.raise_for_status()
            return await response.json()
