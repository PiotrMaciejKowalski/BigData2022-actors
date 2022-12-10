import os
import pyspark
import findspark # Czy na pewno potrzebny?
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import collect_list, first, min, max

def create_spark_context()->SparkSession:
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
    os.environ["SPARK_HOME"] = "/content/spark-3.3.1-bin-hadoop2"
    spark=SparkSession.builder.appName('Colab').getOrCreate()
    return spark

def load_data(spark:SparkSession)->DataFrame:
    df_name_basics=spark.read.option("header", "true").option("delimiter", "\t").csv('name.basics.csv' ) 
    #df_title_akas=spark.read.option("header","true").option("delimiter", "\t").csv('title.akas.csv')
    df_title_basic=spark.read.option("header","true").option("delimiter", "\t").csv('title.basic.csv')
    #df_title_crew=spark.read.option("header","true").option("delimiter", "\t").csv('title.crew.csv')
    # df_title_episode=spark.read.option("header","true").option("delimiter","\t").csv('title.episode.csv')
    df_title_principals=spark.read.option("header","true").option("delimiter","\t").csv('title.principals.csv')
    # df_title_ratings=spark.read.option("header","true").option("delimiter","\t").csv('title.ratings.csv')
    df_name_basics_selected = df_name_basics.filter("primaryProfession like '%actor%' or primaryProfession like '%actress%'")
    df_title_principals_selected = df_title_principals.filter((df_title_principals.category == "actor") | (df_title_principals.category == "actress"))
    df_title_basic_selected = df_title_basic.select(["tconst", "titleType", "originalTitle", "isAdult", "startYear", "endYear", "genres"])
    df_title_principals_selected = df_title_principals_selected.select(["tconst", "nconst", "category", "characters"])
    df_name_basics_selected = df_name_basics_selected.select(["nconst", "primaryName", "knownForTitles"])
    print("df_name_basics_selected dataframe size: ", (df_name_basics_selected.count(), len(df_name_basics_selected.columns)))
    print("df_title_principals_selected dataframe size: ", (df_title_principals_selected.count(), len(df_title_principals_selected.columns)))
    print("df_title_basic_selected dataframe size: ", (df_title_basic_selected.count(), len(df_title_basic_selected.columns)))
    data = df_title_basic_selected.join(df_title_principals_selected, "tconst", "right")
    print("joined dataframe size: ", (data.count(), len(data.columns)))
    data = data.join(df_name_basics_selected, "nconst", "inner")
    print("joined dataframe size: ", (data.count(), len(data.columns)))
    data = data.groupby('nconst').agg(collect_list('tconst').alias("tconst"), collect_list('titleType').alias("titleType"), collect_list('originalTitle').alias("originalTitle"), collect_list('isAdult').alias("isAdult"), min('startYear').alias("startYear"), max('endYear').alias("endYear"), collect_list('genres').alias("genres"), first('category').alias("category"), collect_list('characters').alias("characters"), first('primaryName').alias("primaryName"), first('knownForTitles').alias("knownForTitles"))
    return data