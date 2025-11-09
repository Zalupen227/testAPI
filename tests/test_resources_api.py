import pytest
import requests
import allure
import json


@allure.epic("ReqRes API")
@allure.feature("Resources Management")
class TestResourcesAPI:

    @allure.story("Get Resources")
    @allure.title("Get list of resources")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_resources_list(self, base_url, api_headers):
        with allure.step("Send GET request to /unknown"):
            response = requests.get(
                f"{base_url}/unknown",
                headers=api_headers
            )
            allure.attach(json.dumps(response.json(), indent=2), "Resources List", allure.attachment_type.JSON)

        with allure.step("Verify resources data"):
            assert response.status_code == 200
            data = response.json()
            assert "page" in data
            assert "per_page" in data
            assert "total" in data
            assert "data" in data

            if data["data"]:
                resource = data["data"][0]
                assert "id" in resource
                assert "name" in resource
                assert "year" in resource
                assert "color" in resource
                assert "pantone_value" in resource

    @allure.story("Get Single Resource")
    @allure.title("Get resource by ID")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_single_resource(self, base_url, api_headers):
        with allure.step("Send GET request to /unknown/2"):
            response = requests.get(
                f"{base_url}/unknown/2",
                headers=api_headers
            )
            allure.attach(json.dumps(response.json(), indent=2), "Resource Details", allure.attachment_type.JSON)

        with allure.step("Verify resource details"):
            assert response.status_code == 200
            data = response.json()["data"]
            assert data["id"] == 2
            assert data["name"] == "fuchsia rose"
            assert data["year"] == 2001
            assert data["color"] == "#C74375"
            assert data["pantone_value"] == "17-2031"