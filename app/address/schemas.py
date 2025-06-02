from pydantic import BaseModel, constr
from typing import Optional, Annotated
from pydantic import field_validator


class AddressBase(BaseModel):
    street: Annotated[str, constr(strip_whitespace=True, min_length=1)]
    city: Annotated[str, constr(strip_whitespace=True, min_length=1)]
    state: Annotated[str, constr(strip_whitespace=True, min_length=1)]
    country: Annotated[str, constr(strip_whitespace=True, min_length=1)]
    postal_code: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1)]] = None
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def latitude_range(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def longitude_range(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1)]] = None
    city: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1)]] = None
    state: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1)]] = None
    country: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1)]] = None
    postal_code: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1)]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("latitude")
    @classmethod
    def latitude_range(cls, v):
        if v is not None and not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def longitude_range(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressOut(AddressBase):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True
