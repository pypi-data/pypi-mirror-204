from apinator import EndpointGroup, EndpointAction

from . import model
from .._common.api import DatabricksApi, DatabricksSubApi


class DatabricksMarketplaceProviderApi(DatabricksApi):
    sub_api = DatabricksSubApi(prefix="marketplace-provider", version="2.0")

    listings = EndpointGroup(
        "/listings",
        actions=[
            EndpointAction.list(model.ListingList),
            EndpointAction.retrieve(model.Listing),
            EndpointAction.create(model.Listing),
            EndpointAction.update(model.Listing),
            EndpointAction.partial_update(model.Listing),
            EndpointAction.destroy(),
        ],
    )
