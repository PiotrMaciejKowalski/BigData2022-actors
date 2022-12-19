import requests
from bs4 import BeautifulSoup

from pyspark.sql.functions import udf


def extract_link_to_image(text: str) -> str:
    try:
        first = 'src="'
        last = "._V1"
        start = text.rindex(first) + len(first)
        end = text.rindex(last, start)
        return text[start:end]
    except ValueError:
        return None


def get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    return extract_link_to_image(image_info)


udf_get_link_to_image = udf(get_link_to_imdb_image)
