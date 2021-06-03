import pytest
import requests
import responses

from waves import get_unique_waves_packs

waves_mock = [
    {"id": "1", "pack_id": 1},
    {"id": "2", "pack_id": 2},
    {"id": "3", "pack_id": 2},
    {"id": "3", "pack_id": 1},
]


@responses.activate
def test_get_oms_waves():
    responses.add(
        responses.Response(
            status=200,
            method=responses.GET,
            url="https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/1",
            json=waves_mock,
        ),
    )

    # Add a new response instead of using requests_mock.side_effect
    responses.add(
        responses.Response(
            status=200,
            method=responses.GET,
            url="https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/2",
            json=[{"id": 1, "pack_id": 4}],
        )
    )

    # There is no need to assert the URL again because responses will automatically raise an exception
    # Example (Request made with a extra "/"):
    # E requests.exceptions.ConnectionError: Connection refused by Responses - the call doesn't match any registered mock.
    # E
    # E Request:
    # E - GET https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/1/
    # E
    # E Available matches:
    # E - GET https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/1 URL does not match

    response = get_unique_waves_packs(number_of_requests=2)

    assert response == {1, 2, 4}


@responses.activate
def test_get_oms_waves_raises():
    responses.add(
        responses.Response(
            status=400,
            method="GET",
            url="https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/1",
            json={"message": "Api error."},
        )
    )
    with pytest.raises(requests.exceptions.HTTPError):
        response = get_unique_waves_packs()
