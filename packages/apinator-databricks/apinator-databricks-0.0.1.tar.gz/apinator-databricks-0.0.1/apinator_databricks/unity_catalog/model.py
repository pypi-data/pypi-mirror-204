import uuid
from datetime import datetime
from typing import Optional, List

from apinator.common import StrictBaseModel
from pydantic import Json

from .._common.model import DatabricksBase


class Catalog(DatabricksBase):
    name: str
    owner: str
    comment: str
    metastore_id: uuid.UUID
    catalogue_type: Optional[str]
    isolation_mode: str
    full_name: str


class CatalogList(StrictBaseModel):
    catalogs: List[Catalog] = []


class Schema(DatabricksBase):
    name: str
    catalog_name: str
    owner: str
    comment: str
    properties: Optional[dict]
    metastore_id: uuid.UUID
    full_name: str
    catalogue_type: Optional[str]


class SchemaList(StrictBaseModel):
    schemas: List[Schema] = []


class Column(StrictBaseModel):
    name: str
    nullable: bool
    position: int
    type_json: Json[dict]
    type_name: str
    type_precision: int
    type_scale: int
    type_text: str


class Table(DatabricksBase):
    name: str
    catalog_name: str
    schema_name: str
    table_type: str
    data_source_format: Optional[str]
    columns: List[Column]
    storage_location: Optional[str]
    owner: str
    properties: dict = {}
    storage_credential_name: Optional[str]
    generation: int
    metastore_id: uuid.UUID
    full_name: str
    data_access_configuration_id: uuid.UUID
    table_id: uuid.UUID
    delta_runtime_properties_kvpairs: dict


class TableList(StrictBaseModel):
    tables: List[Table] = []


class SharedObject(StrictBaseModel):
    name: str
    data_object_type: str
    added_at: datetime
    added_by: str
    shared_as: str
    cdf_enabled: bool
    history_data_sharing_status: str
    status: str


class SharePartial(DatabricksBase):
    name: str
    owner: str
    full_name: str
    comment: str = ""


class Share(SharePartial):
    objects: Optional[
        List[SharedObject]
    ]  # Key not included if missing a query parameter


class ShareList(StrictBaseModel):
    shares: List[SharePartial] = []
