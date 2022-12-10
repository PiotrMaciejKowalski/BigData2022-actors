wget https://datasets.imdbws.com/name.basics.tsv.gz
wget https://datasets.imdbws.com/title.akas.tsv.gz
wget https://datasets.imdbws.com/title.basics.tsv.gz
wget https://datasets.imdbws.com/title.crew.tsv.gz
wget https://datasets.imdbws.com/title.episode.tsv.gz
wget https://datasets.imdbws.com/title.principals.tsv.gz
wget https://datasets.imdbws.com/title.ratings.tsv.gz

gzip -dc /content/name.basics.tsv.gz > name.basics.csv
gzip -dc /content/title.akas.tsv.gz > title.akas.csv
gzip -dc /content/title.basics.tsv.gz > title.basic.csv
gzip -dc /content/title.crew.tsv.gz > title.crew.csv
gzip -dc /content/title.episode.tsv.gz > title.episode.csv
gzip -dc /content/title.principals.tsv.gz > title.principals.csv
gzip -dc /content/title.ratings.tsv.gz > title.ratings.csv