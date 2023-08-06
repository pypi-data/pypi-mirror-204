import pandas as pd

import pyspark.sql.functions as F

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import *


def pandas2pyspark(df: pd.DataFrame, spark: SparkSession) -> DataFrame:
    spark_schema = StructType([
        StructField(col, _get_spark_type(df[col]), True)
        for col in df.columns
    ])
    spark_df = spark.createDataFrame(df, spark_schema)
    return spark_df


def spark2pandas(df: DataFrame) -> pd.DataFrame:
    return df.toPandas()


def _get_spark_type(pandas_type):
    if issubclass(pandas_type.type, pd.Timestamp):
        return TimestampType()
    elif issubclass(pandas_type.type, pd.BooleanDtype):
        return BooleanType()
    elif issubclass(pandas_type.type, pd.Float32Dtype):
        return FloatType()
    elif issubclass(pandas_type.type, pd.Float64Dtype):
        return DoubleType()
    elif issubclass(pandas_type.type, pd.Int8Dtype):
        return ByteType()
    elif issubclass(pandas_type.type, pd.Int16Dtype):
        return ShortType()
    elif issubclass(pandas_type.type, pd.Int32Dtype):
        return IntegerType()
    elif issubclass(pandas_type.type, pd.Int64Dtype):
        return LongType()
    elif issubclass(pandas_type.type, pd.UInt8Dtype):
        return ByteType()
    elif issubclass(pandas_type.type, pd.UInt16Dtype):
        return ShortType()
    elif issubclass(pandas_type.type, pd.UInt32Dtype):
        return IntegerType()
    elif issubclass(pandas_type.type, pd.UInt64Dtype):
        return LongType()
    else:
        return StringType()
