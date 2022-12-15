# Metryka
## Cel użycia metryki/metryk
W naszym projekcie metryki będziemy używać aby zbadać efektywność naszego modelu po zakończeniu uczenia.
## Co będzie mierzyć nasza metryka?
Nasz model dla wybranego aktora szereguje aktorów ze zbioru i zwraca ustaloną liczbę najbardziej godnych polecenia. Kolejność wystąpienia aktorów na liście będzie od najbardziej podobnego do najmniej podobnego. W związku z tym metryka będzie porównywała wybranego aktora do aktorów z listy, przykładając większą wagę do tych którzy będą na niej wcześniej. Aby móc dokonać takiego zestawienia należy ustalić jakie parametry aktoró będziemy porównywać.
## Jakie parametry warto wziąć pod uwagę?
Najbardziej przydatne będą parametry które pozwolą nam w czytelny sposób rozróżnić czy para aktorów jest do siebie podobna. Przykładem może być płeć gdzie dla dwóch wybraych aktorw jest ona jednakowa lub nie. W podobny sposób można porównać czy dwóch aktorów najcześciej gra w tym samym gatunku filmów lub typie produkcji filmowej. Możemy wybrać taką liczbę parametró jaką uznamy za stosowne. Jednak musimy pamiętać, żeby były dla nas rozróżnialne.
## Szkic metryki
<pre>
def (id_aktor, lista_id_aktorów):
  result = 0
  sum = 0
  pozycja = 0
  for other_actor in lista_id_aktorow:
    licznik = 0
    if id_aktor.plec == other_actor.plec:
      licznik += 1
    if id_aktor.top_gatunek == other_actor.top_gatuenk:
      licznik += 1
    if id_aktor.top_typ_filmu == other_actor.top_typ_filmu:
      licznik += 1
    sum += licznik/max_licznik * (len(lista_id_aktorow) - pozycja)
    pozycja+= 1
  result = sum/(max_licznik*(len(lista_id_aktorow))!)
return result
</pre>
## Wyjaśnienie elementów funkcji
id_aktora - id wybranego przez nas aktora\
lista_id_aktorów - lista id aktorów zwróconych przez model\
other_actor - id aktora z listy\
licznik - zlicza tożsame wartości dla aktorów\
max_licznik - maksymalna wartość licznika równa liczbie parametrów\
poyzcja - pozycja aktora na liście. Mnożnik któego używamy z uwagi na wagę kolejności na liście(bardziej podobni są wcześniej)\
sum - suma punktów przyznanych przez funkcję\
result - końcowy wynik który jest wynikiem dzielenia zdobytych punktów przez maksymalną liczbę punktów możliwych do zdobycia. Podanie wyniku w tej formie może w nam pomóc łatwiej porównać wynik dla różnej liczby aktorów bądź parametrów
