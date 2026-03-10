from pydantic import BaseModel


class SearchResult(BaseModel):
    type: str
    id: int
    title: str
    snippet: str
    score: float
    url: str


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResult]
