from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.search import SearchResponse, SearchResult

router = APIRouter(tags=["search"])

SEARCH_QUERIES = {
    "transcripts": """
        SELECT 'transcript' AS type, id, title,
               ts_headline('english', content, query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM transcripts, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "summaries": """
        SELECT 'summary' AS type, id, filename AS title,
               ts_headline('english', content, query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM summaries, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "weekly_reports": """
        SELECT 'weekly_report' AS type, id, title,
               ts_headline('english', content, query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM weekly_reports, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "stakeholders": """
        SELECT 'stakeholder' AS type, id, name AS title,
               ts_headline('english', coalesce(role,'') || ' ' || coalesce(concerns,'') || ' ' || coalesce(key_contributions,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM stakeholders, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "decisions": """
        SELECT 'decision' AS type, id,
               'Decision #' || number AS title,
               ts_headline('english', decision || ' ' || coalesce(rationale,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM decisions, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "open_threads": """
        SELECT 'open_thread' AS type, id, title,
               ts_headline('english', coalesce(context,'') || ' ' || coalesce(question,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM open_threads, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "tasks": """
        SELECT 'task' AS type, id,
               coalesce(title, 'Task ' || number) AS title,
               ts_headline('english', coalesce(title,'') || ' ' || coalesce(description,'') || ' ' || coalesce(context,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM tasks, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "glossary": """
        SELECT 'glossary' AS type, id, term AS title,
               ts_headline('english', definition, query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM glossary_entries, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "documents": """
        SELECT 'document' AS type, id, title,
               ts_headline('english', content, query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(search_vector, query) AS score
        FROM documents, plainto_tsquery('english', :q) query
        WHERE search_vector @@ query
    """,
    "topic_signals": """
        SELECT 'topic_signal' AS type, id, topic AS title,
               ts_headline('english', coalesce(topic,'') || ' ' || coalesce(key_quote,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(to_tsvector('english', coalesce(topic,'') || ' ' || coalesce(key_quote,'')), query) AS score
        FROM topic_signals, plainto_tsquery('english', :q) query
        WHERE to_tsvector('english', coalesce(topic,'') || ' ' || coalesce(key_quote,'')) @@ query
    """,
    "contradictions": """
        SELECT 'contradiction' AS type, id,
               coalesce(person, 'Unknown') || ' - ' || contradiction_type AS title,
               ts_headline('english', coalesce(person,'') || ' ' || coalesce(statement_a,'') || ' ' || coalesce(statement_b,'') || ' ' || coalesce(gap_description,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(to_tsvector('english', coalesce(person,'') || ' ' || coalesce(statement_a,'') || ' ' || coalesce(statement_b,'') || ' ' || coalesce(gap_description,'')), query) AS score
        FROM contradictions, plainto_tsquery('english', :q) query
        WHERE to_tsvector('english', coalesce(person,'') || ' ' || coalesce(statement_a,'') || ' ' || coalesce(statement_b,'') || ' ' || coalesce(gap_description,'')) @@ query
    """,
    "risk_entries": """
        SELECT 'risk_entry' AS type, id, title,
               ts_headline('english', coalesce(title,'') || ' ' || coalesce(description,'') || ' ' || coalesce(owner,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(to_tsvector('english', coalesce(title,'') || ' ' || coalesce(description,'') || ' ' || coalesce(owner,'')), query) AS score
        FROM risk_entries, plainto_tsquery('english', :q) query
        WHERE to_tsvector('english', coalesce(title,'') || ' ' || coalesce(description,'') || ' ' || coalesce(owner,'')) @@ query
    """,
    "meeting_scores": """
        SELECT 'meeting_score' AS type, id, meeting_title AS title,
               ts_headline('english', coalesce(meeting_title,'') || ' ' || coalesce(recommendations,''), query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(to_tsvector('english', coalesce(meeting_title,'') || ' ' || coalesce(recommendations,'')), query) AS score
        FROM meeting_scores, plainto_tsquery('english', :q) query
        WHERE to_tsvector('english', coalesce(meeting_title,'') || ' ' || coalesce(recommendations,'')) @@ query
    """,
    "project_summaries": """
        SELECT 'project_summary' AS type, id,
               'Project Summary' AS title,
               ts_headline('english', content, query, 'MaxWords=40, MinWords=20') AS snippet,
               ts_rank(to_tsvector('english', content), query) AS score
        FROM project_summaries, plainto_tsquery('english', :q) query
        WHERE to_tsvector('english', content) @@ query
    """,
}

URL_PREFIXES = {
    "transcript": "/transcripts",
    "summary": "/summaries",
    "weekly_report": "/weekly-reports",
    "stakeholder": "/stakeholders",
    "decision": "/decisions",
    "open_thread": "/open-threads",
    "task": "/tasks",
    "glossary": "/glossary",
    "document": "/documents",
    "topic_signal": "/topic-signals",
    "contradiction": "/contradictions",
    "risk_entry": "/risk-entries",
    "meeting_score": "/meeting-scores",
    "project_summary": "/project-summaries",
}


@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1),
    types: str = Query("all"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if types == "all":
        selected_types = list(SEARCH_QUERIES.keys())
    else:
        selected_types = [t.strip() for t in types.split(",") if t.strip() in SEARCH_QUERIES]
        if not selected_types:
            selected_types = list(SEARCH_QUERIES.keys())

    union_parts = [SEARCH_QUERIES[t] for t in selected_types]
    union_sql = " UNION ALL ".join(union_parts)
    full_sql = f"SELECT * FROM ({union_sql}) combined ORDER BY score DESC LIMIT :limit"

    result = await db.execute(text(full_sql), {"q": q, "limit": limit})
    rows = result.all()

    results = [
        SearchResult(
            type=row.type,
            id=row.id,
            title=row.title or "",
            snippet=row.snippet or "",
            score=float(row.score),
            url=f"{URL_PREFIXES.get(row.type, '')}/{row.id}",
        )
        for row in rows
    ]

    return SearchResponse(query=q, total=len(results), results=results)
