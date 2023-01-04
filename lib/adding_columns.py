from pandas import DataFrame
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml import Pipeline
from pyspark.ml.feature import MinMaxScaler, VectorAssembler
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import explode, col, count, avg, udf

from lib.pyspark_init import load_ratings_data


def add_number_of_oscars(data: DataFrame) -> DataFrame:
    oscars_nominations = (
        data.select("*", explode("winner_oscars").alias("exploded"))
        .groupBy("nconst", "winner_oscars")
        .agg(count("exploded").alias("no_nominations_oscars"))
        .select(["nconst", "no_nominations_oscars"])
    )

    oscars_win = (
        data.select("*", explode("winner_oscars").alias("exploded"))
        .where(col("exploded") == True)
        .groupBy("nconst", "winner_oscars")
        .agg(count("exploded").alias("no_oscars"))
        .select(["nconst", "no_oscars"])
    )

    data = data.join(oscars_nominations, on="nconst", how="left")
    data = data.join(oscars_win, on="nconst", how="left")
    return data


def add_number_of_globes(data: DataFrame) -> DataFrame:
    globes_nominations = (
        data.select("*", explode("win_globes").alias("exploded"))
        .groupBy("nconst", "win_globes")
        .agg(count("exploded").alias("no_nominations_globes"))
        .select(["nconst", "no_nominations_globes"])
    )

    globes_win = (
        data.select("*", explode("win_globes").alias("exploded"))
        .where(col("exploded") == True)
        .groupBy("nconst", "win_globes")
        .agg(count("exploded").alias("no_globes"))
        .select(["nconst", "no_globes"])
    )

    data = data.join(globes_nominations, on="nconst", how="left")
    data = data.join(globes_win, on="nconst", how="left")
    return data


def add_number_of_emmy_awards(data: DataFrame) -> DataFrame:
    emmy_nominations = (
        data.select("*", explode("win_emmy").alias("exploded"))
        .groupBy("nconst", "win_emmy")
        .agg(count("exploded").alias("no_nominations_emmy"))
        .select(["nconst", "no_nominations_emmy"])
    )

    emmy_win = (
        data.select("*", explode("win_emmy").alias("exploded"))
        .where(col("exploded") == True)
        .groupBy("nconst", "win_emmy")
        .agg(count("exploded").alias("no_emmy"))
        .select(["nconst", "no_emmy"])
    )

    data = data.join(emmy_nominations, on="nconst", how="left")
    data = data.join(emmy_win, on="nconst", how="left")
    return data


def add_number_of_films(data: DataFrame) -> DataFrame:
    number_of_films = (
        data.select("*", explode("tconst").alias("exploded"))
        .groupBy("nconst", "tconst")
        .agg(count("exploded").alias("no_films"))
        .select(["nconst", "no_films"])
    )
    data = data.join(number_of_films, on="nconst", how="left")
    return data


def add_average_films_ratings(spark: SparkSession, data: DataFrame) -> DataFrame:
    films_ratings = load_ratings_data(spark)
    data_exploded = data.select("*", explode("tconst").alias("exploded"))
    data_with_ratings = (
        data_exploded.join(
            films_ratings, data_exploded.exploded == films_ratings.tconst, how="left"
        )
        .groupBy("nconst")
        .agg(avg("averageRating").alias("average_films_rating"))
        .select(["nconst", "average_films_rating"])
    )
    data = data.join(data_with_ratings, on="nconst", how="left")
    return data

def add_normalized_number_of_oscars(data: DataFrame) -> DataFrame:
    unlist = udf(lambda x: round(float(list(x)[0]),3), DoubleType())
    for i in ['no_nominations_oscars', 'no_oscars', 'no_nominations_globes', 'no_globes', 'no_nominations_emmy', 'no_emmy', 'no_films', 'average_films_rating']:
        assembler = VectorAssembler(inputCols = [i], outputCol = i + "_Vect")
        transformed = assembler.transform(data)
        scaler = MinMaxScaler(inputCol = i + "_Vect", outputCol=i + "_Scaled")
        scalerModel =  scaler.fit(transformed.select(i + "_Vect"))
        scaledData = scalerModel.transform(transformed)
    return scaledData

def add_all_columns(spark: SparkSession, data: DataFrame) -> DataFrame:
    data = add_number_of_oscars(data)
    data = add_number_of_globes(data)
    data = add_number_of_emmy_awards(data)
    data = add_number_of_films(data)
    data = add_average_films_ratings(spark, data)
    return data
