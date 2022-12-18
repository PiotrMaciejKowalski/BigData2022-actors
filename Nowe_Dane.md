# Nowe Dane

Dysponujemy dodatkowymi zbiorami uzupełniające nasze informacje. 
Pierwsze trzy zawierają informacje o nagrodach za filmy.
Warto zwrócić uwagę, że Oscary przyznawane są za produkcje kinowe, Emmy-telewizyjne, natomiast Złote Globy za oba typy produkcji.
Dzięki wykorzystniu wszystkich zbiorów danych z nagrodami możemy uzyskać pełniejszy obraz. Pod odstatnim linkiem znajduje się baza TMBD. Znajdują się tam między innymi informacje o popularności filmów oraz ich budżetach.


## Oscary
Zbiór danych pod poniższym linkiem zawiera o nominowanych oraz zdobywców Oscarów w latach 1927-2020. Dane zawierają wszystkie kategorie w związku z czym informacje o aktorach, które najbardziej nas interesują, to tylko ich wycinek. Każda nominacja aktora/aktorki jest powiązana z rokiem powstania filmu, rokiem ceremonii (również jej numerem), filmem oraz informacją czy była zwycięska.

[Oscary](https://www.kaggle.com/datasets/unanimad/the-oscar-award)

Pod powyższym linkiem brakuje danych z dwóch ostatnich ceremonii. Możliwe, że da się je pobrać bezpośrednio z oficjalnej strony. Niestety nie wiem jak można to zrobić.

[Oscary Oficjalna Strona](https://awardsdatabase.oscars.org/)

## Złote Globy
Zbiór danych pod poniższym linkiem zawiera o nominowanych oraz zdobywców Złotych Globów w latach 1944-2020. Znajdziemy tu dane analogiczne do Oscarów.

[Złote Globy](https://www.kaggle.com/datasets/unanimad/golden-globe-awards)

Na kagglu jest informacja, że dane pochodzą z oficnalnej strony. W związku z tym podaję link. Możliwe, że damy radę je uzupełnić.

[Złote Globy Oficjalna Strona](https://www.goldenglobes.com/awards-database)

## Nagrody Emmy
Zbiór danych pod poniższym linkiem zawiera o nominowanych oraz zdobywców Emmy w latach 1949-2019. W tym zbiorze każda nominacja ma swoje id. Przypisane są do niej takie wartości jak rok, kategoria, nominowany(film/serial), załoga(na przykład aktor wraz z rolą), wytwórnia, kanał emisji oraz informacja czy wygrał. Aktorzy wymienieni są z imienia i nazwiska wraz z odgrywaną rolą.

[Emmy](https://www.kaggle.com/datasets/unanimad/emmy-awards?select=the_emmy_awards.csv)

Na kagglu jest informacja, że dane pochodzą z oficnalnej strony. W związku z tym podaję link. Możliwe, że damy radę je uzupełnić.

[Emmy Oficjalna Strona](https://www.emmys.com/awards/nominees-winners)

## TMDB 5000
Zbiór danych pod poniższym linkeim zawiera informację z bazy TMDB. Znajdziemy tu informacje o aktorach i osobach pracujących przy produkcji filmów oraz budżetach, gatunkach, popularności, wytwórniach filmowych, oryginalnyh językach i tytułach.

[TMDB](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)

Podaję również link do analizy TMDB zrobionej przez kogoś.

[TMDB Analiza](https://github.com/YashMotwani/TMDB-Movies-Dataset-Investigation-)

Bardziej aktualne dane można przygotować korzystając z poniższego źródła. Jednak jest to trochę bardziej złożone zadanie i w mojej ocenie warto rozważyć przydatność tych danych na już przygotowanym zbiorze.

[TMDB Źródło](https://developers.themoviedb.org/3/getting-started/introduction)

Jak dane zostały przygotowane możemy dowiedzieć się tutaj.

[TMDB Przygotowanie Danych](https://gist.github.com/SohierDane/4a84cb96d220fc4791f52562be37968b)

## Rotten Tomatoes

Rotten Tomatoes to serwis któy od początku wydał mi się bardzo interesujący. Możemy tam znaleźć oceny aktorów wystawione przez widownię oraz krytyków za poszczególne filmy. Poniżej przykład.

[Tom Hanks](https://www.rottentomatoes.com/celebrity/tom_hanks)

Niestety nie znalazłem możliwości pobrania tych danych. Możliwe, że jednak damy radę je przygotować w jakiś sposób sami?

[Web Scraping Rotten Tomatoes](https://www.analyticsvidhya.com/blog/2022/05/a-guide-to-web-scraping-rotten-tomatoes/)

## TVDB

TVDB to baza która może bardzo nam pomóc rozszerzyć informacje o aktorach. Możemy tam się dowiedzieć o ich rasie(sic!), miejscu i dacie urodzeniach oraz nominacjach do nagród.

[Bowen Yang](https://thetvdb.com/people/8116811-bowen-yang)

Niestety wygląda na to, że dostęp do tych danych jest płatny ale może komuś uda się jakoś je wydobyć?

[API](https://thetvdb.com/api-information)

## Wikipedia

Miejscem gdzie na pewno znajdziemy bardzo wiele przydatnych informacji o aktorach jest Wikipedia. W mojej ocenie nadmiar i brak uporządkowania danych może stanowić problem. W związku z tym warto zastanowić się nad powróceniem do tego źródła, gdybyśmy ustalili o jakie konkretnie dane chcielibyśmy rozszerzyć nasz zbiór. W takim przypadku możmy zweryfikować czy damy radę je stamtąd uzyskać.

## Pominięte Zbiory

Znalazłem całkiem sporo baz, kóre w mojej ocenie okazały się kompletnie nieprzydatne. Zdecydowałem, że nie będę odnosił się do każdej z osobna, lecz opiszę krótko jakie problemy napotykałem. Były to nieaktualne dane, dane o bardzo wąskiej tematyce(pojazdy z filmów lub bronie), wymagane uzyskanie licencji na dostęp do danych, oraz mała ilość danych lub pokrywające się z tym o już mamy.
