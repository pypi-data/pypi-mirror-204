from typing import Optional

import aiohttp

from aiohttp import ClientResponseError
from aiohttp.web_exceptions import HTTPNotFound

from klu.common.errors import (
    UnknownKluError,
    UnknownKluAPIError,
    WorkspaceNotFoundError,
)
from klu.api.client import APIClient
from klu.action.errors import ActionNotFoundError, InvalidActionPromptData
from klu.action.models import ActionPromptResponse, PlaygroundPromptResponse
from klu.action.constants import ACTION_PROMPT_ENDPOINT, PLAYGROUND_PROMPT_ENDPOINT


async def run_action_prompt(
    action_id: str,
    prompt: str,
    filter: Optional[str] = None,
    streaming: Optional[str] = None,
) -> ActionPromptResponse:
    """
    Run a prompt with an agent, optionally using streaming.

    Args:
        prompt (str): The prompt to run with the agent.
        action_id (str): The GUID of the agent to run the prompt with.
        filter (Optional[str]): The filter to use when running the prompt.
        streaming (Optional[str]): Whether to use streaming or not. Set to "true" if you want to enable streaming

    Returns: An object result of running the prompt with the message and a feedback_url for providing feedback.
    """
    async with aiohttp.ClientSession() as session:
        client = APIClient(session)
        try:
            response = await client.post(
                ACTION_PROMPT_ENDPOINT,
                {
                    "filter": filter,
                    "prompt": prompt,
                    "agent": action_id,
                    "streaming": streaming,
                },
            )
        except (HTTPNotFound, ClientResponseError) as e:
            if e.status == 404:
                raise ActionNotFoundError(action_id)

            raise UnknownKluAPIError(e.status, e.message)
        except Exception:
            raise UnknownKluError()

        return ActionPromptResponse(**response)


async def run_playground_prompt(
    prompt: str,
    model_id: str,
    tool_ids: Optional[list] = None,
    index_ids: Optional[list] = None,
    model_config: Optional[dict] = None,
) -> PlaygroundPromptResponse:
    """
    Run a prompt with an agent, optionally using streaming.

    Args:
        prompt (str): The prompt to run.
        model_id (int): The ID of the model to use.
        tool_ids (list): Optional list of tool IDs to use. Defaults to an empty array
        index_ids (list): Optional list of index IDs to use. Defaults to an empty array
        model_config (dict): Optional configuration of the model

    Returns: An object result of running the prompt with the message and a feedback_url for providing feedback.
    """
    tool_ids = tool_ids or []
    index_ids = index_ids or []

    async with aiohttp.ClientSession() as session:
        client = APIClient(session)
        try:
            response = await client.post(
                PLAYGROUND_PROMPT_ENDPOINT,
                {
                    "prompt": prompt,
                    "toolIds": tool_ids,
                    "modelId": model_id,
                    "indexIds": index_ids,
                    "modelConfig": model_config,
                },
            )
        except (HTTPNotFound, ClientResponseError) as e:
            if e.status == 404:
                raise WorkspaceNotFoundError()
            if e.status == 400:
                raise InvalidActionPromptData(e.message)

            raise UnknownKluAPIError(e.status, e.message)
        except Exception:
            raise UnknownKluError()

        return PlaygroundPromptResponse(**response)
