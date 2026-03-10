from pydantic import BaseModel


class GlossaryEntrySchema(BaseModel):
    id: int
    term: str
    definition: str
    category: str
    aliases: list[str]
    is_manual: bool = False


# GlossaryGrouped is represented as dict[str, list[GlossaryEntrySchema]]
# in API responses — no separate Pydantic model needed.
GlossaryGrouped = dict[str, list[GlossaryEntrySchema]]


class GlossaryCreate(BaseModel):
    term: str
    definition: str
    category: str = "Uncategorized"


class GlossaryUpdate(BaseModel):
    definition: str | None = None
    category: str | None = None
