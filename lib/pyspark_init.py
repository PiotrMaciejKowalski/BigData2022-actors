import os
import pyspark
import findspark  # Czy na pewno potrzebny?
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import collect_list, first, min, max, split, explode, when, col,  monotonically_increasing_id
from pyspark.sql.types import StructType, StringType, IntegerType, BooleanType, FloatType, TimestampType, DateType, ArrayType, MapType
from typing import List, Tuple, Dict, Any
import numpy

def create_spark_context() -> SparkSession:
    if "SPARK_HOME" not in os.environ:
        os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
        os.environ["SPARK_HOME"] = "/content/spark-3.3.1-bin-hadoop2"
    spark = SparkSession.builder.appName("Colab").getOrCreate()
    return spark

def init_schema(conf, column_type_collection, map_types):
  map = {}
  for pole in conf:
    for python_type, column_list in column_type_collection.items():
      if pole in column_list:
        map[pole] = map_types[python_type]
  schemat= StructType()
  for pole, typ in map.items():
    schemat = schemat.add(pole, typ, True)
  return schemat

def string_to_array(df, list_columns_names, p):
  list_columns=[]
  df=df.select("*").withColumn("id", monotonically_increasing_id())
  for column_str in list_columns_names:
    list_columns.append(df.select(split(col(column_str), p).alias(column_str)))
    df=df.drop(column_str)
  for df_column in list_columns:
    assert not "id1" in df.columns, "kolumna id1 już istnieje"
    df_column=df_column.select("*").withColumn("id1", monotonically_increasing_id())
    df=df.join(df_column, col("id")==col("id1"), 'leftouter')
    df=df.drop("id1")
  DF=df.drop("id")
  return DF

def load_data(spark: SparkSession) -> DataFrame:  
  map_types = {
      str : StringType(),
      int : IntegerType(),
      bool : BooleanType(),
      float: FloatType(),
      'timestamp' : TimestampType(),
      'date' : DateType(),
      List[str] : ArrayType(StringType()),
      Tuple[str] : ArrayType(StringType()),
      Dict[str, str] : MapType(StringType(), StringType())
  }
  column_conf = {
    'title_basics' : ['tconst','titleType','primaryTitle','originalTitle','isAdult','startYear','endYear','runtimeMinutes','genres'],
    'principals' : ['tconst','ordering','nconst','category','job','characters'],
    'name_basics' : ['nconst','primaryName','birthYear','deathYear','primaryProfession','knownForTitles'],
  }
  column_type_collection = {
      int : ['startYear', 'endYear', 'runtimeMinutes', 'birthYear', 'deathYear', 'isAdult'],
      str : [ 'titleType', 'primaryTitle', 'originalTitle', 'genres', 'category', 'job', 'characters', \
            'primaryName', 'primaryProfession', 'knownForTitles'],
      bool : [],
      float : [],
      'date': []
  }
  Schematy=[schemat_title_basics, schemat_title_principals, schemat_name_basics] = [ 
  init_schema(column_conf[table], column_type_collection, map_types) 
      for table in ( 'title_basics', 'principals', 'name_basics')]  
  df_name_basics = (
      spark.read.option("header", "true")
      .option("delimiter", "\t")
      .schema(schemat_name_basics)
      .csv("name.basics.csv")
  )
  # df_title_akas=spark.read.option("header","true").option("delimiter", "\t").csv('title.akas.csv')
  df_title_basics = (
      spark.read.option("header", "true")
      .option("delimiter", "\t")
      .schema(schemat_title_basics)
      .csv("title.basic.csv")
  )
  # df_title_crew=spark.read.option("header","true").option("delimiter", "\t").csv('title.crew.csv')
  # df_title_episode=spark.read.option("header","true").option("delimiter","\t").csv('title.episode.csv')
  df_title_principals = (
      spark.read.option("header", "true")
      .option("delimiter", "\t")
      .schema(schemat_title_principals)
      .csv("title.principals.csv")
  )

  for column in ['knownForTitles']:
    df_name_basics = df_name_basics.withColumn(column, when(df_name_basics[column] == "\\N", None).otherwise(df_name_basics[column]))
  for column in ['titleType', 'originalTitle', 'genres']:
    df_title_basics = df_title_basics.withColumn(column, when(df_title_basics[column] == "\\N", None).otherwise(df_title_basics[column]))
  for column in ['ordering', 'category', 'characters']:
    df_title_principals = df_title_principals.withColumn(column, when(df_title_principals[column] == "\\N", None).otherwise(df_title_principals[column]))
  
  df_title_basics = df_title_basics.withColumn("isAdult", df_title_basics["isAdult"].cast(BooleanType()))

  df_name_basics=string_to_array(df_name_basics, ['primaryProfession', 'knownForTitles'], ',')
  df_title_basics=string_to_array(df_title_basics, ['genres'], ',')

  df_name_basics_selected = df_name_basics.filter(
      "primaryProfession like '%actor%' or primaryProfession like '%actress%'"
  )
  df_title_principals_selected = df_title_principals.filter(
      (df_title_principals.category == "actor")
      | (df_title_principals.category == "actress")
  )
  df_title_basics_selected = df_title_basics.select(
      [
          "tconst",
          "titleType",
          "originalTitle",
          "isAdult",
          "startYear",
          "endYear",
          "genres",
      ]
  )
  df_title_principals_selected = df_title_principals_selected.select(
      ["tconst", "nconst", "category", "characters"]
  )
  df_name_basics_selected = df_name_basics_selected.select(
      ["nconst", "primaryName", "knownForTitles"]
  )
  print(
      "df_name_basics_selected dataframe size: ",
      (df_name_basics_selected.count(), len(df_name_basics_selected.columns)),
  )
  print(
      "df_title_principals_selected dataframe size: ",
      (
          df_title_principals_selected.count(),
          len(df_title_principals_selected.columns),
      ),
  )
  print(
      "df_title_basics_selected dataframe size: ",
      (df_title_basics_selected.count(), len(df_title_basics_selected.columns)),
  )
  data = df_title_basics_selected.join(df_title_principals_selected, "tconst", "right")
  print("joined dataframe size: ", (data.count(), len(data.columns)))
  data = data.join(df_name_basics_selected, "nconst", "inner")
  print("joined dataframe size: ", (data.count(), len(data.columns)))
  data = data.groupby("nconst").agg(
      collect_list("tconst").alias("tconst"),
      collect_list("titleType").alias("titleType"),
      collect_list("originalTitle").alias("originalTitle"),
      collect_list("isAdult").alias("isAdult"),
      min("startYear").alias("startYear"),
      max("endYear").alias("endYear"),
      collect_list("genres").alias("genres"),
      first("category").alias("category"),
      collect_list("characters").alias("characters"),
      first("primaryName").alias("primaryName"),
      first("knownForTitles").alias("knownForTitles"),
  )
  return data 


def load_ratings_data(spark: SparkSession) -> DataFrame:
    df_title_ratings = (
        spark.read.option("header", "true")
        .option("delimiter", "\t")
        .csv("title.ratings.csv")
    )
    return df_title_ratings


def add_kaggle_data(spark: SparkSession, data: DataFrame) -> DataFrame:
  map_types = {
      str : StringType(),
      int : IntegerType(),
      bool : BooleanType(),
      float: FloatType(),
      'timestamp' : TimestampType(),
      'date' : DateType(),
      List[str] : ArrayType(StringType()),
      Tuple[str] : ArrayType(StringType()),
      Dict[str, str] : MapType(StringType(), StringType())
  }
  column_conf = {
    'oscars': ['year_film', 'year_ceremony', 'ceremony', 'category', 'name', 'film', 'winner'],
    'globe':['year_film', 'year_award', 'ceremony', 'category', 'nominee', 'film', 'win'],
    'emmy_awards': ['id', 'year', 'category', 'nominee', 'staff', 'company', 'producer', 'win']
  }
  column_type_collection = {
      int : ['year_award', 'year_film', 'year_ceremony', 'ceremony', 'year'],
      str : ['category', 'nominee', 'film', 'name', 'staff','company', 'producer'],
      bool : ['win', 'winner'],
      float : [],
      'date': []
  }
  Schematy=[schemat_oscars, schemat_globe, schemat_emmy_awards] = [ 
  init_schema(column_conf[table], column_type_collection, map_types) 
      for table in ( 'oscars', 'globe', 'emmy_awards')]   

  oscars = spark.read.option("header", "true").schema(schemat_oscars).csv("the_oscar_award.csv")
  globe = spark.read.option("header", "true").schema(schemat_globe).csv("golden_globe_awards.csv")
  # emmy_awards_category = spark.read.option("header", "true").csv(
  #     "emmy_awards_categories.csv"
  # )
  emmy_awards = spark.read.option("header", "true").schema(schemat_emmy_awards).csv("the_emmy_awards.csv")
  # tmdb_credits=spark.read.option("header","true").csv('tmdb_5000_credits.csv')
  # tmdb_movies=spark.read.option("header","true").csv('tmdb_5000_movies.csv')

  emmy_awards=string_to_array(emmy_awards, ['staff'], ";")
  
  oscars_selected = oscars.filter(
      (oscars.category.like("%ACTOR%")) | (oscars.category.like("%ACTRESS%"))
  )
  globe_selected = globe.filter(
      (globe.category.like("%Actor%")) | (globe.category.like("%Actress%"))
  )
  actor_categories = [
      "Outstanding Lead Actor in a Comedy Series",
      "Outstanding Lead Actor in a Drama Series",
      "Outstanding Lead Actor in a Limited or Anthology Series or Movie",
      "Outstanding Lead Actress in a Comedy Series",
      "Outstanding Lead Actress in a Drama Series",
      "Outstanding Lead Actress in a Limited or Anthology Series or Movie",
      "Outstanding Supporting Actor in a Comedy Series",
      "Outstanding Supporting Actor in a Drama Series",
      "Outstanding Supporting Actor in a Limited or Anthology Series or Movie",
      "Outstanding Supporting Actress in a Comedy Series",
      "Outstanding Supporting Actress in a Drama Series",
      "Outstanding Supporting Actress in a Limited or Anthology Series or Movie",
      "Outstanding Character Voice-Over Performance",
      "Outstanding Guest Actor in a Drama Series",
      "Outstanding Guest Actor in a Comedy Series",
      "Outstanding Guest Actress in a Drama Series",
      "Outstanding Guest Actress in a Comedy Series",
      "Outstanding Narrator",
      "Outstanding Actor in a Short Form Comedy or Drama Series",
      "Outstanding Actress in a Short Form Comedy or Drama Series",
      "Best Specialty Act – Single or Group",
      "Outstanding Voice-Over Performance",
      "Outstanding Sports Personality",
      "Most Outstanding Live Personality",
      "Most Outstanding Kinescoped Personality",
  ]
  emmy_awards_selected = emmy_awards.filter(
      emmy_awards.category.isin(actor_categories)
  )
  emmy_awards_selected = emmy_awards_selected.withColumn(
      "staff", explode(split("staff", ", "))
  )
  emmy_awards_selected = emmy_awards_selected.groupby(
      "nominee", "id", "year", "category", "company", "producer", "win"
  ).agg(
      first("staff").alias("staff"),
  )
  oscars_selected = oscars.select(
      ["year_ceremony", "category", "name", "film", "winner"]
  )
  globe_selected = globe.select(["year_award", "category", "nominee", "film", "win"])
  emmy_awards_selected = emmy_awards.select(
      ["year", "category", "nominee", "staff", "company", "producer", "win"]
  )
  oscars_selected = (
      oscars_selected.withColumnRenamed("year_ceremony", "year_oscars")
      .withColumnRenamed("category", "category_oscars")
      .withColumnRenamed("film", "film_oscars")
      .withColumnRenamed("winner", "winner_oscars")
  )
  globe_selected = (
      globe_selected.withColumnRenamed("year_award", "year_globes")
      .withColumnRenamed("category", "category_globes")
      .withColumnRenamed("film", "film_globes")
      .withColumnRenamed("win", "win_globes")
  )
  emmy_awards_selected = (
      emmy_awards_selected.withColumnRenamed("year", "year_emmy")
      .withColumnRenamed("category", "category_emmy")
      .withColumnRenamed("nominee", "nominee_emmy")
      .withColumnRenamed("company", "company_emmy")
      .withColumnRenamed("producer", "producer_emmy")
      .withColumnRenamed("win", "win_emmy")
  )
  data = data.join(oscars_selected, data.primaryName == oscars_selected.name, "left")
  data = data.groupby(
      "nconst",
      "tconst",
      "titleType",
      "originalTitle",
      "isAdult",
      "startYear",
      "endYear",
      "genres",
      "category",
      "characters",
      "primaryName",
      "knownForTitles",
  ).agg(
      collect_list("year_oscars").alias("year_oscars"),
      first("category_oscars").alias("category_oscars"),
      collect_list("film_oscars").alias("film_oscars"),
      collect_list("winner_oscars").alias("winner_oscars"),
  )
  data = data.join(globe_selected, data.primaryName == globe_selected.nominee, "left")
  data = data.groupby(
      "nconst",
      "tconst",
      "titleType",
      "originalTitle",
      "isAdult",
      "startYear",
      "endYear",
      "genres",
      "category",
      "characters",
      "primaryName",
      "knownForTitles",
      "year_oscars",
      "category_oscars",
      "film_oscars",
      "winner_oscars",
  ).agg(
      collect_list("year_globes").alias("year_globes"),
      collect_list("category_globes").alias("category_globes"),
      collect_list("film_globes").alias("film_globes"),
      collect_list("win_globes").alias("win_globes"),
  )
  data = data.join(
      emmy_awards_selected, data.primaryName == emmy_awards_selected.staff, "left"
  )
  data = data.groupby(
      "nconst",
      "tconst",
      "titleType",
      "originalTitle",
      "isAdult",
      "startYear",
      "endYear",
      "genres",
      "category",
      "characters",
      "primaryName",
      "knownForTitles",
      "year_oscars",
      "category_oscars",
      "film_oscars",
      "winner_oscars",
      "year_globes",
      "category_globes",
      "film_globes",
      "win_globes",
  ).agg(
      collect_list("year_emmy").alias("year_emmy"),
      collect_list("category_emmy").alias("category_emmy"),
      collect_list("nominee_emmy").alias("nominee_emmy"),
      collect_list("company_emmy").alias("company_emmy"),
      collect_list("producer_emmy").alias("producer_emmy"),
      collect_list("win_emmy").alias("win_emmy"),
  )

  for df in data:
    df=df.distinct()
  data = data.withColumn("image_url", udf_get_link_to_image(data.nconst))
  return data
  # TODO uruchomic te metody i wygenerowac nowy plik z danymi, gdy będzie potrzebna kolumna z linkami URL do zdjec aktorow
  
