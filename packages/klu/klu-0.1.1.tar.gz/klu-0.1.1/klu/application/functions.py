import aiohttp

from typing import List
from aiohttp import ClientResponseError
from aiohttp.web_exceptions import HTTPNotFound

from klu.action.models import Action
from klu.api.client import APIClient
from klu.application.constants import APPLICATION_ENDPOINT
from klu.application.errors import ApplicationNotFoundError
from klu.common.errors import UnknownKluAPIError, UnknownKluError


async def get_application_actions(app_id: str) -> List[Action]:
    """
    Retrieves app actions information based on the app GUID.

    Args:
        app_id (str): ID of an application to fetch actions for.

    Returns: An array of actions found by provided app id.
    """
    async with aiohttp.ClientSession() as session:
        client = APIClient(session)
        try:
            response = await client.get(
                f"{APPLICATION_ENDPOINT}/actions", {"app": app_id}
            )
        except (HTTPNotFound, ClientResponseError) as e:
            if e.status == 404:
                raise ApplicationNotFoundError(app_id)

            raise UnknownKluAPIError(e.status, e.message)
        except Exception:
            raise UnknownKluError()

        return [Action._from_engine_format(action) for action in response]
