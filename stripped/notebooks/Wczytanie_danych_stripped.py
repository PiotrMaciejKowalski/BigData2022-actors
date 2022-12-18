#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

while 'colabs' in os.getcwd() or 'notebooks' in os.getcwd():
    os.chdir('..')
os.getcwd()


# In[2]:


import pandas as pd
from lib.pyspark_init import create_spark_context, load_data
from lib.const import JOINED_DATA


# In[3]:


spark = create_spark_context()
spark


# In[ ]:


get_ipython().system('chmod +x download_data.sh')
get_ipython().system('./download_data.sh')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'data = load_data(spark)
data.show(3)
')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'data.write.parquet(JOINED_DATA)
')

