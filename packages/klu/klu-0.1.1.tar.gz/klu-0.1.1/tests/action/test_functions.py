#!/usr/bin/env python
"""Tests for `action` module functions"""
import pytest

from aiohttp import web
from unittest.mock import patch

from tests.action.utils import get_action_data
from klu.application.errors import ApplicationNotFoundError
from klu.application.functions import get_application_actions
from tests.utils.mock import (
    get_api_client_mock,
    client_get_function_mock,
    get_return_value_side_effect,
)


@pytest.mark.asyncio
@patch("klu.application.functions.APIClient", new_callable=get_api_client_mock)
async def test_get_app_actions_converts_response_to_dataclass_provided_valid_response_dicts(
    client_mock,
):
    action_1_guid = "test_action_1"
    action_2_guid = "test_action_2"

    test_action_1 = get_action_data(guid=action_1_guid)
    test_action_2 = get_action_data(guid=action_2_guid)

    client_mock.get = client_get_function_mock(
        get_return_value_side_effect([test_action_1, test_action_2])
    )
    result = await get_application_actions("test")

    assert len(result) == 2
    assert result[0].guid == action_1_guid
    assert result[1].guid == action_2_guid


@pytest.mark.asyncio
@patch("klu.application.functions.APIClient", new_callable=get_api_client_mock)
async def test_get_app_actions_raises_klu_error_provided_404_response_from_api(
    client_mock,
):
    client_mock.get = client_get_function_mock(web.HTTPNotFound())
    with pytest.raises(Exception) as exc_info:
        await get_application_actions("test")

    assert exc_info.type is ApplicationNotFoundError
