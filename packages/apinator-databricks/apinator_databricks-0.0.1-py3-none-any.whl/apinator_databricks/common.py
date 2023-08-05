from typing import Union

from pydantic import BaseModel, SecretStr, constr


class DatabricksContext(BaseModel):
    access_token: Union[SecretStr, str]
    account: constr(regex=r"^[a-z0-9_-]+$")
