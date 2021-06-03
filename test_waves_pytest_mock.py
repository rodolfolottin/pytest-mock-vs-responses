import pytest
import requests

from waves import get_unique_waves_packs

waves_mock = [
    {"id": "1", "pack_id": 1},
    {"id": "2", "pack_id": 2},
    {"id": "3", "pack_id": 2},
    {"id": "3", "pack_id": 1},
]


def waves_oms_mock_response(status_code=200, data=waves_mock):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: data

    return response


def test_get_oms_waves(mocker):
    requests_get_mock = mocker.patch("requests.get")
    requests_get_mock.side_effect = [
        waves_oms_mock_response(),
        waves_oms_mock_response(data=[{"id": "3", "pack_id": 4}]),
    ]

    response = get_unique_waves_packs(number_of_requests=2)

    requests_get_mock.assert_has_calls(
        [
            mocker.call("https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/1"),
            mocker.call("https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/2"),
        ]
    )
    # Repeated assert
    assert requests_get_mock.call_count == 2

    assert response == {1, 2, 4}


def test_get_oms_waves_raises(mocker):
    requests_get_mock = mocker.patch("requests.get")
    requests_get_mock.return_value = waves_oms_mock_response(
        status_code=400, data={"message": "Api error."}
    )

    with pytest.raises(requests.exceptions.HTTPError):
        response = get_unique_waves_packs()

    requests_get_mock.assert_called_once_with(
        "https://6082d3aa5dbd2c001757a988.mockapi.io/oms/waves/1"
    )
