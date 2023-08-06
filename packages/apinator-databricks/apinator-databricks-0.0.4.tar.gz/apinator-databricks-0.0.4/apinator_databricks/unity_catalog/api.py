from apinator import EndpointGroup, EndpointAction

from .._common.api import DatabricksApi, DatabricksSubApi
from . import model


class DatabricksUnityCatalogApi(DatabricksApi):
    sub_api = DatabricksSubApi(prefix="unity-catalog", version="2.1")

    datashares = EndpointGroup(
        "/shares",
        actions=[
            EndpointAction.list(model.ShareList),
            EndpointAction.retrieve(
                model.Share,
                default_query={"include_shared_data": "true"},
            ),
            EndpointAction.create(model.Share),
            EndpointAction.update(model.Share),
            EndpointAction.partial_update(model.Share),
            EndpointAction.destroy(),
            EndpointAction(
                action_name="get_permissions",
                method="GET",
                url="/{id}/permissions",
                response_model=model.SharePermissions,
                arg_names=["id"],
            ),
            EndpointAction(
                action_name="update_permissions",
                method="PATCH",
                url="/{id}/permissions",
                body_model=model.SharePermissionChanges,
                arg_names=["id"],
            ),
        ],
    )

    catalogs = EndpointGroup(
        "/catalogs",
        actions=[
            EndpointAction.list(model.CatalogList),
            EndpointAction.retrieve(model.Catalog),
            EndpointAction.head(),
        ],
    )

    schemas = EndpointGroup(
        "/schemas",
        actions=[
            EndpointAction(
                action_name="list",
                url="/schemas",
                arg_names=["catalog_name"],
                response_model=model.SchemaList,
                default_query={
                    "catalog_name": None,
                },
            ),
            EndpointAction.retrieve(model.Schema),
            EndpointAction.create(model.Schema),
        ],
    )

    tables = EndpointGroup(
        "/tables",
        actions=[
            EndpointAction(
                action_name="list",
                arg_names=["catalog_name", "schema_name"],
                response_model=model.SchemaList,
                default_query={
                    "catalog_name": None,
                    "schema_name": None,
                    "include_delta_metadata": "true",
                },
            ),
            EndpointAction.retrieve(model.Table),
            EndpointAction.head(),
        ],
    )
