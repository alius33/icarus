from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, entity: str, id: int | str):
        super().__init__(status_code=404, detail=f"{entity} with id {id} not found")


class DuplicateError(HTTPException):
    def __init__(self, entity: str, field: str, value: str):
        super().__init__(status_code=409, detail=f"{entity} with {field} '{value}' already exists")


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "This action is not allowed"):
        super().__init__(status_code=403, detail=detail)
