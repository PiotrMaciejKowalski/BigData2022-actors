#! /bin/bash
docker run -it --rm -p 8888:8888 -p 4040:4040 --network="host" -v "$PWD":/home/jovyan/project "$@" jupyter/all-spark-notebook
