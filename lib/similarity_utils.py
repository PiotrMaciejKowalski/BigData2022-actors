from typing import List, Any
import pandas as pd


def pokrycie_przedzialow(przedzial1: List[int], przedzial2: List[int]) -> float:
    """metoda przyjmuje jako argument dwie listy w postaci przedzialu liczbowego, tj. lista = [a, b], gdzie a <= b
    metoda zwraca liczbę z przedziału [0, 1]"""
    assert len(przedzial1) == 2 and len(przedzial2) == 2, "dlugosci podanych list powinny wynosic 2"
    assert przedzial1[1] >= przedzial1[0] and przedzial2[1] >= przedzial2[0], "przedzial [a, b] jest niepoprawny (b<a)"
    min_l = min(przedzial1[0], przedzial2[0])
    max_l = max(przedzial1[0], przedzial2[0])
    min_p = min(przedzial1[1], przedzial2[1])
    max_p = max(przedzial1[1], przedzial2[1])
    return (min_p - max_l) / (max_p - min_l)


def iou(lista1: List[Any], lista2: List[Any]) -> float:
    """metoda przyjmuje jako argument dwie listy i zwraca ich indeks Jaccarda, czyli liczbę z przedzialu [0,1]"""
    if not lista1 or not lista2:
        return 0
    else:
        intersection = set(lista1).intersection(set(lista2))
        union = set(lista1).union(set(lista2))
        return len(intersection) / len(union)


def sort_two_lists(list1: List[float], list2: List[Any], reverse=True):
    """metoda sortuje dwie listy równocześnie
    list1 jest sortowana po wartościach, a kolejność elementów w list2 zależy od sortowania list1
    reverse = True oznacza kolejność malejącą, a reverse = False oznacza kolejność rosnącą"""
    zipped_lists = zip(list1, list2)
    list1, list2 = zip(*sorted(zipped_lists, reverse=reverse))
    return list1, list2


def prepare_pandas_row(pandas_row: pd.DataFrame) -> List[Any]:
    """metoda zamienia wiersz wydobyty z Pandas DataFrame i przekształca go w pythonową  listę"""
    p_list = []
    for value in pandas_row:
        try:
            p_list.append(value.tolist())
        except AttributeError:
            p_list.append(value)
    return p_list


def similarity(actor1: List[Any], actor2: List[Any]) -> float:
    """metoda licząca similarity pomiędzy dwoma aktorami
    jej argumentami są dwie listy, a wartością wyjściową wartość z przedziału [-1, 1]
    metoda jest przygotowana pod dane ze zbioru JOINED_DATA"""
    if actor1[0] == actor2[0]:
        return -1
    else:
        weights = [0.6, 0.2, 0.2]
        values = [
            iou(actor1[1], actor2[1]),  # similarty ze względu na ilość wspólnych filmów
            iou(actor1[2], actor2[2]),  # similarity ze względu na rodzaj granych produkcji
            iou(actor1[7], actor2[7])  # similarity ze względu na gatunek granych produkcji
        ]
        no_of_columns = 3
        return sum(weights[i] * values[i] for i in range(no_of_columns)) * 2 - 1


def similarity_1_vs_all(data: pd.DataFrame, main_actor: List[Any]):
    ids = []
    similarities = []
    for i in range(len(data)):
        actor = prepare_pandas_row(data.loc[i].values.tolist())
        ids.append(actor[0])
        similarities.append(similarity(main_actor, actor[0:]))
    return ids, similarities
