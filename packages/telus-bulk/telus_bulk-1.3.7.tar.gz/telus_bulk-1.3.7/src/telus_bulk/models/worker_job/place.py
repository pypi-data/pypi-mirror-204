from __future__ import annotations

from typing import Optional, Literal, List

from fastapi_camelcase import CamelModel
from pydantic import Field
from telus_bulk.models.ams.coordinate import Coordinate
from telus_bulk.models.clli import Clli


class Place(CamelModel):
    id: str
    index: Optional[int] = None
    role: Optional[str] = None
    _type: str = Field(alias="@type", default="GeographicAddress")


class PlaceAMS(Place):
    city: Optional[str] = None
    city_aliases: Optional[List[str]] = None
    country: Literal["USA", "CAN"] = "CAN"
    postcode: Optional[str] = None
    state_or_province: Optional[str] = None
    street_dir: Optional[str] = None
    street_name: Optional[str] = None
    street_nr: Optional[str] = None
    street_type: Optional[str] = None
    street_type_suffix: Optional[str] = None
    street_type_prefix: Optional[str] = None
    street_number_prefix: Optional[str] = None
    street_number_suffix: Optional[str] = None
    dir_prefix: Optional[str] = None
    dir_suffix: Optional[str] = None
    floor: Optional[str] = None
    unit: Optional[str] = None
    address_type: Optional[str] = None
    coordinate: Optional[Coordinate] = None
    clli: Optional[Clli] = Field(default=None)
    name: Optional[str] = None
