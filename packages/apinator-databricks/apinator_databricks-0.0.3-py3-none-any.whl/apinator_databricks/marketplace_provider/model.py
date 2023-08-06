import enum
import uuid
from datetime import datetime
from typing import Optional, List

from apinator.common import StrictBaseModel
from pydantic import Field, BaseModel, validator


class ShareType(str, enum.Enum):
    SAMPLE = "SAMPLE"
    FULL = "FULL"


class ListingType(str, enum.Enum):
    STANDARD = "STANDARD"
    PERSONALIZED = "PERSONALIZED"


class ListingStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    SUSPENDED = "SUSPENDED"


class ListingShare(StrictBaseModel):
    name: str
    type: ShareType


class ListingSetting(StrictBaseModel):
    visibility: str = "PUBLIC"  # deprecated


class ListingSummary(StrictBaseModel):
    name: str
    subtitle: str
    status: ListingStatus
    provider_info: dict = None  # deprecated
    share: Optional[ListingShare] = None
    setting: Optional[ListingSetting] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_by_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_by_id: Optional[int] = None
    categories: List[str] = []
    listing_type: ListingType = Field(alias="listingType")
    provider_id: uuid.UUID

    class Config:
        allow_population_by_field_name = True


class EmbeddedNotebookFileParent(StrictBaseModel):
    parent_id: uuid.UUID
    file_parent_type: str


class EmbeddedNotebookFileInfo(StrictBaseModel):
    id: uuid.UUID
    display_name: Optional[str] = None
    marketplace_file_type: str
    file_parent: EmbeddedNotebookFileParent
    mime_type: str
    download_link: str
    created_at: datetime
    updated_at: datetime


class ListingDetail(StrictBaseModel):
    description: str
    documentation_link: str = ""
    terms_of_service: str = ""
    contact_email: str = ""
    support_link: str = ""
    privacy_policy_link: str = ""
    embedded_notebook_file_infos: List[EmbeddedNotebookFileInfo] = []


class Listing(StrictBaseModel):
    id: Optional[uuid.UUID] = None
    summary: ListingSummary
    detail: ListingDetail
    deployment_name: str


class ListingList(BaseModel):
    listings: List[Listing] = []
