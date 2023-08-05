import json
from datetime import datetime

import pytest
import responses
from pydantic import SecretStr
from responses import matchers

from apinator_databricks.common import DatabricksContext
from apinator_databricks.unity_catalog import DatabricksUnityCatalogApi, uc_model


@pytest.fixture
def databricks_context() -> DatabricksContext:
    return DatabricksContext(
        access_token=SecretStr("TOKEN"),
        account="account",
    )


@pytest.fixture
def uc_api(databricks_context) -> DatabricksUnityCatalogApi:
    return DatabricksUnityCatalogApi(context=databricks_context)


@responses.activate
def test_api_basically_works(uc_api):
    sample_obj = uc_model.Share(
        name="test-share",
        owner="owner",
        full_name="test-share",
        objects=[],
        created_at=datetime.now(),
        created_by="test-user",
        updated_at=datetime.now(),
        updated_by="test-user",
        securable_kind="",
        securable_type="",
    )
    responses.get(
        "https://account.cloud.databricks.com/api/2.1/unity-catalog/shares/test-share/?include_shared_data=true",
        json=json.loads(sample_obj.json()),
        match=[matchers.header_matcher({"Authorization": "Bearer TOKEN"})],
    )

    returned_share = uc_api.datashares.retrieve(id=sample_obj.name)
    assert returned_share == sample_obj

    returned_share = uc_api.datashares.retrieve(sample_obj.name)
    assert returned_share == sample_obj
