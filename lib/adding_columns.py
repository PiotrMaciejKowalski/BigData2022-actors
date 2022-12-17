from pandas import DataFrame
from pyspark.sql.functions import explode, col, count
import requests
from bs4 import BeautifulSoup


def add_number_of_oscars(data:DataFrame)->DataFrame:
    oscars_nominations = data.select("*", explode("winner_oscars").alias("exploded"))\
    .groupBy("nconst", "winner_oscars")\
    .agg(count("exploded").alias("no_nominations_oscars"))\
    .select(["nconst", "no_nominations_oscars"])

    oscars_win = data.select("*", explode("winner_oscars").alias("exploded"))\
        .where(col("exploded") == True)\
        .groupBy("nconst", "winner_oscars")\
        .agg(count("exploded").alias("no_oscars"))\
        .select(["nconst", "no_oscars"])

    data = data.join(oscars_nominations, on="nconst", how="left")
    data = data.join(oscars_win, on="nconst", how="left")
    return data
    
def add_number_of_globes(data:DataFrame)->DataFrame:
    globes_nominations = data.select("*", explode("win_globes").alias("exploded"))\
        .groupBy("nconst", "win_globes")\
        .agg(count("exploded").alias("no_nominations_globes"))\
        .select(["nconst", "no_nominations_globes"])

    globes_win = data.select("*", explode("win_globes").alias("exploded"))\
        .where(col("exploded") == True)\
        .groupBy("nconst", "win_globes")\
        .agg(count("exploded").alias("no_globes"))\
        .select(["nconst", "no_globes"])

    data = data.join(globes_nominations, on="nconst", how="left")    
    data = data.join(globes_win, on="nconst", how="left")
    return data

def add_number_of_emmy_awards(data:DataFrame)->DataFrame:
    emmy_nominations = data.select("*", explode("win_emmy").alias("exploded"))\
        .groupBy("nconst", "win_emmy")\
        .agg(count("exploded").alias("no_nominations_emmy"))\
        .select(["nconst", "no_nominations_emmy"])

    emmy_win = data.select("*", explode("win_emmy").alias("exploded"))\
        .where(col("exploded") == True)\
        .groupBy("nconst", "win_emmy")\
        .agg(count("exploded").alias("no_emmy"))\
        .select(["nconst", "no_emmy"])

    data = data.join(emmy_nominations, on="nconst", how="left")    
    data = data.join(emmy_win, on="nconst", how="left")
    return data

def add_number_of_films(data:DataFrame)->DataFrame:
    number_of_films = data.select("*", explode("tconst").alias("exploded"))\
        .groupBy("nconst", "tconst")\
        .agg(count("exploded").alias("no_films"))\
        .select(["nconst", "no_films"])
    data = data.join(number_of_films, on="nconst", how="left")
    return data

def extract_link_to_image(text: str) -> str:
    try:
        first = 'src="'
        last = '._V1'
        start = text.rindex(first) + len(first)
        end = text.rindex(last, start)
        return text[start: end]
    except ValueError:
        return None

def get_link_to_imdb_image(actor_id: str) -> str:
    url = f'https://www.imdb.com/name/{actor_id}/mediaindex'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_info = str(soup.find('img', attrs={'class': 'poster'}))
    return extract_link_to_image(image_info)

def add_url_to_actor_image(data:DataFrame)->DataFrame:
    data.withColumn("image_url", get_link_to_imdb_image(data.nconst))
    return data

def add_all_columns(data:DataFrame)->DataFrame:
    data = add_number_of_oscars(data)
    data = add_number_of_globes(data)
    data = add_number_of_emmy_awards(data)
    data = add_number_of_films(data)
    data = add_url_to_actor_image(data)
    return data