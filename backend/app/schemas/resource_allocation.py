from pydantic import BaseModel


class AllocationEntry(BaseModel):
    project: str
    percentage: int


class ResourceAllocationSchema(BaseModel):
    id: int
    person_name: str
    role: str | None = None
    allocations: list[AllocationEntry] = []
    capacity_status: str = "available"
    notes: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class ResourceAllocationCreate(BaseModel):
    person_name: str
    role: str | None = None
    allocations: list[AllocationEntry] = []
    capacity_status: str = "available"
    notes: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class ResourceAllocationUpdate(BaseModel):
    person_name: str | None = None
    role: str | None = None
    allocations: list[AllocationEntry] | None = None
    capacity_status: str | None = None
    notes: str | None = None
    start_date: str | None = None
    end_date: str | None = None
