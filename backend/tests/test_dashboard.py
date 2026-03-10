"""Tests for the /api/dashboard endpoint."""

import pytest


class TestDashboard:
    """GET /api/dashboard"""

    async def test_returns_200_with_expected_shape(self, client):
        resp = await client.get("/api/dashboard")
        assert resp.status_code == 200
        body = resp.json()

        # Top-level scalar metrics
        assert "total_transcripts" in body
        assert "total_decisions" in body
        assert "open_actions" in body
        assert "critical_threads" in body
        assert isinstance(body["total_transcripts"], int)
        assert isinstance(body["total_decisions"], int)

        # Projects list
        assert "projects" in body
        assert isinstance(body["projects"], list)

        # Activity feed
        assert "recent_activity" in body
        assert isinstance(body["recent_activity"], list)

        # Needs attention
        assert "needs_attention" in body
        assert isinstance(body["needs_attention"], list)

        # Stakeholder engagement
        assert "stakeholder_engagement" in body
        assert isinstance(body["stakeholder_engagement"], list)

        # Programme status
        assert "programme_status" in body
        ps = body["programme_status"]
        assert "narrative" in ps
        assert ps["health_rag"] in ("green", "amber", "red")
        assert "open_actions" in ps
        assert "overdue_count" in ps
        assert "critical_risks" in ps

        # KPI data
        assert "kpi" in body
        kpi = body["kpi"]
        assert "total_transcripts" in kpi
        assert "weekly_transcript_counts" in kpi
        assert isinstance(kpi["weekly_transcript_counts"], list)

        # Insights
        assert "insights" in body
        insights = body["insights"]
        assert "action_completion_rate" in insights
        assert "decision_velocity" in insights

    async def test_empty_db_returns_zero_counts(self, client):
        resp = await client.get("/api/dashboard")
        body = resp.json()
        assert body["total_transcripts"] == 0
        assert body["total_decisions"] == 0
        assert body["open_actions"] == 0
        assert body["critical_threads"] == 0
