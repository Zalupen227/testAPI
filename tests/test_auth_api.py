import pytest
import requests
import allure
import json


@allure.epic("ReqRes API")
@allure.feature("Authentication")
class TestAuthentication:

    @allure.story("User Registration")
    @allure.title("Successful user registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "auth")
    def test_successful_registration(self, base_url, api_headers):
        with allure.step("Prepare registration data"):
            payload = {
                "email": "eve.holt@reqres.in",
                "password": "pistol"
            }
            allure.attach(json.dumps(payload, indent=2), "Request Payload", allure.attachment_type.JSON)
            allure.attach(json.dumps(api_headers, indent=2), "Request Headers", allure.attachment_type.JSON)

        with allure.step("Send POST request to /register"):
            response = requests.post(
                f"{base_url}/register",
                json=payload,
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Response Info", allure.attachment_type.TEXT)

            if response.status_code == 200:
                allure.attach(json.dumps(response.json(), indent=2), "Response Body", allure.attachment_type.JSON)
            else:
                allure.attach(json.dumps(response.json(), indent=2), "Error Response", allure.attachment_type.JSON)

        with allure.step("Verify response"):
            assert response.status_code == 200
            assert "id" in response.json()
            assert "token" in response.json()
            assert isinstance(response.json()["token"], str)

    @allure.story("User Registration")
    @allure.title("Failed registration with missing password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_missing_password(self, base_url, api_headers):
        with allure.step("Prepare invalid registration data"):
            payload = {
                "email": "eve.holt@reqres.in"
                # password is missing
            }
            allure.attach(json.dumps(payload, indent=2), "Request Payload", allure.attachment_type.JSON)

        with allure.step("Send POST request to /register"):
            response = requests.post(
                f"{base_url}/register",
                json=payload,
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Response Info", allure.attachment_type.TEXT)
            allure.attach(json.dumps(response.json(), indent=2), "Error Response", allure.attachment_type.JSON)

        with allure.step("Verify error response"):
            assert response.status_code == 400
            assert "error" in response.json()
            assert response.json()["error"] == "Missing password"

    @allure.story("User Login")
    @allure.title("Successful user login")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, base_url, api_headers):
        with allure.step("Prepare login credentials"):
            payload = {
                "email": "eve.holt@reqres.in",
                "password": "cityslicka"
            }
            allure.attach(json.dumps(payload, indent=2), "Login Payload", allure.attachment_type.JSON)

        with allure.step("Send POST request to /login"):
            response = requests.post(
                f"{base_url}/login",
                json=payload,
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Response", allure.attachment_type.TEXT)

            if response.status_code == 200:
                allure.attach(json.dumps(response.json(), indent=2), "Login Response", allure.attachment_type.JSON)

        with allure.step("Verify login response"):
            assert response.status_code == 200
            assert "token" in response.json()
            assert len(response.json()["token"]) > 0

    @allure.story("User Login")
    @allure.title("Failed login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_failed_login(self, base_url, api_headers):
        with allure.step("Prepare invalid credentials"):
            payload = {
                "email": "nonexistent@reqres.in",
                "password": "wrongpassword"
            }
            allure.attach(json.dumps(payload, indent=2), "Invalid Credentials", allure.attachment_type.JSON)

        with allure.step("Send POST request to /login"):
            response = requests.post(
                f"{base_url}/login",
                json=payload,
                headers=api_headers
            )
            allure.attach(f"Status Code: {response.status_code}", "Response Info", allure.attachment_type.TEXT)
            allure.attach(json.dumps(response.json(), indent=2), "Error Response", allure.attachment_type.JSON)

        with allure.step("Verify error message"):
            assert response.status_code == 400
            assert "error" in response.json()