import requests

MOCK_API_URL = "https://6082d3aa5dbd2c001757a988.mockapi.io/oms"


def get_unique_waves_packs(number_of_requests=1):
    waves = set()

    for number in range(1, number_of_requests + 1):
        response = requests.get(f"{MOCK_API_URL}/waves/{number}")
        response.raise_for_status()

        for wave in response.json():
            waves.add(wave["pack_id"])

    return waves
