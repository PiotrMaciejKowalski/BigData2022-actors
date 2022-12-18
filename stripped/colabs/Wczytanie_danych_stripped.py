from google.colab import drive
drive.mount('/content/gdrive')

!git clone https://github.com/PiotrMaciejKowalski/BigData2022-actors.git
!mv /content/BigData2022-actors/* .
!mv /content/BigData2022-actors/.* .
!rmdir /content/BigData2022-actors/

#!git checkout

!chmod +x setup_sparka.sh
!./setup_sparka.sh

import pandas as pd
from lib.pyspark_init import create_spark_context, load_data
from lib.const import JOINED_DATA

spark = create_spark_context()
spark

!chmod +x download_data.sh
!./download_data.sh

%%time
data = load_data(spark)
data.show(3)

%%time
data.write.parquet(JOINED_DATA)


