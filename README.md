# BigData2022-actors

Projekt dotyczy utworzenia modelu wyznaczającego podobieństwo pomiędzy aktorami z bazy imdb, dostępnymi pod linkiem

[dane](https://datasets.imdbws.com/)

z opisem pól

[opis](https://www.imdb.com/interfaces/)

Model ma w założeniu wyliczać dla dwóch rekordów aktorów (ludzi filmu) liczbę z przedziału [-1,1].

# Instalacja lokalnej condy
```
conda create --name bigdata python=3.9
conda activate bigdata
pip install pyspark
```