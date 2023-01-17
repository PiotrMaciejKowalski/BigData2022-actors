import requests
from bs4 import BeautifulSoup
from pyspark.sql.functions import udf
from lxml import html


def try_extract_link_to_image(text: str) -> str:
    """metoda dla wejściowego tekstu zwraca część tego tekst znajdującą się pomiędzy sekwencjami znaków 'src="' i "._";
    metoda obsługuje wyjątki poprzez zwrócenie elemntu None"""
    try:
        first = 'src="'
        last = "._"
        start = text.rindex(first) + len(first)
        end = text.rindex(last, start)
        return text[start:end]
    except ValueError:
        return None


def try_get_link_to_imdb_image(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    BeautifulSoup, korzystając z metody try_extract_link_to_image do ucięcia części linku odpowiadającej za
    formatowanie"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = str(soup.find("img", attrs={"class": "poster"}))
    return try_extract_link_to_image(image_info)


udf_try_get_link_to_imdb_image = udf(try_get_link_to_imdb_image)


def extract_link_to_image(text: str) -> str:
    """metoda zwraca tekst znajdujący się pomiędzy sekwencjami znaków 'src="' oraz '._'"""
    first = 'src="'
    last = "._"
    start = text.rindex(first) + len(first)
    end = text.rindex(last, start)
    return text[start:end]


def if_get_link_to_imdb_image(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    BeautifulSoup, korzystając z metody extract_link_to_image do ucięcia części linku odpowiadającej za formatowanie
    zdjęcia;
    gdy link do zdjęcia jest pusty, tj. aktor nie ma zdjęcia, to metoda zwraca element None"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = soup.find("img", attrs={"class": "poster"})
    if image_info:
        return extract_link_to_image(str(image_info))
    else: return None


udf_if_get_link_to_imdb_image = udf(if_get_link_to_imdb_image)


def try_get_link_to_imdb_image_src(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    BeautifulSoup, poprzez odwołanie się do odpowiedniego elementu src na stronie oraz następne przycięcie linku przed
    wystąpieniem sekwencji znaków "._";
    metoda obsługuje wyjątki gdy link jest pusty poprzez zwrócenie elemntu None"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = soup.find("img", attrs={"class": "poster"})
    print(image_info)
    try:
        return image_info.get("src").split("._")[0]
    except AttributeError:
        return None


udf_try_get_link_to_imdb_image_src = udf(try_get_link_to_imdb_image_src)


def if_get_link_to_imdb_image_src(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    BeautifulSoup, poprzez odwołanie się do odpowiedniego elementu src na stronie oraz następne przycięcie linku przed
    wystąpieniem sekwencji znaków "._";
    metoda w przypadku gdy link jest pusty zwraca elemnt None;
    używany parser to 'html.parser'"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_info = soup.find("img", attrs={"class": "poster"})
    print(image_info)
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else: return None


udf_if_get_link_to_imdb_image_src = udf(if_get_link_to_imdb_image_src)


def if_get_link_to_imdb_image_lxml(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    BeautifulSoup, poprzez odwołanie się do odpowiedniego elementu src na stronie oraz następne przycięcie linku przed
    wystąpieniem sekwencji znaków "._";
    metoda w przypadku gdy link jest pusty zwraca elemnt None;
    używany parser to 'lxml'"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    image_info = soup.find("img", attrs={"class": "poster"})
    print(image_info)
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else: return None


udf_if_get_link_to_imdb_image_lxml = udf(if_get_link_to_imdb_image_lxml)


def if_get_link_to_imdb_image_html5lib(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    BeautifulSoup, poprzez odwołanie się do odpowiedniego elementu src na stronie oraz następne przycięcie linku przed
    wystąpieniem sekwencji znaków "._";
    metoda w przypadku gdy link jest pusty zwraca elemnt None;
    używany parser to 'html5lib'"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    image_info = soup.find("img", attrs={"class": "poster"})
    print(image_info)
    if image_info is not None:
        return image_info.get("src").split("._")[0]
    else: return None


udf_if_get_link_to_imdb_image_html5lib = udf(if_get_link_to_imdb_image_html5lib)


def lxml_get_link_to_imdb_image(actor_id: str) -> str:
    """metoda przyjmuje jako argument id aktora ze strony IMDB i zwraca link do jego/jej zdjęcia za pomocą biblioteki
    lxml, poprzez odwołanie się do odpowiedniego elementu src na stronie oraz następne przycięcie linku przed
    wystąpieniem sekwencji znaków "._";
    do działania biblioteki wymagane jest zainstalowanie cssselect za pomocą poniższej linijki z kodem:
    !sudo pip3 install cssselect"""
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    poster_el = tree.find('.//img[@class="poster"]')
    if poster_el is not None:
        return poster_el.attrib['src'].split("._")[0]
    else: return None


udf_lxml_get_link_to_image = udf(lxml_get_link_to_imdb_image)
