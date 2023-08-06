import enum
import uuid
from datetime import datetime
from typing import Optional, List

from apinator.common import StrictBaseModel
from pydantic import Json, BaseModel

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


class Privilege(str, enum.Enum):
    READ_PRIVATE_FILES = "READ_PRIVATE_FILES"
    WRITE_PRIVATE_FILES = "WRITE_PRIVATE_FILES"
    CREATE = "CREATE"
    USAGE = "USAGE"
    USE_CATALOG = "USE_CATALOG"
    USE_SCHEMA = "USE_SCHEMA"
    CREATE_SCHEMA = "CREATE_SCHEMA"
    CREATE_VIEW = "CREATE_VIEW"
    CREATE_EXTERNAL_TABLE = "CREATE_EXTERNAL_TABLE"
    CREATE_MATERIALIZED_VIEW = "CREATE_MATERIALIZED_VIEW"
    CREATE_FUNCTION = "CREATE_FUNCTION"
    CREATE_CATALOG = "CREATE_CATALOG"
    CREATE_MANAGED_STORAGE = "CREATE_MANAGED_STORAGE"
    CREATE_EXTERNAL_LOCATION = "CREATE_EXTERNAL_LOCATION"
    CREATE_STORAGE_CREDENTIAL = "CREATE_STORAGE_CREDENTIAL"
    CREATE_SHARE = "CREATE_SHARE"
    CREATE_RECIPIENT = "CREATE_RECIPIENT"
    CREATE_PROVIDER = "CREATE_PROVIDER"
    USE_SHARE = "USE_SHARE"
    USE_RECIPIENT = "USE_RECIPIENT"
    USE_PROVIDER = "USE_PROVIDER"
    SET_SHARE_PERMISSION = "SET_SHARE_PERMISSION"
    SELECT = "SELECT"
    MODIFY = "MODIFY"
    REFRESH = "REFRESH"
    EXECUTE = "EXECUTE"
    READ_FILES = "READ_FILES"
    WRITE_FILES = "WRITE_FILES"
    CREATE_TABLE = "CREATE_TABLE"
    ALL_PRIVILEGES = "ALL_PRIVILEGES"


class SharePermissionPrivilege(StrictBaseModel):
    principal: str
    privileges: List[Privilege]


class SharePermissions(StrictBaseModel):
    privilege_assignments: List[SharePermissionPrivilege] = []


class SharePermissionChange(StrictBaseModel):
    add: List[Privilege]
    remove: List[Privilege]
    principal: str


class SharePermissionChanges(StrictBaseModel):
    changes: List[SharePermissionChange]
