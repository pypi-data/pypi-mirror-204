from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import pytest

from great_expectations.core.yaml_handler import YAMLHandler
from great_expectations.data_context import CloudDataContext, FileDataContext
from tests.datasource.fluent.conftest import (
    FAKE_ORG_ID,
    GX_CLOUD_MOCK_BASE_URL,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from responses import RequestsMock

    from great_expectations.datasource.fluent import SqliteDatasource

# apply markers to entire test module
pytestmark = [pytest.mark.integration]


yaml = YAMLHandler()


@pytest.mark.cloud
def test_add_fluent_datasource_are_persisted(
    cloud_api_fake: RequestsMock,
    empty_cloud_context_fluent: CloudDataContext,
    db_file: pathlib.Path,
    mocker: MockerFixture,
):
    context = empty_cloud_context_fluent
    set_spy = mocker.spy(context._datasource_store, "set")

    datasource_name = "save_ds_test"

    datasource = context.sources.add_sqlite(
        name=datasource_name, connection_string=f"sqlite:///{db_file}"
    )

    assert datasource.id
    assert set_spy.call_count == 1
    cloud_api_fake.assert_call_count(
        f"{GX_CLOUD_MOCK_BASE_URL}/organizations/{FAKE_ORG_ID}/datasources",
        1,
    )


@pytest.mark.cloud
def test_add_fluent_datasource_are_persisted_without_duplicates(
    empty_file_context: FileDataContext,
    db_file: pathlib.Path,
):
    context = empty_file_context
    datasource_name = "save_ds_test"

    context.sources.add_sqlite(
        name=datasource_name, connection_string=f"sqlite:///{db_file}"
    )

    yaml_path = pathlib.Path(context.root_directory, context.GX_YML)
    assert yaml_path.exists()
    yaml_dict: dict = yaml.load(yaml_path.read_text())
    assert datasource_name in yaml_dict["fluent_datasources"]
    assert datasource_name not in yaml_dict["datasources"]


@pytest.mark.cloud
@pytest.mark.xfail(reason="Fluent logic attempts to delete before updating")
def test_context_add_or_update_datasource(
    cloud_api_fake: RequestsMock,
    empty_contexts: CloudDataContext | FileDataContext,
    db_file: pathlib.Path,
):
    context = empty_contexts

    datasource: SqliteDatasource = context.sources.add_sqlite(
        name="save_ds_test", connection_string=f"sqlite:///{db_file}"
    )

    assert datasource.connection_string == f"sqlite:///{db_file}"

    # modify the datasource
    datasource.connection_string = "sqlite:///"  # type: ignore[assignment]
    context.sources.add_or_update_sqlite(datasource)

    if isinstance(empty_contexts, CloudDataContext):
        # TODO: adjust call counts as needed
        cloud_api_fake.assert_call_count(
            f"{GX_CLOUD_MOCK_BASE_URL}/organizations/{FAKE_ORG_ID}/datasources",
            1,
        )
        cloud_api_fake.assert_call_count(
            f"{GX_CLOUD_MOCK_BASE_URL}/organizations/{FAKE_ORG_ID}/datasources{datasource.id}",
            1,
        )


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
