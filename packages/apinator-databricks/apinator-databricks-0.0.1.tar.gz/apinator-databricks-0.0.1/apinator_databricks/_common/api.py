from apinator import JsonApiBase
from pydantic import BaseModel, constr, validate_arguments

from apinator_databricks.common import DatabricksContext


class DatabricksSubApi(BaseModel):
    version: constr(regex=r"\d+\.\d+")
    prefix: constr(regex=r"^[a-z0-9_-]+$")


class DatabricksApi(JsonApiBase):
    context_type = DatabricksContext
    sub_api: DatabricksSubApi = None

    @validate_arguments
    def __init__(
        self,
        context: DatabricksContext,
    ):
        self.context = context
        path_prefix = f"api/{self.sub_api.version}/{self.sub_api.prefix}"
        host = f"{context.account}.cloud.databricks.com"
        super().__init__(path_prefix=path_prefix, host=host, append_trailing_slash=True)

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.context.access_token.get_secret_value()}"
        }
