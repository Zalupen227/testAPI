import pytest
import requests
import allure


@allure.epic("ReqRes API")
@allure.feature("Basic API Tests")
class TestBasicAPI:

    @allure.story("API Health Check")
    @allure.title("Test API is accessible")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_request(self, base_url, api_headers):
        with allure.step("Send simple GET request"):
            response = requests.get(f"{base_url}/users/1", headers=api_headers)

        with allure.step("Verify API response"):
            assert response.status_code == 200
            assert "data" in response.json()