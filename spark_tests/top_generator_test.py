import pytest
import pyspark
from pyspark.sql import SparkSession, DataFrame

from lib.pyspark_init import create_spark_context
from lib.adding_columns import add_top_genres


def test_add_top_generes():
    spark = create_spark_context()
    df = spark.createDataFrame(
        [
            (1, ["Drama", "Action", "Drama", "Comedy", "Action", "Action"]),
            (2, ["Drama", "Drama", "Drama", "Comedy", "Action", "Comedy", "Romance"]),
        ],
        "id int, generes List[str]",
    )

    df = add_top_genres(df)
    print(df.toPandas())
