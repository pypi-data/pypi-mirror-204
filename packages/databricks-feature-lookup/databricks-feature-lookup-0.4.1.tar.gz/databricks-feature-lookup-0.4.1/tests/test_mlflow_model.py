"""
To run this test:
  pytest tests/test_mlflow_model.py
"""

import io
import os
import sys
from typing import List, Tuple
from unittest.mock import ANY, MagicMock, patch

import mlflow
import numpy as np
import pandas as pd
import pytest

from databricks.feature_store import mlflow_model
from databricks.feature_store.entities.cloud import Cloud
from databricks.feature_store.entities.column_info import ColumnInfo
from databricks.feature_store.entities.data_type import DataType
from databricks.feature_store.entities.feature_column_info import FeatureColumnInfo
from databricks.feature_store.entities.feature_table_info import FeatureTableInfo
from databricks.feature_store.entities.feature_tables_for_serving import (
    FeatureTablesForSageMakerServing,
    FeatureTablesForServing,
)
from databricks.feature_store.entities.online_feature_table import (
    FeatureDetails,
    OnlineFeatureTable,
    PrimaryKeyDetails,
)
from databricks.feature_store.entities.online_store_for_serving import (
    DynamoDbConf,
    MySqlConf,
    OnlineStoreForSageMakerServing,
    OnlineStoreForServing,
)
from databricks.feature_store.entities.query_mode import QueryMode
from databricks.feature_store.entities.source_data_column_info import (
    SourceDataColumnInfo,
)
from databricks.feature_store.entities.store_type import StoreType
from databricks.feature_store.utils.feature_spec_test_utils import (
    create_test_feature_spec,
)
from databricks.feature_store.utils.metrics_utils import (
    LOOKUP_E2E_LATENCY,
    OVERRIDEN_FEATURE_COUNT,
)

MODEL_URI = "models:/test/1"

os.environ["FEATURE_TABLES_FOR_SERVING_FILEPATH"] = "/tmp/abc"
os.environ["my_secret_scope_my_secret_prefix_USER"] = "the_db_user"
os.environ["my_secret_scope_my_secret_prefix_PASSWORD"] = "the_db_password"


##### Fixtures


class SumFeaturesModel(object):
    @staticmethod
    def predict(pdf):
        return pdf.values.sum(axis=1)


@pytest.fixture(scope="module")
def sum_features_model():
    model_meta = mlflow.models.Model(
        flavors={"python_function": {"loader_module": "someFlavour"}},
    )
    return mlflow.pyfunc.PyFuncModel(
        model_meta=model_meta, model_impl=SumFeaturesModel()
    )


# For metrics instrumentation, we want to test all potential return types from model.predict:
# np.array, List, pd.Dataframe, and pd.Series. Default SumFeaturesModel returns np.array
class ListOutputModel(object):
    @staticmethod
    def predict(pdf):
        return pdf.values.sum(axis=1).tolist()


@pytest.fixture(scope="module")
def list_output_model():
    model_meta = mlflow.models.Model(
        flavors={"python_function": {"loader_module": "someFlavour"}},
    )
    return mlflow.pyfunc.PyFuncModel(
        model_meta=model_meta, model_impl=ListOutputModel()
    )


class DataFrameOutputModel(object):
    @staticmethod
    def predict(pdf):
        return pd.DataFrame(pdf.values.sum(axis=1))


@pytest.fixture(scope="module")
def dataframe_output_model():
    model_meta = mlflow.models.Model(
        flavors={"python_function": {"loader_module": "someFlavour"}},
    )
    return mlflow.pyfunc.PyFuncModel(
        model_meta=model_meta, model_impl=DataFrameOutputModel()
    )


class SeriesOutputModel(object):
    @staticmethod
    def predict(pdf):
        return pd.Series(pdf.values.sum(axis=1))


@pytest.fixture(scope="module")
def series_output_model():
    model_meta = mlflow.models.Model(
        flavors={"python_function": {"loader_module": "someFlavour"}},
    )
    return mlflow.pyfunc.PyFuncModel(
        model_meta=model_meta, model_impl=SeriesOutputModel()
    )


class IdentityModel(object):
    def __init__(self):
        self._is_databricks_internal_feature_serving_model = True

    def predict(self, context, model_input):
        return model_input


class PyFuncWrapper(object):
    def __init__(self, python_model):
        self.python_model = python_model

    def predict(self, context, model_input):
        self.python_model.predict(context, model_input)


@pytest.fixture(scope="module")
def identity_model():
    model_meta = mlflow.models.Model(
        flavors={"python_function": {"loader_module": "otherFlavour"}},
    )
    return mlflow.pyfunc.PyFuncModel(
        model_meta=model_meta, model_impl=PyFuncWrapper(IdentityModel())
    )


# returns np array sum by default
@pytest.fixture(scope="function", autouse=True)
def pyfunc_model_load(sum_features_model):
    with patch(
        "databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model"
    ) as mock:
        mock.return_value = sum_features_model
        yield mock
        return


@pytest.fixture(scope="function")
def pyfunc_model_load_list_output(list_output_model):
    with patch(
        "databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model"
    ) as mock:
        mock.return_value = list_output_model
        yield mock
        return


@pytest.fixture(scope="function")
def pyfunc_model_load_dataframe_output(dataframe_output_model):
    with patch(
        "databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model"
    ) as mock:
        mock.return_value = dataframe_output_model
        yield mock
        return


@pytest.fixture(scope="function")
def pyfunc_model_load_series_output(series_output_model):
    with patch(
        "databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model"
    ) as mock:
        mock.return_value = series_output_model
        yield mock
        return


@pytest.fixture(scope="function")
def feature_serving_model_load(identity_model):
    with patch(
        "databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model"
    ) as mock:
        mock.return_value = identity_model
        yield mock
        return


@pytest.fixture(scope="module", autouse=True)
def environ():
    return patch.dict(os.environ, {"abc": "def"})


@pytest.fixture(scope="module", autouse=True)
def disable_response_format_patch():
    with patch(
        "databricks.feature_store.mlflow_model.FEATURE_SERVING_RESPONSE_FORMAT_ENABLED",
        False,
    ) as mock:
        yield mock


@pytest.fixture(scope="module")
def online_store_for_serving():
    return OnlineStoreForServing(
        cloud=Cloud.AWS,
        store_type=StoreType.MYSQL,
        extra_configs=MySqlConf(host="test_host", port=123),
        read_secret_prefix="my_secret_scope_my_secret_prefix",
        creation_timestamp_ms=123,
        query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
    )


@pytest.fixture(scope="module")
def online_feature_table1(online_store_for_serving):
    return OnlineFeatureTable(
        feature_table_name="test.ft1",
        online_feature_table_name="test_db_online.test_ft1_online",
        online_store=online_store_for_serving,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def online_feature_table2(online_store_for_serving):
    return OnlineFeatureTable(
        feature_table_name="test.ft2",
        online_feature_table_name="test_db_online.test_ft2_online",
        online_store=online_store_for_serving,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def feature_tables_for_serving_basic(online_feature_table1):
    return FeatureTablesForServing(
        online_feature_tables=[
            online_feature_table1,
        ]
    )


@pytest.fixture(scope="module")
def feature_tables_for_serving_advanced(online_feature_table1, online_feature_table2):
    return FeatureTablesForServing(
        online_feature_tables=[online_feature_table1, online_feature_table2]
    )


@pytest.fixture(scope="function")
def feature_tables_for_serving_load():
    with patch(
        "databricks.feature_store.entities.feature_tables_for_serving.FeatureTablesForServing.load"
    ) as mock:
        yield mock
        return


@pytest.fixture(scope="module")
def dynamo_db_online_store():
    return OnlineStoreForServing(
        cloud=Cloud.AWS,
        store_type=StoreType.DYNAMODB,
        extra_configs=DynamoDbConf(region="us-south-16"),
        read_secret_prefix="my_secret_scope_my_secret_prefix",
        creation_timestamp_ms=123,
        query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
    )


@pytest.fixture(scope="module")
def dynamo_db_online_store_range_lookup():
    return OnlineStoreForServing(
        cloud=Cloud.AWS,
        store_type=StoreType.DYNAMODB,
        extra_configs=DynamoDbConf(region="us-south-16"),
        read_secret_prefix="my_secret_scope_my_secret_prefix",
        creation_timestamp_ms=123,
        query_mode=QueryMode.RANGE_QUERY,
    )


@pytest.fixture(scope="module")
def dynamo_db_online_store2():
    return OnlineStoreForServing(
        cloud=Cloud.AWS,
        store_type=StoreType.DYNAMODB,
        extra_configs=DynamoDbConf(region="us-south-16"),
        read_secret_prefix="my_secret_scope_my_secret_prefix2",
        creation_timestamp_ms=123,
        query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
    )


@pytest.fixture(scope="module")
def dynamo_db_feature_table1(dynamo_db_online_store):
    return OnlineFeatureTable(
        feature_table_name="test.ft1",
        online_feature_table_name="test_db_online.test_ft1_online",
        online_store=dynamo_db_online_store,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def dynamo_db_feature_table2(dynamo_db_online_store):
    return OnlineFeatureTable(
        feature_table_name="test.ft2",
        online_feature_table_name="test_db_online.test_ft2_online",
        online_store=dynamo_db_online_store,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def dynamo_db_feature_table3(dynamo_db_online_store2):
    return OnlineFeatureTable(
        feature_table_name="test.ft2",
        online_feature_table_name="test_db_online.test_ft2_online",
        online_store=dynamo_db_online_store2,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def dynamo_db_feature_table4(dynamo_db_online_store_range_lookup):
    return OnlineFeatureTable(
        feature_table_name="test.ft2",
        online_feature_table_name="test_db_online.test_ft2_online",
        online_store=dynamo_db_online_store_range_lookup,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def dynamo_db_feature_tables_for_batch_serving_basic(dynamo_db_feature_table1):
    return FeatureTablesForServing(online_feature_tables=[dynamo_db_feature_table1])


@pytest.fixture(scope="module")
def dynamo_db_feature_tables_for_batch_serving_advanced(
    dynamo_db_feature_table1, dynamo_db_feature_table2
):
    return FeatureTablesForServing(
        online_feature_tables=[dynamo_db_feature_table1, dynamo_db_feature_table2]
    )


@pytest.fixture(scope="module")
def dynamo_db_feature_tables_with_range_query(
    dynamo_db_feature_table1, dynamo_db_feature_table4
):
    return FeatureTablesForServing(
        online_feature_tables=[dynamo_db_feature_table1, dynamo_db_feature_table4]
    )


@pytest.fixture(scope="module")
def cross_account_dynamo_db_feature_tables_for_serving(
    dynamo_db_feature_table1, dynamo_db_feature_table3
):
    return FeatureTablesForServing(
        online_feature_tables=[dynamo_db_feature_table1, dynamo_db_feature_table3]
    )


@pytest.fixture(scope="module")
def mixed_store_feature_tables_for_serving(
    dynamo_db_feature_table1, online_feature_table2
):
    return FeatureTablesForServing(
        online_feature_tables=[dynamo_db_feature_table1, online_feature_table2]
    )


@pytest.fixture(scope="module")
def online_store_for_sagemaker_serving():
    return OnlineStoreForSageMakerServing(
        creation_timestamp_ms=123,
        extra_configs=DynamoDbConf(region="us-south-16"),
        query_mode=QueryMode.PRIMARY_KEY_LOOKUP,
    )


@pytest.fixture(scope="module")
def online_store_range_query_for_sagemaker_serving():
    return OnlineStoreForSageMakerServing(
        creation_timestamp_ms=123,
        extra_configs=DynamoDbConf(region="us-south-16"),
        query_mode=QueryMode.RANGE_QUERY,
    )


@pytest.fixture(scope="module")
def online_feature_table_for_sagemaker_serving(online_store_for_sagemaker_serving):
    return OnlineFeatureTable(
        feature_table_name="test.ft1",
        online_feature_table_name="test_db_online.test_ft1_online",
        online_store=online_store_for_sagemaker_serving,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def online_feature_table_range_query_for_sagemaker_serving(
    online_store_range_query_for_sagemaker_serving,
):
    return OnlineFeatureTable(
        feature_table_name="test.ft1",
        online_feature_table_name="test_db_online.test_ft1_online",
        online_store=online_store_range_query_for_sagemaker_serving,
        primary_keys=[PrimaryKeyDetails("pk", DataType.INTEGER)],
        feature_table_id="abc123",
        features=[
            FeatureDetails("Ft1", DataType.STRING),
            FeatureDetails(
                "Ft2",
                DataType.ARRAY,
                """{"containsNull":true,"elementType":"integer","type":"array"}""",
            ),
        ],
        timestamp_keys=[],
    )


@pytest.fixture(scope="module")
def feature_tables_for_sagemaker_serving(online_feature_table_for_sagemaker_serving):
    return FeatureTablesForSageMakerServing(
        online_feature_tables=[
            online_feature_table_for_sagemaker_serving,
        ]
    )


@pytest.fixture(scope="module")
def feature_tables_for_sagemaker_serving_range_query(
    online_feature_table_range_query_for_sagemaker_serving,
):
    return FeatureTablesForSageMakerServing(
        online_feature_tables=[
            online_feature_table_range_query_for_sagemaker_serving,
        ]
    )


@pytest.fixture(scope="function")
def feature_tables_for_sagemaker_serving_load():
    with patch(
        "databricks.feature_store.entities.feature_tables_for_serving.FeatureTablesForSageMakerServing.load"
    ) as mock:
        yield mock
        return


@pytest.fixture(scope="module")
def ci_for_feature1():
    return ColumnInfo(
        info=FeatureColumnInfo(
            table_name="test.ft1",
            feature_name="age",
            lookup_key=["user_id"],
            output_name="age",
        ),
        include=True,
    )


# See the following doc for why default 3L namespaces are tested:
# https://docs.google.com/document/d/1x_V9GshlnoAAFFCuDsXWdJVtop9MG2HWTUo5IK_1mEw
@pytest.fixture(scope="module")
def ci_for_feature1_3_level_default_hive_metastore():
    return ColumnInfo(
        info=FeatureColumnInfo(
            table_name="hive_metastore.test.ft1",
            feature_name="age",
            lookup_key=["user_id"],
            output_name="age",
        ),
        include=True,
    )


@pytest.fixture(scope="module")
def ci_for_feature2():
    return ColumnInfo(
        info=FeatureColumnInfo(
            table_name="test.ft2",
            feature_name="num_purchases",
            lookup_key=["product_id"],
            output_name="num_purchases",
        ),
        include=True,
    )


@pytest.fixture(scope="module")
def ci_for_feature2_3_level_default_spark_metastore():
    return ColumnInfo(
        info=FeatureColumnInfo(
            table_name="spark_catalog.test.ft2",
            feature_name="num_purchases",
            lookup_key=["product_id"],
            output_name="num_purchases",
        ),
        include=True,
    )


@pytest.fixture(scope="module")
def ci_for_feature3():
    return ColumnInfo(
        info=FeatureColumnInfo(
            table_name="test.ft2",
            feature_name="rating",
            lookup_key=["product_id"],
            output_name="rating",
        ),
        include=True,
    )


@pytest.fixture(scope="module")
def ci_for_feature3_3_level_default_spark_metastore():
    return ColumnInfo(
        info=FeatureColumnInfo(
            table_name="spark_catalog.test.ft2",
            feature_name="rating",
            lookup_key=["product_id"],
            output_name="rating",
        ),
        include=True,
    )


@pytest.fixture(scope="module")
def ci_for_source_data1():
    return ColumnInfo(
        info=SourceDataColumnInfo(
            name="session_duration",
        ),
        include=True,
    )


# FeatureTableInfo.table_id remains the same between identical 2L and default metastore 3L tables for ease of testing.
# This is required to keep 2L FeatureSpec == reformatted default metastore 3L FeatureSpec
@pytest.fixture(scope="module")
def feature_table_info1():
    return FeatureTableInfo(table_name="test.ft1", table_id="test.ft1_id")


@pytest.fixture(scope="module")
def feature_table_info1_3_level_default_hive_metastore():
    return FeatureTableInfo(
        table_name="hive_metastore.test.ft1", table_id="test.ft1_id"
    )


@pytest.fixture(scope="module")
def feature_table_info2():
    return FeatureTableInfo(table_name="test.ft2", table_id="test.ft2_id")


@pytest.fixture(scope="module")
def feature_table_info2_3_level_default_spark_metastore():
    return FeatureTableInfo(table_name="spark_catalog.test.ft2", table_id="test.ft2_id")


@pytest.fixture(scope="function")
def feature_spec_basic(ci_for_feature1, feature_table_info1):
    return create_test_feature_spec(
        column_infos=[ci_for_feature1], table_infos=[feature_table_info1]
    )


@pytest.fixture(scope="module")
def feature_spec_basic_default_metastore(
    ci_for_feature1_3_level_default_hive_metastore,
    feature_table_info1_3_level_default_hive_metastore,
):
    return create_test_feature_spec(
        column_infos=[ci_for_feature1_3_level_default_hive_metastore],
        table_infos=[feature_table_info1_3_level_default_hive_metastore],
    )


@pytest.fixture(scope="function")
def feature_spec_advanced(
    ci_for_feature1,
    ci_for_feature2,
    ci_for_feature3,
    ci_for_source_data1,
    feature_table_info1,
    feature_table_info2,
):
    return create_test_feature_spec(
        column_infos=[
            ci_for_feature1,
            ci_for_feature2,
            ci_for_feature3,
            ci_for_source_data1,
        ],
        table_infos=[feature_table_info1, feature_table_info2],
    )


@pytest.fixture(scope="module")
def feature_spec_advanced_default_metastore(
    ci_for_feature1_3_level_default_hive_metastore,
    ci_for_feature2_3_level_default_spark_metastore,
    ci_for_feature3_3_level_default_spark_metastore,
    ci_for_source_data1,
    feature_table_info1_3_level_default_hive_metastore,
    feature_table_info2_3_level_default_spark_metastore,
):
    return create_test_feature_spec(
        column_infos=[
            ci_for_feature1_3_level_default_hive_metastore,
            ci_for_feature2_3_level_default_spark_metastore,
            ci_for_feature3_3_level_default_spark_metastore,
            ci_for_source_data1,
        ],
        table_infos=[
            feature_table_info1_3_level_default_hive_metastore,
            feature_table_info2_3_level_default_spark_metastore,
        ],
    )


@pytest.fixture(scope="function")
def feature_spec_multiple_lookup_key(ci_for_feature1):
    ci_for_feature1_different_lookup_key = ColumnInfo(
        info=FeatureColumnInfo(
            table_name="test.ft1",
            feature_name="age",
            lookup_key=["friend_id"],
            output_name="friend_age",
        ),
        include=True,
    )
    return create_test_feature_spec(
        [ci_for_feature1, ci_for_feature1_different_lookup_key]
    )


@pytest.fixture(scope="function")
def feature_spec_load():
    with patch(
        "databricks.feature_store.entities.feature_spec.FeatureSpec.load"
    ) as mock:
        yield mock
        return


@pytest.fixture(scope="function")
def basic_setup(
    feature_spec_load,
    feature_spec_basic,
    feature_tables_for_serving_load,
    feature_tables_for_serving_basic,
):
    """
    This fixture can be passed to a test function to patch FeatureSpec.load and
    FeatureTablesForServing.load to return the basic feature_spec and feature_tables_for_serving
    fixtures defined above. It may remain unused in a test case.
    """
    feature_spec_load.return_value = feature_spec_basic
    feature_tables_for_serving_load.return_value = feature_tables_for_serving_basic


@pytest.fixture(scope="function")
def advanced_setup(
    feature_spec_load,
    feature_spec_advanced,
    feature_tables_for_serving_load,
    feature_tables_for_serving_advanced,
):
    """
    This fixture can be passed to a test function to patch FeatureSpec.load and
    FeatureTablesForServing.load to return the advanced feature_spec and feature_tables_for_serving
    fixtures defined above. It may remain unused in a test case.
    """
    feature_spec_load.return_value = feature_spec_advanced
    feature_tables_for_serving_load.return_value = feature_tables_for_serving_advanced


@pytest.fixture(scope="function")
def lookup_client_basic(online_feature_table1, online_feature_table2):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        yield mock.return_value
        return


@pytest.fixture(scope="function")
def lookup_client_advanced(online_feature_table1, online_feature_table2):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        lookup_client1 = MagicMock()
        lookup_client2 = MagicMock()

        def mock_constructor(online_ft: OnlineFeatureTable, serving_environment: str):
            if online_ft == online_feature_table1:
                return lookup_client1
            elif online_ft == online_feature_table2:
                return lookup_client2
            else:
                raise ValueError(
                    "Unexpected argument passed to OnlineLookupClient constructor"
                )

        mock.side_effect = mock_constructor
        yield (lookup_client1, lookup_client2)
        return


@pytest.fixture(scope="function")
def lookup_client_batch(dynamo_db_feature_table1, dynamo_db_feature_table2):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        yield mock.return_value
        return


@pytest.fixture(scope="function")
def lookup_client_dynamo_db(
    dynamo_db_feature_table1, dynamo_db_feature_table2, dynamo_db_feature_table4
):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        lookup_client1 = MagicMock()
        lookup_client2 = MagicMock()
        lookup_client3 = MagicMock()
        lookup_client4 = MagicMock()

        def mock_constructor(online_ft: OnlineFeatureTable, serving_environment: str):
            if online_ft == dynamo_db_feature_table1:
                return lookup_client1
            elif online_ft == dynamo_db_feature_table2:
                return lookup_client2
            elif online_ft == dynamo_db_feature_table4:
                return lookup_client3
            elif isinstance(online_ft, List):
                return lookup_client4
            else:
                raise ValueError(
                    "Unexpected argument passed to OnlineLookupClient constructor"
                )

        mock.side_effect = mock_constructor
        yield (lookup_client1, lookup_client2)
        return


@pytest.fixture(scope="function")
def lookup_client_sagemaker(online_feature_table_for_sagemaker_serving):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        yield mock.return_value
        return


@pytest.fixture(scope="function")
def lookup_client_dynamo_db_different_account(
    dynamo_db_feature_table1, dynamo_db_feature_table3
):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        lookup_client1 = MagicMock()
        lookup_client2 = MagicMock()

        def mock_constructor(online_ft: OnlineFeatureTable, serving_environment: str):
            if online_ft == dynamo_db_feature_table1:
                return lookup_client1
            elif online_ft == dynamo_db_feature_table3:
                return lookup_client2
            else:
                raise ValueError(
                    "Unexpected argument passed to OnlineLookupClient constructor"
                )

        mock.side_effect = mock_constructor
        yield (lookup_client1, lookup_client2)
        return


@pytest.fixture(scope="function")
def lookup_client_mixed_stores(dynamo_db_feature_table1, online_feature_table2):
    with patch("databricks.feature_store.mlflow_model.OnlineLookupClient") as mock:
        lookup_client1 = MagicMock()
        lookup_client2 = MagicMock()

        def mock_constructor(online_ft: OnlineFeatureTable, serving_environment: str):
            if online_ft == dynamo_db_feature_table1:
                return lookup_client1
            elif online_ft == online_feature_table2:
                return lookup_client2
            else:
                raise ValueError(
                    "Unexpected argument passed to OnlineLookupClient constructor"
                )

        mock.side_effect = mock_constructor
        yield (lookup_client1, lookup_client2)
        return


##### Tests

## Tests: _load_pyfunc succeeds


@pytest.mark.parametrize(
    "feature_spec_yaml", ["feature_spec_basic", "feature_spec_basic_default_metastore"]
)
def test_load_basic(
    feature_spec_load,
    feature_spec_basic,
    feature_tables_for_serving_load,
    feature_tables_for_serving_basic,
    lookup_client_basic,
    pyfunc_model_load,
    sum_features_model,
    online_feature_table1,
    ci_for_feature1,
    request,
    feature_spec_yaml,
):
    feature_spec_load.return_value = request.getfixturevalue(feature_spec_yaml)
    feature_tables_for_serving_load.return_value = feature_tables_for_serving_basic

    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)

    # models using non dynamoDB stores are not elgigible for batch lookup
    assert not loaded_model._is_model_eligible_for_batch_lookup(
        loaded_model.ft_metadata
    )

    assert loaded_model.feature_spec == feature_spec_basic
    assert loaded_model.raw_model == sum_features_model
    assert list(loaded_model.ft_metadata.keys()) == ["test.ft1"]

    actual_meta = loaded_model.ft_metadata["test.ft1"]
    assert isinstance(actual_meta, mlflow_model._FeatureTableMetadata)
    assert list(actual_meta.feature_col_infos_by_lookup_key.keys()) == [("user_id",)]
    assert actual_meta.feature_col_infos_by_lookup_key[("user_id",)] == [
        ci_for_feature1.info
    ]
    assert actual_meta.online_ft == online_feature_table1

    actual_ft_to_lookup_client = loaded_model.ft_to_lookup_client
    assert list(actual_ft_to_lookup_client.keys()) == ["test.ft1"]

    feature_tables_for_serving_load.assert_called_once_with(path="/tmp/abc")
    pyfunc_model_load.assert_called_once_with(f"{MODEL_URI}/raw_model")
    feature_spec_load.assert_called_once_with(MODEL_URI)


@patch("databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model")
def test_load_raw_feature_serving_model(mock_load_model, identity_model):
    mock_load_model.return_value = identity_model

    raw_model = mlflow_model._load_raw_model(MODEL_URI)

    assert raw_model == identity_model
    assert hasattr(
        raw_model._model_impl.python_model,
        "_is_databricks_internal_feature_serving_model",
    )
    mock_load_model.assert_called_once_with(f"{MODEL_URI}/raw_model")


@patch("databricks.feature_store.mlflow_model.mlflow.pyfunc.load_model")
@pytest.mark.usefixtures(
    "feature_spec_load",
    "feature_tables_for_serving_load",
    "lookup_client_basic",
)
@pytest.mark.parametrize("features_serving_format_enabled", [False, True])
def test_load_feature_serving_model_and_patch_json_change(
    mock_load_model, features_serving_format_enabled, identity_model
):
    mock_load_model.return_value = identity_model
    mlflow_serving_module = MagicMock()
    sys.modules["src.mlflowserving"] = mlflow_serving_module
    # set up with a dummy implementation
    mlflow_serving_module.scoring_server.predictions_to_json = (
        lambda x, y: "original result"
    )

    df = pd.DataFrame({"user_id": [123]})
    output = io.StringIO()

    with patch(
        "databricks.feature_store.mlflow_model.FEATURE_SERVING_RESPONSE_FORMAT_ENABLED"
    ) as is_flag_enabled:
        # The method predictions_to_json will be patched if the flag is True
        is_flag_enabled.return_value = features_serving_format_enabled

        mlflow_model._load_pyfunc(MODEL_URI)
        mlflow_serving_module.scoring_server.predictions_to_json(df, output)

        # assert
        mock_load_model.assert_called_with(f"{MODEL_URI}/raw_model")
        if is_flag_enabled:
            assert mock_load_model.call_count == 2
            assert output.getvalue() == '{"features": [{"user_id": 123}]}'
        else:
            assert mock_load_model.call_count == 1
            assert output.getvalue() == "original result"


@patch.dict(os.environ, {"SERVING_ENVIRONMENT": "SageMaker"})
@pytest.mark.parametrize(
    "feature_spec_yaml", ["feature_spec_basic", "feature_spec_basic_default_metastore"]
)
def test_load_sagemaker(
    feature_spec_load,
    feature_spec_basic,
    feature_tables_for_sagemaker_serving_load,
    feature_tables_for_sagemaker_serving,
    lookup_client_sagemaker,
    pyfunc_model_load,
    sum_features_model,
    online_feature_table_for_sagemaker_serving,
    ci_for_feature1,
    request,
    feature_spec_yaml,
):
    feature_spec_load.return_value = request.getfixturevalue(feature_spec_yaml)
    feature_tables_for_sagemaker_serving_load.return_value = (
        feature_tables_for_sagemaker_serving
    )
    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)

    # models on sagemaker are always eligible for batch lookup (same role for DynamoDB auth)
    assert loaded_model._is_model_eligible_for_batch_lookup(loaded_model.ft_metadata)

    assert loaded_model.feature_spec == feature_spec_basic
    assert loaded_model.raw_model == sum_features_model
    assert list(loaded_model.ft_metadata.keys()) == ["test.ft1"]

    actual_meta = loaded_model.ft_metadata["test.ft1"]
    assert isinstance(actual_meta, mlflow_model._FeatureTableMetadata)
    assert list(actual_meta.feature_col_infos_by_lookup_key.keys()) == [("user_id",)]
    assert actual_meta.feature_col_infos_by_lookup_key[("user_id",)] == [
        ci_for_feature1.info
    ]
    assert actual_meta.online_ft == online_feature_table_for_sagemaker_serving

    assert loaded_model.batch_lookup_client is not None

    feature_tables_for_sagemaker_serving_load.assert_called_once_with(path=MODEL_URI)
    pyfunc_model_load.assert_called_once_with(f"{MODEL_URI}/raw_model")
    feature_spec_load.assert_called_once_with(MODEL_URI)


@pytest.mark.parametrize(
    "feature_spec_yaml",
    ["feature_spec_advanced", "feature_spec_advanced_default_metastore"],
)
def test_load_advanced(
    feature_spec_load,
    feature_spec_advanced,
    feature_tables_for_serving_load,
    feature_tables_for_serving_advanced,
    lookup_client_advanced,
    pyfunc_model_load,
    sum_features_model,
    online_feature_table1,
    online_feature_table2,
    ci_for_feature1,
    ci_for_feature2,
    ci_for_feature3,
    request,
    feature_spec_yaml,
):
    feature_spec_load.return_value = request.getfixturevalue(feature_spec_yaml)
    feature_tables_for_serving_load.return_value = feature_tables_for_serving_advanced

    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)

    # models using non dynamoDB stores are not eligible for batch lookup
    assert not loaded_model._is_model_eligible_for_batch_lookup(
        loaded_model.ft_metadata
    )

    assert loaded_model.feature_spec == feature_spec_advanced
    assert loaded_model.raw_model == sum_features_model
    assert list(loaded_model.ft_metadata.keys()) == ["test.ft1", "test.ft2"]

    actual_meta1 = loaded_model.ft_metadata["test.ft1"]
    assert isinstance(actual_meta1, mlflow_model._FeatureTableMetadata)
    assert list(actual_meta1.feature_col_infos_by_lookup_key.keys()) == [("user_id",)]
    assert actual_meta1.feature_col_infos_by_lookup_key[("user_id",)] == [
        ci_for_feature1.info
    ]
    assert actual_meta1.online_ft == online_feature_table1

    actual_meta2 = loaded_model.ft_metadata["test.ft2"]
    assert isinstance(actual_meta2, mlflow_model._FeatureTableMetadata)
    assert list(actual_meta2.feature_col_infos_by_lookup_key.keys()) == [
        ("product_id",)
    ]
    assert actual_meta2.feature_col_infos_by_lookup_key[("product_id",)] == [
        ci_for_feature2.info,
        ci_for_feature3.info,
    ]
    assert actual_meta2.online_ft == online_feature_table2

    actual_ft_to_lookup_client = loaded_model.ft_to_lookup_client
    assert list(actual_ft_to_lookup_client.keys()) == ["test.ft1", "test.ft2"]

    feature_tables_for_serving_load.assert_called_once_with(path="/tmp/abc")
    pyfunc_model_load.assert_called_once_with(f"{MODEL_URI}/raw_model")
    feature_spec_load.assert_called_once_with(MODEL_URI)


## Tests: test batch lookup behavior
# TODO: eventually this should be replaced with more end-to-end behavior once batching implemented rather than calling "private" method

# if all feature tables are dynamo db, should be eligible for batch feature lookup
@patch.dict(
    os.environ,
    {
        "SERVING_ENVIRONMENT": "Databricks",
        "my_secret_scope_my_secret_prefix_ACCESS_KEY_ID": "0",
        "my_secret_scope_my_secret_prefix_SECRET_ACCESS_KEY": "key",
    },
)
def test_batch_eligibility_same_dynamo(
    feature_spec_load,
    feature_spec_advanced,
    feature_tables_for_serving_load,
    dynamo_db_feature_tables_for_batch_serving_advanced,
    lookup_client_dynamo_db,
):
    feature_spec_load.return_value = feature_spec_advanced
    feature_tables_for_serving_load.return_value = (
        dynamo_db_feature_tables_for_batch_serving_advanced
    )
    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)
    assert loaded_model._is_model_eligible_for_batch_lookup(loaded_model.ft_metadata)


@patch.dict(
    os.environ,
    {
        "SERVING_ENVIRONMENT": "Databricks",
        "my_secret_scope_my_secret_prefix_ACCESS_KEY_ID": "0",
        "my_secret_scope_my_secret_prefix_SECRET_ACCESS_KEY": "key",
    },
)
def test_batch_eligibility_with_range_query(
    feature_spec_load,
    feature_spec_advanced,
    feature_tables_for_serving_load,
    dynamo_db_feature_tables_with_range_query,
    lookup_client_dynamo_db,
):
    feature_spec_load.return_value = feature_spec_advanced
    feature_tables_for_serving_load.return_value = (
        dynamo_db_feature_tables_with_range_query
    )
    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)
    assert not loaded_model._is_model_eligible_for_batch_lookup(
        loaded_model.ft_metadata
    )


@patch.dict(
    os.environ,
    {
        "SERVING_ENVIRONMENT": "SageMaker",
    },
)
def test_batch_eligibility_with_range_query_sagemaker(
    feature_spec_load,
    feature_tables_for_sagemaker_serving_load,
    feature_tables_for_sagemaker_serving_range_query,
    lookup_client_basic,
    request,
):

    feature_spec_load.return_value = request.getfixturevalue("feature_spec_basic")
    feature_tables_for_sagemaker_serving_load.return_value = (
        feature_tables_for_sagemaker_serving_range_query
    )
    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)
    assert not loaded_model._is_model_eligible_for_batch_lookup(
        loaded_model.ft_metadata
    )


@patch.dict(
    os.environ,
    {
        "SERVING_ENVIRONMENT": "Databricks",
        "my_secret_scope_my_secret_prefix_ACCESS_KEY_ID": "0",
        "my_secret_scope_my_secret_prefix_SECRET_ACCESS_KEY": "key",
        "my_secret_scope_my_secret_prefix2_ACCESS_KEY_ID": "1",
        "my_secret_scope_my_secret_prefix2_SECRET_ACCESS_KEY": "key2",
    },
)
def test_batch_eligibility_dynamo_different_accounts(
    feature_spec_load,
    feature_spec_advanced,
    feature_tables_for_serving_load,
    cross_account_dynamo_db_feature_tables_for_serving,
    lookup_client_dynamo_db_different_account,
):
    feature_spec_load.return_value = feature_spec_advanced
    feature_tables_for_serving_load.return_value = (
        cross_account_dynamo_db_feature_tables_for_serving
    )
    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)
    assert not loaded_model._is_model_eligible_for_batch_lookup(
        loaded_model.ft_metadata
    )


# if not all feature tables are dynamo db, should not use batch feature lookup
@patch.dict(
    os.environ,
    {
        "SERVING_ENVIRONMENT": "Databricks",
        "my_secret_scope_my_secret_prefix_ACCESS_KEY_ID": "0",
        "my_secret_scope_my_secret_prefix_SECRET_ACCESS_KEY": "key",
    },
)
def test_batch_eligibility_mixed_stores(
    feature_spec_load,
    feature_spec_advanced,
    feature_tables_for_serving_load,
    mixed_store_feature_tables_for_serving,
    lookup_client_mixed_stores,
):
    feature_spec_load.return_value = feature_spec_advanced
    feature_tables_for_serving_load.return_value = (
        mixed_store_feature_tables_for_serving
    )
    loaded_model = mlflow_model._load_pyfunc(MODEL_URI)
    assert not loaded_model._is_model_eligible_for_batch_lookup(
        loaded_model.ft_metadata
    )


## Tests: _load_pyfunc fails
@patch("databricks.feature_store.mlflow_model.databricks_utils")
@pytest.mark.parametrize("env", ["notebook", "job"])
def test_load_fails_in_notebook_or_job(databricks_utils, env):
    databricks_utils.is_in_databricks_notebook.return_value = env == "notebook"
    databricks_utils.is_in_databricks_job.return_value = env == "job"
    with pytest.raises(NotImplementedError) as e:
        mlflow_model._load_pyfunc(MODEL_URI)
    assert "Feature Store packaged models cannot be loaded with MLflow APIs" in str(
        e.value
    )


def test_load_pkey_mismatch(
    feature_spec_load,
    feature_spec_basic,
    feature_tables_for_serving_load,
):
    feature_spec_load.return_value = feature_spec_basic
    extra_pk_online_ft = OnlineFeatureTable(
        feature_table_name="test.ft1",
        online_feature_table_name="test_db_online.test_ft_online",
        online_store=online_store_for_serving,
        primary_keys=[
            PrimaryKeyDetails("pk", DataType.STRING),
            PrimaryKeyDetails("surprise_extra_pk", DataType.INTEGER),
        ],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )
    extra_pk_ft_serving = FeatureTablesForServing(
        online_feature_tables=[extra_pk_online_ft]
    )
    feature_tables_for_serving_load.return_value = extra_pk_ft_serving

    with pytest.raises(Exception) as e:
        mlflow_model._load_pyfunc(MODEL_URI)
    assert "Internal error: Online feature table has primary keys" in str(e)


def test_load_feature_spec_feature_tables_for_serving_mismatch(
    feature_spec_load,
    feature_spec_basic,
    feature_tables_for_serving_load,
    online_store_for_serving,
):
    feature_spec_load.return_value = feature_spec_basic
    online_ft = OnlineFeatureTable(
        feature_table_name="test.this_was_not_the_ft_from_feature_spec",
        online_feature_table_name="test_db_online.test_ft_online",
        online_store=online_store_for_serving,
        primary_keys=[PrimaryKeyDetails("pk", DataType.STRING)],
        feature_table_id="abc123",
        features=[],
        timestamp_keys=[],
    )
    ft_serving = FeatureTablesForServing(online_feature_tables=[online_ft])
    feature_tables_for_serving_load.return_value = ft_serving

    with pytest.raises(Exception) as e:
        mlflow_model._load_pyfunc(MODEL_URI)
    assert "Internal error: Online feature table information could not be found" in str(
        e
    )


## Tests: predict succeeds

# Test metrics with all potential model.predict return types: np.array, list, pd.DataFrame, pd.Series
# see https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html#inference-api
@pytest.mark.parametrize("instrumentation_enabled", ["", "false", "true"])
def test_predict_metrics_array(
    basic_setup, lookup_client_basic, instrumentation_enabled
):
    with patch.dict(
        os.environ, {"LOOKUP_CLIENT_INSTRUMENTATION_ENABLED": instrumentation_enabled}
    ):
        with patch("time.time", side_effect=[1.05, 2.25]):
            fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
            df = pd.DataFrame({"user_id": [123]})
            lookup_client_basic.lookup_features.return_value = pd.DataFrame(
                {"age": [55]}
            )
            prediction = fs_model.predict(df)

            lookup_client_basic.lookup_features.assert_called_once_with(
                ANY, ["age"], metrics=ANY
            )
            pd.testing.assert_frame_equal(
                lookup_client_basic.lookup_features.call_args[0][0],
                pd.DataFrame({"pk": [123]}),
            )
            assert list(prediction) == [55]

            # lookup instrumentation enabled, verify prediction converted to series and e2e latency metrics annotated
            if instrumentation_enabled == "true":
                assert isinstance(prediction, pd.Series)
                assert prediction.attrs[LOOKUP_E2E_LATENCY] == 1200
                assert prediction.attrs[OVERRIDEN_FEATURE_COUNT] == 0
            # lookup instrumentation environment variable false or not not set, should not return any metrics or modify return type
            else:
                assert isinstance(prediction, np.ndarray)


@pytest.mark.parametrize("instrumentation_enabled", ["", "false", "true"])
def test_predict_metrics_list(
    basic_setup,
    lookup_client_basic,
    pyfunc_model_load_list_output,
    instrumentation_enabled,
):
    with patch.dict(
        os.environ, {"LOOKUP_CLIENT_INSTRUMENTATION_ENABLED": instrumentation_enabled}
    ):
        with patch("time.time", side_effect=[1.05, 2.25]):
            fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
            df = pd.DataFrame({"user_id": [123]})
            lookup_client_basic.lookup_features.return_value = pd.DataFrame(
                {"age": [55]}
            )
            prediction = fs_model.predict(df)

            lookup_client_basic.lookup_features.assert_called_once_with(
                ANY, ["age"], metrics=ANY
            )
            pd.testing.assert_frame_equal(
                lookup_client_basic.lookup_features.call_args[0][0],
                pd.DataFrame({"pk": [123]}),
            )
            assert list(prediction) == [55]

            # lookup instrumentation enabled, verify prediction converted to series and e2e latency metrics annotated
            if instrumentation_enabled == "true":
                assert isinstance(prediction, pd.Series)
                assert prediction.attrs[LOOKUP_E2E_LATENCY] == 1200
                assert prediction.attrs[OVERRIDEN_FEATURE_COUNT] == 0
            # lookup instrumentation environment variable false or not not set, should not return any metrics or modify return type
            else:
                assert isinstance(prediction, list)


@pytest.mark.parametrize("instrumentation_enabled", ["", "false", "true"])
def test_predict_metrics_dataframe(
    basic_setup,
    lookup_client_basic,
    pyfunc_model_load_dataframe_output,
    instrumentation_enabled,
):
    with patch.dict(
        os.environ, {"LOOKUP_CLIENT_INSTRUMENTATION_ENABLED": instrumentation_enabled}
    ):
        with patch("time.time", side_effect=[1.05, 2.25]):
            fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
            df = pd.DataFrame({"user_id": [123]})
            lookup_client_basic.lookup_features.return_value = pd.DataFrame(
                {"age": [55]}
            )
            prediction = fs_model.predict(df)

            lookup_client_basic.lookup_features.assert_called_once_with(
                ANY, ["age"], metrics=ANY
            )
            pd.testing.assert_frame_equal(
                lookup_client_basic.lookup_features.call_args[0][0],
                pd.DataFrame({"pk": [123]}),
            )
            # Return type should always be DataFrame, regardless of precense of metrics
            assert isinstance(prediction, pd.DataFrame) and prediction.iloc[
                0
            ].values == [55]

            # lookup instrumentation enabled, verify e2e latency metrics annotated
            if instrumentation_enabled == "true":
                assert prediction.attrs[LOOKUP_E2E_LATENCY] == 1200
                assert prediction.attrs[OVERRIDEN_FEATURE_COUNT] == 0
            # lookup instrumentation environment variable false or not not set, should not return any metrics
            else:
                assert prediction.attrs == {}


@pytest.mark.parametrize("instrumentation_enabled", ["", "false", "true"])
def test_predict_metrics_series(
    basic_setup,
    lookup_client_basic,
    pyfunc_model_load_series_output,
    instrumentation_enabled,
):
    with patch.dict(
        os.environ, {"LOOKUP_CLIENT_INSTRUMENTATION_ENABLED": instrumentation_enabled}
    ):
        with patch("time.time", side_effect=[1.05, 2.25]):
            fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
            df = pd.DataFrame({"user_id": [123]})
            lookup_client_basic.lookup_features.return_value = pd.DataFrame(
                {"age": [55]}
            )
            prediction = fs_model.predict(df)

            lookup_client_basic.lookup_features.assert_called_once_with(
                ANY, ["age"], metrics=ANY
            )
            pd.testing.assert_frame_equal(
                lookup_client_basic.lookup_features.call_args[0][0],
                pd.DataFrame({"pk": [123]}),
            )
            # Return type should always be Series, regardless of precense of metrics
            assert isinstance(prediction, pd.Series) and list(prediction) == [55]

            # lookup instrumentation enabled, verify e2e latency metrics annotated
            if instrumentation_enabled == "true":
                assert prediction.attrs[LOOKUP_E2E_LATENCY] == 1200
                assert prediction.attrs[OVERRIDEN_FEATURE_COUNT] == 0
            # lookup instrumentation environment variable false or not not set, should not return any metrics
            else:
                assert prediction.attrs == {}


@patch.dict(os.environ, {"SERVING_ENVIRONMENT": "SageMaker"})
@patch("databricks.feature_store.mlflow_model.OnlineLookupClient")
def test_predict_sagemaker(
    lookup_client_sagemaker,
    feature_spec_load,
    feature_spec_basic,
    online_feature_table_for_sagemaker_serving,
    feature_tables_for_sagemaker_serving_load,
    feature_tables_for_sagemaker_serving,
):
    feature_spec_load.return_value = feature_spec_basic
    feature_tables_for_sagemaker_serving_load.return_value = (
        feature_tables_for_sagemaker_serving
    )
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123]})
    lookup_client_obj = lookup_client_sagemaker.return_value
    lookup_client_obj.batch_lookup_features.return_value = {
        "test_db_online.test_ft1_online": {("user_id",): pd.DataFrame({"age": [55]})}
    }
    prediction = fs_model.predict(df)

    lookup_client_sagemaker.assert_called_once_with(
        [online_feature_table_for_sagemaker_serving], serving_environment="SageMaker"
    )
    lookup_client_obj.batch_lookup_features.assert_called_once_with(
        ANY, {"test_db_online.test_ft1_online": {("user_id",): ["age"]}}, metrics=ANY
    )
    pd.testing.assert_frame_equal(
        lookup_client_obj.batch_lookup_features.call_args[0][0][
            "test_db_online.test_ft1_online"
        ][("user_id",)],
        pd.DataFrame({"pk": [123]}),
    )
    assert prediction == [55]


@patch.dict(
    os.environ,
    {
        "SERVING_ENVIRONMENT": "Databricks",
        "my_secret_scope_my_secret_prefix_ACCESS_KEY_ID": "0",
        "my_secret_scope_my_secret_prefix_SECRET_ACCESS_KEY": "key",
        "LOOKUP_CLIENT_INSTRUMENTATION_ENABLED": "true",
    },
)
@pytest.mark.parametrize(
    (
        "feature_spec",
        "feature_tables",
        "input_df",
        "batch_lookup_values",
        "prediction_result",
        "overridden_feature_count",
    ),
    [
        (
            # basic
            "feature_spec_basic",
            "dynamo_db_feature_tables_for_batch_serving_basic",
            pd.DataFrame({"user_id": [123]}),
            {
                "test_db_online.test_ft1_online": {
                    ("user_id",): pd.DataFrame({"age": [55]})
                }
            },
            [55],
            0,
        ),
        (
            # multiple feature tables
            "feature_spec_advanced",
            "dynamo_db_feature_tables_for_batch_serving_advanced",
            pd.DataFrame(
                {"user_id": [123], "product_id": [555], "session_duration": [77]}
            ),
            {
                "test_db_online.test_ft1_online": {
                    ("user_id",): pd.DataFrame({"age": [55]})
                },
                "test_db_online.test_ft2_online": {
                    ("product_id",): pd.DataFrame(
                        {"num_purchases": [3], "rating": [4.2]}
                    )
                },
            },
            [55 + 3 + 4.2 + 77],
            0,
        ),
        (
            # multiple rows
            "feature_spec_basic",
            "dynamo_db_feature_tables_for_batch_serving_basic",
            pd.DataFrame({"user_id": [123, 456]}),
            {
                "test_db_online.test_ft1_online": {
                    ("user_id",): pd.DataFrame({"age": [55, 32]})
                }
            },
            [55, 32],
            0,
        ),
        (
            # multiple lookup keys
            "feature_spec_multiple_lookup_key",
            "dynamo_db_feature_tables_for_batch_serving_basic",
            pd.DataFrame({"user_id": [123], "friend_id": [456]}),
            {
                "test_db_online.test_ft1_online": {
                    ("user_id",): pd.DataFrame({"age": [55]}),
                    ("friend_id",): pd.DataFrame({"age": [73]}),
                }
            },
            [55 + 73],
            0,
        ),
        (
            # Fully overriden feature values
            "feature_spec_basic",
            "dynamo_db_feature_tables_for_batch_serving_basic",
            pd.DataFrame({"user_id": [123], "age": [7]}),
            {
                "test_db_online.test_ft1_online": {
                    ("user_id",): pd.DataFrame(
                        {"age": [5]}
                    )  # this value will get overriden
                }
            },
            [7],
            1,
        ),
        (
            # Partially overriden feature values
            "feature_spec_advanced",
            "dynamo_db_feature_tables_for_batch_serving_advanced",
            pd.DataFrame(
                {
                    "user_id": [123, 456, 789],
                    "product_id": [555, 666, 777],
                    "age": [
                        55,
                        66,
                        None,
                    ],  # <-- partially-overriden feature: 1st and 2nd row gets overridden, 3nd uses lookup value
                    "num_purchases": [15, None, 23],  # 2nd row will use lookup value
                    "session_duration": [7, 8, 10],
                }
            ),
            {
                "test_db_online.test_ft1_online": {
                    ("user_id",): pd.DataFrame({"age": [44, 44, 44]})
                },
                "test_db_online.test_ft2_online": {
                    ("product_id",): pd.DataFrame(
                        {"num_purchases": [9, 9, 9], "rating": [4.2, 3.1, 5.1]}
                    )
                },
            },
            [55 + 4.2 + 15 + 7, 66 + 3.1 + 9 + 8, 44 + 5.1 + 23 + 10],
            4,  # 2 age values get overridden + 2 num_purchase values overridden
        ),
    ],
)
def test_predict_batch(
    feature_spec,
    feature_tables,
    input_df,
    batch_lookup_values,
    prediction_result,
    overridden_feature_count,
    request,
    lookup_client_batch,
    feature_spec_load,
    feature_tables_for_serving_load,
):
    feature_spec_load.return_value = request.getfixturevalue(feature_spec)
    feature_tables_for_serving_load.return_value = request.getfixturevalue(
        feature_tables
    )

    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    lookup_client_batch.batch_lookup_features.return_value = batch_lookup_values
    prediction = fs_model.predict(input_df)

    assert prediction.attrs[OVERRIDEN_FEATURE_COUNT] == overridden_feature_count
    assert list(prediction) == prediction_result


def test_predict_advanced(
    advanced_setup,
    lookup_client_advanced,
):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123], "product_id": [555], "session_duration": [77]})
    lookup_client1, lookup_client2 = lookup_client_advanced
    lookup_client1.lookup_features.return_value = pd.DataFrame({"age": [55]})
    lookup_client2.lookup_features.return_value = pd.DataFrame(
        {"num_purchases": [3], "rating": [4.2]}
    )
    prediction = fs_model.predict(df)

    lookup_client1.lookup_features.assert_called_once_with(ANY, ["age"], metrics=ANY)
    pd.testing.assert_frame_equal(
        lookup_client1.lookup_features.call_args[0][0], pd.DataFrame({"pk": [123]})
    )

    lookup_client2.lookup_features.assert_called_once_with(
        ANY, ["num_purchases", "rating"], metrics=ANY
    )
    pd.testing.assert_frame_equal(
        lookup_client2.lookup_features.call_args[0][0], pd.DataFrame({"pk": [555]})
    )
    assert prediction == [55 + 3 + 4.2 + 77]


def test_predict_multiple_rows(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123, 456]})
    lookup_client_basic.lookup_features.return_value = pd.DataFrame({"age": [55, 32]})
    prediction = fs_model.predict(df)

    lookup_client_basic.lookup_features.assert_called_once_with(
        ANY, ["age"], metrics=ANY
    )
    pd.testing.assert_frame_equal(
        lookup_client_basic.lookup_features.call_args[0][0],
        pd.DataFrame({"pk": [123, 456]}),
    )
    assert list(prediction) == [55, 32]


def test_multiple_lookup_keys(
    feature_spec_load,
    feature_spec_multiple_lookup_key,
    feature_tables_for_serving_load,
    feature_tables_for_serving_basic,
    lookup_client_basic,
    ci_for_feature1,
    feature_table_info1,
):
    feature_spec = feature_spec_multiple_lookup_key
    feature_spec_load.return_value = feature_spec
    feature_tables_for_serving_load.return_value = feature_tables_for_serving_basic

    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123], "friend_id": [456]})
    lookup_client_basic.lookup_features.side_effect = [
        pd.DataFrame({"age": [55]}),
        pd.DataFrame({"age": [73]}),
    ]
    prediction = fs_model.predict(df)

    assert lookup_client_basic.lookup_features.call_count == 2
    first_call = lookup_client_basic.lookup_features.call_args_list[0]
    pd.testing.assert_frame_equal(first_call[0][0], pd.DataFrame({"pk": [123]}))
    assert first_call[0][1] == ["age"]

    second_call = lookup_client_basic.lookup_features.call_args_list[1]
    pd.testing.assert_frame_equal(second_call[0][0], pd.DataFrame({"pk": [456]}))
    assert second_call[0][1] == ["age"]

    assert prediction == [55 + 73]


def test_predict_override_all_feature_values(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123], "age": [7]})
    prediction = fs_model.predict(df)

    assert lookup_client_basic.lookup_features.call_count == 0
    assert prediction == [7]


def test_predict_override_some_feature_values(
    advanced_setup,
    lookup_client_advanced,
):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame(
        {
            "user_id": [123, 456],
            "product_id": [555, 666],
            "num_purchases": [15, 22],  # <-- overrides feature value
            "session_duration": [7, 10],
        }
    )
    lookup_client1, lookup_client2 = lookup_client_advanced
    lookup_client1.lookup_features.return_value = pd.DataFrame({"age": [55, 66]})
    lookup_client2.lookup_features.return_value = pd.DataFrame({"rating": [4.2, 3.1]})
    prediction = fs_model.predict(df)

    lookup_client1.lookup_features.assert_called_once_with(ANY, ["age"], metrics=ANY)
    pd.testing.assert_frame_equal(
        lookup_client1.lookup_features.call_args[0][0], pd.DataFrame({"pk": [123, 456]})
    )

    # num_purchases is not looked up since it is overridden for all rows
    lookup_client2.lookup_features.assert_called_once_with(ANY, ["rating"], metrics=ANY)
    pd.testing.assert_frame_equal(
        lookup_client2.lookup_features.call_args[0][0], pd.DataFrame({"pk": [555, 666]})
    )
    np.testing.assert_array_equal(prediction, [55 + 4.2 + 15 + 7, 66 + 3.1 + 22 + 10])


def test_predict_override_advanced(
    advanced_setup,
    lookup_client_advanced,
):

    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame(
        {
            "user_id": [123, 456],
            "product_id": [555, 666],
            "age": [np.nan, 47],  # <-- override "age" for only some rows
            "num_purchases": [
                888,
                999,
            ],  # <-- override "num_purchases" for all rows
            "session_duration": [7, 10],
        }
    )
    lookup_client1, lookup_client2 = lookup_client_advanced
    lookup_client1.lookup_features.return_value = pd.DataFrame({"age": [22, 32]})
    lookup_client2.lookup_features.return_value = pd.DataFrame({"rating": [4.2, 3.1]})
    prediction = fs_model.predict(df)

    lookup_client1.lookup_features.assert_called_once_with(ANY, ["age"], metrics=ANY)

    # num_purchases should not be looked up, since all feature values were overridden
    lookup_client2.lookup_features.assert_called_once_with(ANY, ["rating"], metrics=ANY)
    pd.testing.assert_frame_equal(
        lookup_client2.lookup_features.call_args[0][0], pd.DataFrame({"pk": [555, 666]})
    )
    np.testing.assert_array_equal(prediction, [22 + 888 + 4.2 + 7, 47 + 999 + 3.1 + 10])


def test_predict_nan_source_data_column_info(
    advanced_setup,
    lookup_client_advanced,
):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame(
        {"user_id": [123], "product_id": [555], "session_duration": [np.nan]}
    )
    lookup_client1, lookup_client2 = lookup_client_advanced
    lookup_client1.lookup_features.return_value = pd.DataFrame({"age": [55]})
    lookup_client2.lookup_features.return_value = pd.DataFrame(
        {"num_purchases": [3], "rating": [4.2]}
    )
    prediction = fs_model.predict(df)

    assert len(prediction) == 1
    assert np.isnan(prediction[0])


def test_predict_extra_columns_are_ignored(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123], "unexpected_column": [73]})
    lookup_client_basic.lookup_features.return_value = pd.DataFrame({"age": [55]})
    prediction = fs_model.predict(df)

    lookup_client_basic.lookup_features.assert_called_once_with(
        ANY, ["age"], metrics=ANY
    )
    pd.testing.assert_frame_equal(
        lookup_client_basic.lookup_features.call_args[0][0], pd.DataFrame({"pk": [123]})
    )
    assert prediction == [55]


## Tests: predict fails


def test_predict_missing_source_data_column_info(
    advanced_setup, lookup_client_advanced
):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    # df is missing session_duration column
    df = pd.DataFrame({"user_id": [123], "product_id": [555]})
    with pytest.raises(ValueError) as e:
        fs_model.predict(df)
    assert "Input is missing columns" in str(e)


def test_predict_missing_lookup_key(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"not_the_lookup_key": [123]})
    with pytest.raises(ValueError) as e:
        fs_model.predict(df)
    assert "Input is missing columns" in str(e)


def test_predict_nan_lookup_key(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [np.nan]})
    with pytest.raises(ValueError) as e:
        fs_model.predict(df)
    assert (
        "Failed to lookup feature values due to null values for lookup_key columns"
        in str(e)
    )


def test_predict_duplicate_lookup_key_column(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)

    df = pd.DataFrame({"user_id": [123], "user_id_clone": [123]})
    df.rename({"user_id_clone": "user_id"}, axis=1, inplace=True)
    with pytest.raises(ValueError) as e:
        fs_model.predict(df)
    assert "Input has duplicate columns" in str(e)


def test_predict_duplicate_source_column_info_column(
    advanced_setup, lookup_client_advanced
):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame(
        {
            "user_id": [123],
            "product_id": [555],
            "session_duration": [77],
            "session_duration_clone": [77],
        }
    )
    df.rename({"session_duration_clone": "session_duration"}, axis=1, inplace=True)

    with pytest.raises(ValueError) as e:
        fs_model.predict(df)
    assert "Input has duplicate columns" in str(e)


def test_predict_predict_duplicate_override_column(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    df = pd.DataFrame({"user_id": [123], "age": [7], "age_clone": [7]})
    df.rename({"age_clone": "age"}, axis=1, inplace=True)

    with pytest.raises(ValueError) as e:
        fs_model.predict(df)
    assert "Input has duplicate columns" in str(e)


def test_predict_lookup_returns_too_few_rows(basic_setup, lookup_client_basic):
    fs_model = mlflow_model._FeatureStoreModelWrapper(MODEL_URI)
    # 2 rows in input
    df = pd.DataFrame({"user_id": [123, 456]})
    # lookup_client only returns 1 row
    lookup_client_basic.lookup_features.return_value = pd.DataFrame({"age": [55]})
    with pytest.raises(Exception) as e:
        fs_model.predict(df)
    assert "Expected 2 rows to be looked up" in str(e)
