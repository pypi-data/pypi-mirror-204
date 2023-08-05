import aiohttp

from typing import List
from aiohttp import ClientResponseError
from aiohttp.web_exceptions import HTTPNotFound

from klu.api.client import APIClient
from klu.data.models import Data, ActionData, DataBaseClass
from klu.data.constants import DATA_ENDPOINT
from klu.data.errors import DataNotFoundError
from klu.action.errors import ActionNotFoundError
from klu.common.errors import UnknownKluAPIError, UnknownKluError


async def get_action_data(action_guid: str) -> List[ActionData]:
    """
    Retrieves data information for an action.

    Args:
        action_guid (str): Guid of an action to fetch data for.

    Returns: An array of actions found by provided app id.
    """
    async with aiohttp.ClientSession() as session:
        client = APIClient(session)
        try:
            response = await client.get(f"{DATA_ENDPOINT}", {"agent": action_guid})
        except (HTTPNotFound, ClientResponseError) as e:
            if e.status == 404:
                raise ActionNotFoundError(action_guid)

            raise UnknownKluAPIError(e.status, e.message)
        except Exception:
            raise UnknownKluError()

        return [ActionData._from_engine_format(data) for data in response]


async def get_single_datum(datum_id: int) -> Data:
    """
    Retrieves data information based on the data ID.

    Args:
        datum_id (str): ID of a datum object to fetch.

    Returns: An object
    """
    async with aiohttp.ClientSession() as session:
        client = APIClient(session)
        try:
            response = await client.get(f"{DATA_ENDPOINT}/{datum_id}")
        except (HTTPNotFound, ClientResponseError) as e:
            if e.status == 404:
                raise DataNotFoundError(datum_id)

            raise UnknownKluAPIError(e.status, e.message)
        except Exception:
            raise UnknownKluError()

        return Data._from_engine_format(response)


async def update_single_datum(datum_id: int, datum_data: DataBaseClass) -> dict:
    """
    Updated data information based on the data ID and provided payload.

    Args:
        datum_id (str): ID of a datum object to update.
        datum_data (DataBaseClass): datum data to update

    Returns: Dictionary with a 'message' key containing successful update message
    """
    async with aiohttp.ClientSession() as session:
        client = APIClient(session)
        try:
            response = await client.post(
                f"{DATA_ENDPOINT}/{datum_id}", datum_data._to_engine_format()
            )
        except (HTTPNotFound, ClientResponseError) as e:
            if e.status == 404:
                raise DataNotFoundError(datum_id)

            raise UnknownKluAPIError(e.status, e.message)
        except Exception:
            raise UnknownKluError()

        return {"message": response.get("message")}
