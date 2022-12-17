from pandas import DataFrame
from pyspark.sql.functions import explode, col, count

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

def add_all_columns(data:DataFrame)->DataFrame:
    data = add_number_of_oscars(data)
    data = add_number_of_globes(data)
    data = add_number_of_emmy_awards(data)
    return data