!pip install requests
import requests
import cv2

#wczytuje obrazy i zapisuje w katalogu o sciezce c_path
def save_download(url, file_name, c_path):
    file_name=file_name+'.jpg'
    response = requests.get(url)
    with open(file_name, "wb") as f:
      f.write(response.content)
    cv2.imwrite(c_path+'/'+file_name, cv2.imread('/content/'+file_name))

def df_save_download(dataframe, num_col, num_namecol, c_path):
  for i in range(dataframe.count()):
    save_download(dataframe.collect()[i][num_col], str(dataframe.collect()[i][num_namecol]), c_path)
