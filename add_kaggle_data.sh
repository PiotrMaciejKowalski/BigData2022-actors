pip install kaggle
mkdir ~/.kaggle
cp /content/gdrive/.shortcut-targets-by-id/1QtpqeNnbJx1Wz9AxPPOQVNNAtv8wKdu5/bigdataaktorzy/Secrets/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download unanimad/the-oscar-award
unzip the-oscar-award.zip
kaggle datasets download unanimad/golden-globe-awards
unzip golden-globe-awards.zip
kaggle datasets download unanimad/emmy-awards
unzip emmy-awards.zip
# kaggle datasets download tmdb/tmdb-movie-metadata
# unzip tmdb-movie-metadata.zip