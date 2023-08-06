from typing import Optional, Union
from fastapi_camelcase import CamelModel
from telus_bulk.models.clli import Clli


class ReportAddress(CamelModel):
    location_id: str
    csq_id: Optional[str] = ""
    index: Optional[int] = None
    address: Optional[str] = ""
    best_match_address: Optional[str] = ""
    qual_status: Optional[str] = ""
    carrier: Optional[str] = ""
    best_offer: Optional[str] = ""
    speed: Optional[str] = ""
    technology: Optional[str] = ""
    region_clli: Optional[Clli | str] = None
    nearest_distance: Optional[str] = ""
    location_type: Optional[str] = ""
    comments: Optional[str] = ""
    has_incomplete_items: Optional[bool] = False


class ReportAddressUpdateDto(CamelModel):
    address: Optional[str]
    best_match_address: Optional[str] = ""
    qual_status: Optional[str] = ""
    carrier: Optional[str] = ""
    best_offer: Optional[str] = ""
    speed: Optional[str] = ""
    technology: Optional[str] = ""
    region_clli: Optional[Clli | str] = None
    nearest_distance: Optional[str] = ""
    location_type: Optional[str] = ""
    comments: Optional[str] = ""
    has_incomplete_items: Optional[bool] = False
