import pytest
import requests
import allure
import json


@allure.epic("ReqRes API")
@allure.feature("User Management")
class TestUsersAPI:

    @allure.story("Get Users")
    @allure.title("Get list of users")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "users")
    def test_get_users_list(self, base_url, api_headers):
        with allure.step("Send GET request to /users"):
            response = requests.get(
                f"{base_url}/users?page=2",
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Response Info", allure.attachment_type.TEXT)
            allure.attach(json.dumps(response.json(), indent=2), "Response Body", allure.attachment_type.JSON)

        with allure.step("Verify response structure"):
            assert response.status_code == 200
            data = response.json()
            assert "page" in data
            assert "per_page" in data
            assert "total" in data
            assert "data" in data
            assert isinstance(data["data"], list)

        with allure.step("Verify user data format"):
            if data["data"]:
                user = data["data"][0]
                assert "id" in user
                assert "email" in user
                assert "first_name" in user
                assert "last_name" in user
                assert "avatar" in user

    @allure.story("Get Single User")
    @allure.title("Get user by ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_user(self, base_url, api_headers):
        user_id = 2

        with allure.step(f"Send GET request to /users/{user_id}"):
            response = requests.get(
                f"{base_url}/users/{user_id}",
                headers=api_headers
            )
            allure.attach(json.dumps(response.json(), indent=2), "User Data", allure.attachment_type.JSON)

        with allure.step("Verify user details"):
            assert response.status_code == 200
            data = response.json()["data"]
            assert data["id"] == user_id
            assert data["email"] == "janet.weaver@reqres.in"
            assert data["first_name"] == "Janet"
            assert data["last_name"] == "Weaver"

    @allure.story("Get Single User")
    @allure.title("Get non-existent user")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_nonexistent_user(self, base_url, api_headers):
        with allure.step("Send GET request for non-existent user"):
            response = requests.get(
                f"{base_url}/users/23",
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Response", allure.attachment_type.TEXT)

        with allure.step("Verify 404 response"):
            assert response.status_code == 404
            assert response.json() == {}

    @allure.story("Create User")
    @allure.title("Create new user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, base_url, api_headers):
        with allure.step("Prepare user data"):
            payload = {
                "name": "morpheus",
                "job": "leader"
            }
            allure.attach(json.dumps(payload, indent=2), "Request Payload", allure.attachment_type.JSON)

        with allure.step("Send POST request to /users"):
            response = requests.post(
                f"{base_url}/users",
                json=payload,
                headers=api_headers
            )
            allure.attach(json.dumps(response.json(), indent=2), "Response", allure.attachment_type.JSON)

        with allure.step("Verify user creation"):
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == payload["name"]
            assert data["job"] == payload["job"]
            assert "id" in data
            assert "createdAt" in data

    @allure.story("Update User")
    @allure.title("Update user information")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, base_url, api_headers):
        user_id = 2

        with allure.step("Prepare update data"):
            payload = {
                "name": "morpheus",
                "job": "zion resident"
            }
            allure.attach(json.dumps(payload, indent=2), "Update Payload", allure.attachment_type.JSON)

        with allure.step(f"Send PUT request to /users/{user_id}"):
            response = requests.put(
                f"{base_url}/users/{user_id}",
                json=payload,
                headers=api_headers
            )
            allure.attach(json.dumps(response.json(), indent=2), "Update Response", allure.attachment_type.JSON)

        with allure.step("Verify update response"):
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == payload["name"]
            assert data["job"] == payload["job"]
            assert "updatedAt" in data

    @allure.story("Delete User")
    @allure.title("Delete user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user(self, base_url, api_headers):
        user_id = 2

        with allure.step(f"Send DELETE request to /users/{user_id}"):
            response = requests.delete(
                f"{base_url}/users/{user_id}",
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Delete Response", allure.attachment_type.TEXT)

        with allure.step("Verify deletion success"):
            assert response.status_code == 204
            assert response.text == ""