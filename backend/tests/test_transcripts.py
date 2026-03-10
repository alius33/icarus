"""Tests for the /api/transcripts endpoints."""

import pytest


class TestListTranscripts:
    """GET /api/transcripts"""

    async def test_returns_empty_list(self, client):
        resp = await client.get("/api/transcripts")
        assert resp.status_code == 200
        body = resp.json()
        assert body["items"] == []
        assert body["total"] == 0
        assert body["page"] == 1


class TestGetTranscript:
    """GET /api/transcripts/{id}"""

    async def test_nonexistent_returns_404(self, client):
        resp = await client.get("/api/transcripts/9999")
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()
