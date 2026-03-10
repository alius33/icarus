"""Tests for the /api/stakeholders endpoints."""

import pytest


class TestListStakeholders:
    """GET /api/stakeholders"""

    async def test_returns_empty_list(self, client):
        resp = await client.get("/api/stakeholders")
        assert resp.status_code == 200
        assert resp.json() == []


class TestCreateStakeholder:
    """POST /api/stakeholders"""

    async def test_creates_stakeholder(self, client):
        payload = {"name": "Alice Tester", "role": "QA Lead", "tier": 2}
        resp = await client.post("/api/stakeholders", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "Alice Tester"
        assert body["role"] == "QA Lead"
        assert body["tier"] == 2
        assert body["is_manual"] is True
        assert body["mention_count"] == 0
        assert "id" in body


class TestGetStakeholder:
    """GET /api/stakeholders/{id}"""

    async def test_returns_created_stakeholder(self, client):
        # Create first
        create_resp = await client.post(
            "/api/stakeholders",
            json={"name": "Bob Builder", "role": "Architect", "tier": 1},
        )
        stakeholder_id = create_resp.json()["id"]

        # Fetch
        resp = await client.get(f"/api/stakeholders/{stakeholder_id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == stakeholder_id
        assert body["name"] == "Bob Builder"
        assert body["role"] == "Architect"
        assert body["tier"] == 1

    async def test_nonexistent_returns_404(self, client):
        resp = await client.get("/api/stakeholders/9999")
        assert resp.status_code == 404


class TestDeleteStakeholder:
    """DELETE /api/stakeholders/{id}"""

    async def test_deletes_stakeholder(self, client):
        # Create
        create_resp = await client.post(
            "/api/stakeholders",
            json={"name": "Charlie Temp", "role": "Intern", "tier": 3},
        )
        stakeholder_id = create_resp.json()["id"]

        # Delete
        del_resp = await client.delete(f"/api/stakeholders/{stakeholder_id}")
        assert del_resp.status_code == 200
        assert del_resp.json()["ok"] is True

        # Verify gone
        get_resp = await client.get(f"/api/stakeholders/{stakeholder_id}")
        assert get_resp.status_code == 404

    async def test_delete_nonexistent_returns_404(self, client):
        resp = await client.delete("/api/stakeholders/9999")
        assert resp.status_code == 404
