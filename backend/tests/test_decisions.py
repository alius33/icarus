"""Tests for the /api/decisions endpoints."""

import pytest


class TestListDecisions:
    """GET /api/decisions"""

    async def test_returns_empty_list(self, client):
        resp = await client.get("/api/decisions")
        assert resp.status_code == 200
        assert resp.json() == []


class TestCreateDecision:
    """POST /api/decisions"""

    async def test_creates_decision(self, client):
        payload = {
            "decision": "Adopt pytest for backend testing",
            "rationale": "Faster feedback loop",
            "key_people": ["Alice", "Bob"],
            "date": "2026-03-10",
        }
        resp = await client.post("/api/decisions", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body["description"] == "Adopt pytest for backend testing"
        assert body["date"] == "2026-03-10"
        assert body["status"] == "recorded"
        assert body["is_manual"] is True
        assert "id" in body


class TestUpdateDecision:
    """PATCH /api/decisions/{id}"""

    async def test_updates_decision(self, client):
        # Create
        create_resp = await client.post(
            "/api/decisions",
            json={"decision": "Original decision text", "date": "2026-03-01"},
        )
        decision_id = create_resp.json()["id"]

        # Update
        patch_resp = await client.patch(
            f"/api/decisions/{decision_id}",
            json={"decision": "Updated decision text", "rationale": "New rationale"},
        )
        assert patch_resp.status_code == 200
        body = patch_resp.json()
        assert body["description"] == "Updated decision text"

    async def test_update_nonexistent_returns_404(self, client):
        resp = await client.patch(
            "/api/decisions/9999",
            json={"decision": "Nope"},
        )
        assert resp.status_code == 404
