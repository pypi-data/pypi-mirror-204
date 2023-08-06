from typing import Callable

from pyspark.sql import SparkSession, DataFrame, DataFrameReader
from pyspark.sql.types import *

from mlops_core.utils.strings import str2bool

class ADLSConnector():
    def __init__(self, storage_account: str, container_name: str, spark: SparkSession = None, credentials: tuple(str, str) = None, tenant: str = "5d3e2773-e07f-4432-a630-1a0f68a28a05"):
        self.storage_account = storage_account
        self.container_name = container_name
        self.tenant = tenant
        self.spark = spark
        self.credentials = credentials

    def is_passthrough_enabled(self):
        return str2bool(self.spark.conf.get("spark.databricks.passthrough.enabled", "false"))

    def get_abfs_path(self):
        return f"abfss://{self.container_name}@{self.storage_account}.dfs.core.windows.net"

    def get_http_path(self):
        return f"abfss://{self.container_name}@{self.storage_account}.dfs.core.windows.net"

    def load_data(self, relative_path: str, format: str = 'delta', schema: StructType | str = None, decorate: Callable[[DataFrameReader], DataFrameReader] = lambda x: x) -> DataFrame:
        if self.spark is None:
            raise NotImplementedError("Reading data from ADLS when spark isn't present is currently unsupported")

        data_path = self.get_abfs_path() + "/" + relative_path
        if self.is_passthrough_enabled():
            frame_reader = decorate(self.spark.read.format(format))
            frame_reader.schema(schema)
            return frame_reader.load(data_path)
        elif self.credentials is not None:
            self.spark.conf.set(f"fs.azure.account.auth.type.{self.storage_account}.dfs.core.windows.net", "OAuth")
            self.spark.conf.set(f"fs.azure.account.oauth.provider.type.{self.storage_account}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
            self.spark.conf.set(f"fs.azure.account.oauth2.client.id.{self.storage_account}.dfs.core.windows.net", self.credentials[0])
            self.spark.conf.set(f"fs.azure.account.oauth2.client.secret.{self.storage_account}.dfs.core.windows.net", self.credentials[1])
            self.spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{self.storage_account}.dfs.core.windows.net", "https://login.microsoftonline.com/{self.tenant}/oauth2/token")
            frame_reader = decorate(self.spark.read.format(format))
            frame_reader.schema(schema)
            return frame_reader.load(data_path)
        else:
            raise PermissionError("No credential provided or passthrough configured.")
