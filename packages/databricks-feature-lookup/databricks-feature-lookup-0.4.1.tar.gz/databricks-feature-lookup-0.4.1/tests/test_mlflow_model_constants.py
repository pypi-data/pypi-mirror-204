"""
To run this test:
  pytest tests/test_mlflow_constants.py
"""

from databricks.feature_store import mlflow_model, mlflow_model_constants


def test_mlflow_model_name():
    assert (
        mlflow_model_constants.MLFLOW_MODEL_NAME
        == "databricks.feature_store.mlflow_model"
    )
    assert mlflow_model_constants.MLFLOW_MODEL_NAME == mlflow_model.__name__
