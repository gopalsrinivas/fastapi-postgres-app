from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime


class ItemBase(BaseModel):
    name: str
    description: str
    price: float
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        from_attributes = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True


class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class SuccessResponse(BaseModel):
    message: str
    data: Optional[Union[Item, List[Item]]] = None
    response_code: int


class ErrorResponse(BaseModel):
    message: str
    response_code: int


class APIResponse(BaseModel):
    success: Optional[SuccessResponse] = None
    error: Optional[ErrorResponse] = None
