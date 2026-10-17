"""Authentication and token validation tests."""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


class TestAuth(unittest.TestCase):
    def test_login_success(self):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@cateriq.com", "password": "Password123!"},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["role"], "owner")
        self.assertEqual(data["email"], "demo@cateriq.com")

    def test_login_wrong_password(self):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@cateriq.com", "password": "WrongPassword!"},
        )
        self.assertEqual(resp.status_code, 401)

    def test_get_me_unauthorized(self):
        resp = client.get("/api/v1/auth/me")
        self.assertEqual(resp.status_code, 401)

    def test_get_me_authorized(self):
        login_resp = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@cateriq.com", "password": "Password123!"},
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["email"], "demo@cateriq.com")


if __name__ == "__main__":
    unittest.main()
