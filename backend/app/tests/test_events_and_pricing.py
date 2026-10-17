"""Events, pricing calculations, proposal workflow, and payment idempotency tests."""

from datetime import date, timedelta
import unittest
import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


class TestEventsAndPricing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@cateriq.com", "password": "Password123!"},
        )
        cls.token = resp.json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    def test_event_creation_and_calculation(self):
        # 1. Fetch available clients and menu items
        clients = client.get("/api/v1/clients", headers=self.headers).json()
        menu_items = client.get("/api/v1/menu-items", headers=self.headers).json()

        self.assertGreater(len(clients), 0)
        self.assertGreater(len(menu_items), 0)

        c_id = clients[0]["id"]
        m1 = menu_items[0]
        m2 = menu_items[1]

        # 2. Create Event with 50 headcount
        ev_payload = {
            "client_id": c_id,
            "title": "Corporate Annual Dinner",
            "event_date": str(date.today() + timedelta(days=15)),
            "headcount": 50,
            "items": [
                {"menu_item_id": m1["id"], "quantity": 1},
                {"menu_item_id": m2["id"], "quantity": 1},
            ],
        }
        res = client.post("/api/v1/events", json=ev_payload, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        ev_data = res.json()

        expected_rev = round((m1["price_per_head"] + m2["price_per_head"]) * 50, 2)
        expected_cost = round((m1["cost_per_head"] + m2["cost_per_head"]) * 50, 2)
        expected_profit = round(expected_rev - expected_cost, 2)

        self.assertEqual(ev_data["total_revenue"], expected_rev)
        self.assertEqual(ev_data["total_cost"], expected_cost)
        self.assertEqual(ev_data["projected_profit"], expected_profit)
        self.assertEqual(ev_data["status"], "lead")

        # 3. Generate Proposal for this event
        prop_res = client.post(
            f"/api/v1/events/{ev_data['id']}/proposals",
            json={"deposit_percent": 30.0},
            headers=self.headers,
        )
        self.assertEqual(prop_res.status_code, 200)
        prop_data = prop_res.json()
        token = prop_data["public_token"]

        # 4. Public client view (without auth headers)
        pub_res = client.get(f"/api/v1/p/{token}")
        self.assertEqual(pub_res.status_code, 200)
        self.assertEqual(pub_res.json()["status"], "sent")

        # 5. Public client approves proposal
        appr_res = client.post(f"/api/v1/p/{token}/approve")
        self.assertEqual(appr_res.status_code, 200)
        inv_id = appr_res.json()["invoice_id"]

        # 6. Test Payment and Idempotency
        evt_key = f"evt_test_{uuid.uuid4().hex[:10]}"
        wh_payload = {
            "id": evt_key,
            "type": "checkout.session.completed",
            "data": {"object": {"metadata": {"invoice_id": inv_id}}},
        }

        # First webhook call: should process
        wh1 = client.post("/api/v1/webhooks/stripe", json=wh_payload)
        self.assertEqual(wh1.status_code, 200)
        self.assertEqual(wh1.json()["status"], "processed")

        # Replaying identical webhook: must be recognized as already processed
        wh2 = client.post("/api/v1/webhooks/stripe", json=wh_payload)
        self.assertEqual(wh2.status_code, 200)
        self.assertEqual(wh2.json()["result"]["status"], "already_processed")


if __name__ == "__main__":
    unittest.main()
