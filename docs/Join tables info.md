df_title_akas - None

df_title_basic:
- tconst
- titleType
- originalTitle
- isAdult
- genres

df_title_crew - None

df_title_episode - None

df_title_principals:
- tconst
- nconst
- category
- characters

df_title_ratings - None

df_name_basics:
- nconst
- primaryName
- birthYear
- deathYear
- knownForTitles

------------------------------------------------------

Złączenie danych:
df_name_basics left join df_title_principals on nconst
df_title_principals left join df_title_basic on tconst