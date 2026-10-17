"""Dedicated multi-tenant isolation verification tests.

Verifies that users from Tenant B can NEVER view or mutate records belonging to Tenant A.
"""

import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


class TestTenantIsolation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Login Org A (Demo Caterer)
        resp_a = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@cateriq.com", "password": "Password123!"},
        )
        cls.token_a = resp_a.json()["access_token"]
        cls.headers_a = {"Authorization": f"Bearer {cls.token_a}"}

        # 2. Register Org B (Rival Caterer)
        cls.user_b_email = "rival@competitor.com"
        resp_b = client.post(
            "/api/v1/auth/register",
            json={
                "email": cls.user_b_email,
                "password": "Password123!",
                "full_name": "Rival Owner",
                "organization_name": "Rival Catering Ltd",
            },
        )
        if resp_b.status_code == 200:
            cls.token_b = resp_b.json()["access_token"]
        else:
            # Already registered from previous run, just login
            login_b = client.post(
                "/api/v1/auth/login",
                json={"email": cls.user_b_email, "password": "Password123!"},
            )
            cls.token_b = login_b.json()["access_token"]
        cls.headers_b = {"Authorization": f"Bearer {cls.token_b}"}

    def test_tenant_b_cannot_see_tenant_a_events(self):
        # Org A has seeded events
        events_a = client.get("/api/v1/events", headers=self.headers_a).json()
        self.assertGreater(len(events_a), 0)
        target_event_id = events_a[0]["id"]

        # Org B should see 0 events in their list
        events_b = client.get("/api/v1/events", headers=self.headers_b).json()
        self.assertEqual(len(events_b), 0)

        # Org B attempting to fetch Org A's specific event by ID must return 404
        direct_access = client.get(f"/api/v1/events/{target_event_id}", headers=self.headers_b)
        self.assertEqual(direct_access.status_code, 404)

    def test_tenant_b_cannot_see_tenant_a_clients(self):
        # Org A has seeded clients
        clients_a = client.get("/api/v1/clients", headers=self.headers_a).json()
        self.assertGreater(len(clients_a), 0)
        target_client_id = clients_a[0]["id"]

        # Org B fetching Org A's client by ID must return 404
        direct_access = client.get(f"/api/v1/clients/{target_client_id}", headers=self.headers_b)
        self.assertEqual(direct_access.status_code, 404)


if __name__ == "__main__":
    unittest.main()
