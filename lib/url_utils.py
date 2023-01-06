import requests
from bs4 import BeautifulSoup
from lxml import html
from html5lib import HTMLParser
# from pyquery import PyQuery as pq
from pyspark.sql.functions import udf


def extract_link_to_image(text: str) -> str:
    try:
        first = 'src="'
        last = "._"
        start = text.rindex(first) + len(first)
        end = text.rindex(last, start)
        return text[start:end]
    except ValueError:
        return None


def if_extract_link_to_image(text: str) -> str:
    if text is not None:
        first = 'src="'
        last = "._"
        start = text.rindex(first) + len(first)
        end = text.rindex(last, start)
        return text[start:end]
    else:
        return None


def get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    return extract_link_to_image(image_info)


udf_try_get_link_to_image = udf(get_link_to_imdb_image)


def if_get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    return extract_link_to_image(image_info)


udf_if_get_link_to_image = udf(if_get_link_to_imdb_image)


def get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.get("img", attrs={"class": "poster"}))
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else:
        return None


udf_get_link_to_image = udf(get_link_to_imdb_image)


def find_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else:
        return None


udf_find_link_to_image = udf(find_link_to_imdb_image)


def lxml_get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    poster_el = tree.find('.//img[@class="poster"]')
    if poster_el is not None:
        return poster_el.attrib['src'].split("._")[0]
    else:
        return None


udf_lxml_get_link_to_image = udf(lxml_get_link_to_imdb_image)
# do ruuchomienia tej metody potrzebna będzie doinstalowanie cssselect za pomocą poniższego
# !sudo pip3 install cssselect


def html_get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    parser = HTMLParser()
    soup = parser.parse(response.content)
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    return extract_link_to_image(image_info)


udf_html_get_link_to_image = udf(html_get_link_to_imdb_image)


# def pq_get_link_to_imdb_image(actor_id: str) -> str:
#     url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
#     response = requests.get(url)
#     doc = pq(response.content)
#     image_info = doc("img.poster")
#     if image_info:
#         return image_info.attr("src").split("._")[0]
#     else:
#         return None


# udf_pq_get_link_to_image = udf(pq_get_link_to_imdb_image)
