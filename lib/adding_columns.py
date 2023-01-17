from pandas import DataFrame
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import explode, col, count, avg, array_contains, array

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

def genres_code(data: DataFrame) -> DataFrame:
    assert "genres_code" not in data.columns
    genres = ('Crime', 'Romance', 'Thriller', 'Adventure', 'Drama', 'War', 'Documentary', 'Reality-TV', 'Family', 'Fantasy', 'Game-Show', 'Adult', 'History', 'Mystery', 'Experimental', 'Musical', 'Animation', 'Music', 'Film-Noir', 'Short', 'Horror', 'Western', 'Biography', 'Comedy', 'Action', 'Sport', 'Talk-Show', 'Sci-Fi', 'News')
    genres_list = list(genres)
    for x in genres_list:
        data = data.withColumn(x, array_contains("genres", x).cast("int"))
    data = data.withColumn("genres_code", array(genres_list))
    data = data.drop(*genres)
    return data

def types_code(data: DataFrame) -> DataFrame:
    assert "types_code" not in data.columns
    types = ('tvSeries', 'tvMiniSeries', 'tvMovie', 'tvEpisode', 'movie', 'tvSpecial', 'video', 'videoGame', 'tvShort', 'short', 'tvPilot')
    types_list = list(types)
    for x in types_list:
        data = data.withColumn(x, array_contains("titleType", x).cast("int"))
    data = data.withColumn("types_code", array(types_list))
    data = data.drop(*types)
    return data

def category_code(data: DataFrame) -> DataFrame:
    assert "category_code" not in data.columns
    indexer = StringIndexer(inputCol='category', outputCol='category_code')
    indexer_fitted = indexer.fit(data)
    data = indexer_fitted.transform(data)
    return data

def add_all_columns(spark: SparkSession, data: DataFrame) -> DataFrame:
    data = add_number_of_oscars(data)
    data = add_number_of_globes(data)
    data = add_number_of_emmy_awards(data)
    data = add_number_of_films(data)
    data = add_average_films_ratings(spark, data)
    data = genres_code(data)
    data = types_code(data)
    data = category_code(data)
    return data
