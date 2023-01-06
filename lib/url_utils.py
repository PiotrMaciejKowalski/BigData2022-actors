import requests
from bs4 import BeautifulSoup
from lxml import html
# from html5lib import HTMLParser
# from pyquery import PyQuery as pq
from pyspark.sql.functions import udf


# metody z biblioteki beautiful soup

## metody wycianjące link z pewnej części strony

### wersja try

def try_extract_link_to_image(text: str) -> str:
    try:
        first = 'src="'
        last = "._"
        start = text.rindex(first) + len(first)
        end = text.rindex(last, start)
        return text[start:end]
    except ValueError:
        return None


def try_get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    return try_extract_link_to_image(image_info)


udf_try_get_link_to_imdb_image = udf(try_get_link_to_imdb_image)

### wersja if

def extract_link_to_image(text: str) -> str:
    text = str(text)
    first = 'src="'
    last = "._"
    start = text.rindex(first) + len(first)
    end = text.rindex(last, start)
    return text[start:end]


def if_get_link_to_imdb_image(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = soup.find("img", attrs={"class": "poster"})
    if image_info:
        return extract_link_to_image(str(image_info))
    else: return None


udf_if_get_link_to_imdb_image = udf(if_get_link_to_imdb_image)

## metody docinające końcówkę linku wydobytego z właściwego elemntu (zdjęcia)

### wersja try

def if_get_link_to_imdb_image_src(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = soup.find("img", attrs={"class": "poster"})
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else:
        return image_info.get("src").split("._")[0]


udf_if_get_link_to_imdb_image_src = udf(if_get_link_to_imdb_image_src)

### wersja if

def try_get_link_to_imdb_image_src(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = soup.find("img", attrs={"class": "poster"})
    try:
        return image_info.get("src").split("._")[0]
    except ValueError:
        return None


udf_try_get_link_to_imdb_image_src = udf(try_get_link_to_imdb_image_src)


## testowanie innych parserów

def get_link_to_imdb_image_lxml(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    image_info = soup.find("img", attrs={"class": "poster"})
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else:
        return None


udf_get_link_to_imdb_image_lxml = udf(get_link_to_imdb_image_lxml)


def get_link_to_imdb_image_html5lib(actor_id: str) -> str:
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    image_info = soup.find("img", attrs={"class": "poster"})
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else:
        return None


udf_get_link_to_imdb_image_html5lib = udf(get_link_to_imdb_image_html5lib)


# metody z biblioteki lxml

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
