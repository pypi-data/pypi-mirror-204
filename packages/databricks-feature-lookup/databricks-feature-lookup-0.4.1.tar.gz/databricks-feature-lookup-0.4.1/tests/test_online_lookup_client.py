import os
from unittest.mock import patch

import pytest

from databricks.feature_store import online_lookup_client
from databricks.feature_store.entities.cloud import Cloud
from databricks.feature_store.entities.data_type import DataType
from databricks.feature_store.entities.online_feature_table import (
    OnlineFeatureTable,
    OnlineFeatureTableForSageMakerServing,
    PrimaryKeyDetails,
)
from databricks.feature_store.entities.online_store_for_serving import (
    CosmosDbConf,
    DynamoDbConf,
    MySqlConf,
    OnlineStoreForSageMakerServing,
    OnlineStoreForServing,
    SqlServerConf,
)
from databricks.feature_store.entities.query_mode import QueryMode
from databricks.feature_store.entities.store_type import StoreType
from databricks.feature_store.lookup_engine import (
    LookupCosmosDbEngine,
    LookupDynamoDbEngine,
    LookupMySqlEngine,
    LookupSqlServerEngine,
)


@pytest.fixture(scope="function")
def online_feature_table():
    return OnlineFeatureTable(
        feature_table_name="ft1",
        online_feature_table_name="online_ft1",
        online_store=OnlineStoreForServing(
            cloud=Cloud.AWS,
            store_type=StoreType.DYNAMODB,
            extra_configs=DynamoDbConf(region="us-east-1"),
            read_secret_prefix="READ_SECRET_PREFIX",
            creation_timestamp_ms=123,
            query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
        ),
        primary_keys=[],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )


@pytest.fixture(scope="function")
def online_feature_table_list(online_feature_table):
    return [online_feature_table]


@pytest.fixture(scope="function")
def online_feature_table_for_sagemaker():
    return OnlineFeatureTableForSageMakerServing(
        feature_table_name="ft1",
        online_feature_table_name="online_ft1",
        online_store=OnlineStoreForSageMakerServing(
            creation_timestamp_ms=123,
            extra_configs=DynamoDbConf(region="us-east-1"),
            query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
        ),
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )


@pytest.fixture(scope="function")
def online_feature_table_for_sagemaker_list(online_feature_table_for_sagemaker):
    return [online_feature_table_for_sagemaker]


@pytest.mark.parametrize(
    ("cloud", "store_type", "expected_lookup_engine"),
    [
        (Cloud.AZURE, StoreType.MYSQL, LookupMySqlEngine),
        (Cloud.AZURE, StoreType.SQL_SERVER, LookupSqlServerEngine),
        (Cloud.AWS, StoreType.MYSQL, LookupMySqlEngine),
    ],
)
@patch.dict(
    os.environ,
    {
        "READ_SECRET_PREFIX_USER": "test_user",
        "READ_SECRET_PREFIX_PASSWORD": "test_password",
    },
)
@patch(
    "databricks.feature_store.lookup_engine.LookupSqlEngine._validate_online_feature_table"
)
def test_online_lookup_client_sql_stores(
    _validate_online_feature_table, cloud, store_type, expected_lookup_engine
):
    if store_type == StoreType.MYSQL:
        extra_configs = MySqlConf(host="test_host.azure.com", port=555)
    elif store_type == StoreType.SQL_SERVER:
        extra_configs = SqlServerConf(host="test_host.azure.com", port=555)
    online_store = OnlineStoreForServing(
        store_type=store_type,
        cloud=cloud,
        extra_configs=extra_configs,
        read_secret_prefix="READ_SECRET_PREFIX",
        creation_timestamp_ms=123,
        query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
    )

    online_feature_table = OnlineFeatureTable(
        feature_table_name="ft1",
        online_feature_table_name="db1.online_ft1",
        online_store=online_store,
        primary_keys=[],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )
    lookup_client = online_lookup_client.OnlineLookupClient(
        online_feature_table, "Databricks"
    )
    assert isinstance(lookup_client.lookup_engine, expected_lookup_engine)


@patch.dict(
    os.environ,
    {
        "READ_SECRET_PREFIX_ACCESS_KEY_ID": "test_access_key",
        "READ_SECRET_PREFIX_SECRET_ACCESS_KEY": "test_secret_key",
    },
)
@pytest.mark.parametrize(
    "oft",
    [
        "online_feature_table",
        "online_feature_table_list",
    ],
)
@patch("boto3.client")
@patch("boto3.resource")
@patch(
    "databricks.feature_store.lookup_engine.LookupDynamoDbEngine._validate_online_feature_table"
)
def test_online_lookup_client_dynamodb(
    _validate_online_feature_table, client, resource, oft, request
):
    oft = request.getfixturevalue(oft)

    lookup_client = online_lookup_client.OnlineLookupClient(oft, "Databricks")
    assert isinstance(lookup_client.lookup_engine, LookupDynamoDbEngine)
    client.assert_called_once_with(
        "dynamodb",
        aws_access_key_id="test_access_key",
        aws_secret_access_key="test_secret_key",
        aws_session_token=None,
        region_name="us-east-1",
    )


@pytest.mark.parametrize(
    "oft",
    [
        "online_feature_table_for_sagemaker",
        "online_feature_table_for_sagemaker_list",
    ],
)
@patch("boto3.client")
@patch("boto3.resource")
@patch(
    "databricks.feature_store.lookup_engine.LookupDynamoDbEngine._validate_online_feature_table"
)
def test_online_lookup_client_sagemaker(
    _validate_online_feature_table, client, resource, oft, request
):
    oft = request.getfixturevalue(oft)
    lookup_client = online_lookup_client.OnlineLookupClient(oft, "SageMaker")
    assert isinstance(lookup_client.lookup_engine, LookupDynamoDbEngine)
    client.assert_called_once_with(
        "dynamodb",
        aws_access_key_id=None,  # No creds needed. Authentication is done via SageMaker role.
        aws_secret_access_key=None,
        aws_session_token=None,
        region_name="us-east-1",
    )


@patch.dict(
    os.environ,
    {
        "READ_SECRET_PREFIX_AUTHORIZATION_KEY": "test_authorization_key",
    },
)
@patch("databricks.feature_store.lookup_engine.lookup_cosmosdb_engine.CosmosClient")
@patch(
    "databricks.feature_store.lookup_engine.LookupCosmosDbEngine._validate_online_feature_table"
)
def test_online_lookup_client_cosmosdb(_validate_online_feature_table, client):
    online_feature_table = OnlineFeatureTable(
        feature_table_name="ft1",
        online_feature_table_name="database.container",
        online_store=OnlineStoreForServing(
            cloud=Cloud.AZURE,
            store_type=StoreType.COSMOSDB,
            extra_configs=CosmosDbConf(account_uri="https://account.com"),
            read_secret_prefix="READ_SECRET_PREFIX",
            creation_timestamp_ms=123,
            query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
        ),
        primary_keys=[],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )

    lookup_client = online_lookup_client.OnlineLookupClient(
        online_feature_table, "Databricks"
    )
    assert isinstance(lookup_client.lookup_engine, LookupCosmosDbEngine)
    client.assert_called_once_with("https://account.com", "test_authorization_key")


@pytest.mark.parametrize(
    ("cloud", "store_type"),
    [
        (Cloud.AZURE, StoreType.MYSQL),
        (Cloud.AZURE, StoreType.SQL_SERVER),
        (Cloud.AZURE, StoreType.COSMOSDB),
        (Cloud.AWS, StoreType.MYSQL),
        (Cloud.AWS, StoreType.AURORA_MYSQL),
        (Cloud.AWS, StoreType.DYNAMODB),
    ],
)
def test_load_credentials_from_env_fails_without_secrets(cloud, store_type):
    online_feature_table = OnlineFeatureTable(
        feature_table_name="ft1",
        online_feature_table_name="online_ft1",
        online_store=OnlineStoreForServing(
            cloud=cloud,
            store_type=store_type,
            extra_configs=None,
            read_secret_prefix="READ_SECRET_PREFIX",
            creation_timestamp_ms=123,
            query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
        ),
        primary_keys=[],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )
    with pytest.raises(Exception) as e:
        creds = online_lookup_client.load_credentials_from_env(online_feature_table)

    if store_type == StoreType.DYNAMODB:
        assert (
            "Internal error: READ_SECRET_PREFIX_ACCESS_KEY_ID not found for feature table"
            in str(e)
        )
    elif store_type == StoreType.COSMOSDB:
        assert (
            "Internal error: READ_SECRET_PREFIX_AUTHORIZATION_KEY not found for feature table"
            in str(e)
        )
    else:
        assert (
            "Internal error: READ_SECRET_PREFIX_USER not found for feature table"
            in str(e)
        )
