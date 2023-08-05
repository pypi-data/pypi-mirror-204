from unittest.mock import patch
from tests.utils.mock import APIClientMock


def mock_api_client():
    api_client_patch = patch("klu.api.client.APIClient", new=APIClientMock())
    api_client_patch.start()


# We need it at global level to make sure APIClient is always mocked no matter which function is running
mock_api_client()
