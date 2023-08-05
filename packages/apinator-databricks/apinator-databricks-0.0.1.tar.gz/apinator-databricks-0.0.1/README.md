# Apinator-Databricks

`apinator` bindings for the [Databricks API](https://docs.databricks.com/api-explorer/).

## Example

```python
from apinator_databricks.common import DatabricksContext
from apinator_databricks.unity_catalog import DatabricksUnityCatalogApi, uc_model

context = DatabricksContext(
        access_token="TOKEN",  # Will be kept secret
        account="account",
    )
api = DatabricksUnityCatalogApi(context)
shares: uc_model.ShareList = api.datashares.list()
for share in shares.shares:
    assert isinstance(share, uc_model.SharePartial)  # Not necessary, pydantic guarantees this
    ...
```
