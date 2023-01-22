from typing import List, Any, Tuple
import pandas as pd
import numpy


def pokrycie_przedzialow(przedzial1: List[int], przedzial2: List[int]) -> float:
    """metoda przyjmuje jako argument dwie listy w postaci przedzialu liczbowego, tj. lista = [a, b], gdzie a <= b;
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


def sort_two_lists(list1: List[Any], list2: List[Any], sort_list_index: int = 1, reverse: bool = True) -> Tuple[
    List[Any], List[Any]]:
    """metoda sortuje dwie listy równocześnie;
    wybrana z dwóch list jest sortowana po wartościach, a elementy drugiej listy są zamienione miejscami w taki sposób by odpowiadały sortowaniu wykonanemu na poprzednio wybranej liście, np.
    sort([5, 2, 4, 3, 1], ['Adam', 'Zosia', 'Krystyna', 'Karol', 'Tomek'])= 
        =[1, 2, 3, 4, 5], ['Tomek', 'Zosia', 'Karol', 'Krystyna', 'Adam'];
    indeks sortowanej listy decyduje, po elementach której z dwóch list następuje sortowanie po wartościach;
    reverse = True oznacza kolejność malejącą, a reverse = False oznacza kolejność rosnącą"""
    assert len(list1) == len(list2), "listy są różnych długości"
    assert sort_list_index in [1, 2], "indeks sortowanej listy powinien być równy 1 albo 2"
    if sort_list_index == 1:
        zipped_lists = zip(list1, list2)
        list1, list2 = zip(*sorted(zipped_lists, reverse=reverse))
    elif sort_list_index == 2:
        zipped_lists = zip(list2, list1)
        list2, list1 = zip(*sorted(zipped_lists, reverse=reverse))
    return list1, list2


def find_actor(data: pd.DataFrame, actor_id: str) -> List[Any]:
    """metoda na podstawie ramki danych oraz id aktora, zwraca jego dane z ramki danych"""
    actor_index = data[data['nconst'] == actor_id].index
    return data.iloc[actor_index[0]]


def prepare_pandas_row(pandas_row: pd.DataFrame) -> List[Any]:
    """metoda zamienia wiersz wydobyty z Pandas DataFrame i przekształca go w pythonową listę"""
    p_list = []
    for value in pandas_row:
        if type(value) is numpy.ndarray:
            p_list.append(value.tolist())
        else:
            p_list.append(value)
    return p_list


def similarity(actor1: List[Any], actor2: List[Any], reduced_dataset: bool = False) -> float:
    """metoda licząca similarity pomiędzy dwoma aktorami;
    jej argumentami są dwie listy, a wartością wyjściową wartość z przedziału [-1, 1];
    parametr 'reduced_dataset' domyślnie ustawiony jest na False, jednak w przypadku gdy zbiór 
    danych na którym liczymy similarity ograniczamy do listy poniższych 6 kolumn:
    ["nconst", "tconst", "titleType", "genres", "category", "primaryName"]
    to należy zmienić wartość parametru 'reduced_dataset' na True;
    metoda jest przygotowana pod dane ze zbioru JOINED_DATA"""
    weights = [0.3, 0.2, 0.3, 0.2]
    if reduced_dataset:
        values = [
            iou(actor1[1], actor2[1]),  # similarity ze względu na ilość wspólnych filmów
            iou(actor1[2], actor2[2]),  # similarity ze względu na rodzaj granych produkcji
            iou(actor1[3], actor2[3]),  # similarity ze względu na gatunek granych produkcji
            1 if actor1[4] == actor2[4] else 0  # similarity ze względu na tę samą płeć
        ]
    else:
        values = [
            iou(actor1[1], actor2[1]),  # similarity ze względu na ilość wspólnych filmów
            iou(actor1[2], actor2[2]),  # similarity ze względu na rodzaj granych produkcji
            iou(actor1[7], actor2[7]),  # similarity ze względu na gatunek granych produkcji
            1 if actor1[8] == actor2[8] else 0  # similarity ze względu na tę samą płeć
        ]
    length = len(weights)
    assert length == len(values)
    # TODO dodać linijkę uwzględniającą kolumnę knownForTitles za pomocą metody iou
    return sum(weights[i] * values[i] for i in range(length)) * 2 - 1


def similarity_one_vs_all(data: pd.DataFrame, main_actor: List[Any], reduced_dataset: bool = False) -> Tuple[List[str], List[float]]:
    """metoda liczy similarity pomiędzy aktorem main_actor podanym jako lista wartości, a wszystkimi aktorami obecnymi w ramce danych data;
    każdy wiersz ramki jest zamieniany na listę, a nastepnie do uzyskanej listy i main_actor przykładana jest
    funkcja similarity;
    parametr 'reduced_dataset' domyślnie ustawiony jest na False, jednak w przypadku gdy zbiór 
    danych na którym liczymy similarity ograniczamy do listy poniższych 6 kolumn:
    ["nconst", "tconst", "titleType", "genres", "category", "primaryName"]
    to należy zmienić wartość parametru 'reduced_dataset' na True"""
    actors = data.apply(prepare_pandas_row, axis=1)
    similarities = []
    for actor in actors:
        similarities.append(similarity(main_actor, actor, reduced_dataset))
    return list(data["nconst"]), similarities


def select_top_similiar(ids: List[str], values: List[float], top_length: int = 5, include_self: bool = False) -> Tuple[
    List[str], List[float]]:
    """metoda przyjmuje liste z id aktorów oraz listę z wartościami ich similarity;
    zwracana jest wybrana liczba pierwszych elementów z posortowanych list"""
    ids, values = sort_two_lists(ids, values, sort_list_index=2, reverse=True)
    if include_self:
        return ids[:top_length], values[:top_length]
    else:
        return ids[1:top_length + 1], values[1:top_length + 1]


def replace_ids_with_names(data: pd.DataFrame, ids: List[str], name_column_number: int = 10) -> List[str]:
    """metoda zamienia listę id aktorów, na listę ich imion;
    wartości odczytywane są na podstawie ramki danych data
    dla metody similarity parametr 'name_column_number' powinien wynosić 5 (zredukowany dataset) albo 10 (pełen dataset),
    a dla similari_new parametr 'name_column_number' powinien wynosić 3 (zredukowany dataset) albo 10 (pełen dataset)"""
    return [find_actor(data, id)[name_column_number] for id in ids]


def print_top_similiar(main_actor: str, names: List[str], values: List[float]) -> None:
    """metoda wyświetla tekst o n najpodobniejszych do wybranego aktora aktorów;
    metoda wyświetla imię głownego aktora, imiona najbardziej podbnych aktorów i ich similarity"""
    print(f"Najbardziej podobnymi do {main_actor} aktorami/aktorkami są w kolejności:")
    length = len(names)
    assert length == len(values), "listy z imionami i wartościami są różnych długości"
    for i in range(length):
        print(f'  - {names[i]} z similarity równym: {round(values[i], 3)}')


def get_ranking(data: pd.DataFrame, main_actor_id: str, ranking_length: int = 5, reduced_dataset: bool = False) -> List[str]:
    """metoda dla ramki danych, id aktora oraz (opcjonalnie) długości rankingu, zwraca listę id aktorów najbardziej
    podobnych do wybranego aktora"""
    main_actor = prepare_pandas_row(find_actor(data, main_actor_id))
    ids, similarities = similarity_one_vs_all(data, main_actor, reduced_dataset)
    return select_top_similiar(ids, similarities, ranking_length)[0]


def insert_main_actor_column_values(data: pd.DataFrame, column_name: str, value: Any) -> pd.DataFrame:
    """metoda do wskazanej ramki danych dodaje kolumnę o nazwie column_name_main o wartościach wskazanych w argumencie value"""
    for index, row in data.iterrows():
      data.at[index, column_name + "_main"] = value
    return data


def similarity_pandas(row: pd.DataFrame) -> float:
    """metoda została stworzona do testów! sugerowane jest używanie metody 'similarity'!

    metoda liczy similarity pomiędzy dwoma aktorami znadjującymi się w tym samym wierszu;
    aby dodać do wyciągniętego z załadowanych przez nas danych aktora (który jest podany jako pd.DataFrame) kolumn z wartościami aktora
    względem którego będzie liczone similarity, należy użyć metody 'insert_main_actor_column_values' na poniższych kolumnach:
    "tconst", "titleType", "genres", "category"
    metoda nie tworzy tych kolumn automatycznie"""
    weights = [0.3, 0.2, 0.3, 0.2]
    values = [
        iou(list(row["tconst"]), list(row["tconst_main"])),  # similarity ze względu na ilość wspólnych filmów
        iou(list(row["titleType"]), list(row["titleType_main"])),  # similarity ze względu na rodzaj granych produkcji
        iou(list(row["genres"]), list(row["genres_main"])),  # similarity ze względu na gatunek granych produkcji
        1 if row["category"] == row["category_main"] else 0  # similarity ze względu na tę samą płeć
    ]
    length = len(weights)
    assert length == len(values)
    # TODO dodać linijkę uwzględniającą kolumnę knownForTitles za pomocą metody iou
    return sum(weights[i] * values[i] for i in range(length)) * 2 - 1


def similarity_one_vs_all_pandas(data: pd.DataFrame, main_actor_values: pd.DataFrame) -> Tuple[List[str], List[float]]:
    """metoda została stworzona do testów! sugerowane jest używanie metody 'similarity_one_vs_all'!

    metoda liczy similarity pomiędzy aktorem dla którego dane są dostarczone w postaci pandasowego wiersza, oraz
    wszystkimi aktorami obecnymi w ramce danych data;
    w pojedynczym wierszu znajdują się informacje o jednym aktorze pierwotnie znajdującym się w wierszu, oraz obok tych
    danych doklejane są dane o aktorze względem którego liczone jest similarity;
    dla tak zbudowanych wierszy, do całej ramki danych data przykładana jest metoda similarity_pandas która automatycznie
    dla każdego wiersza liczy wartość similarity pomiędzy pierwotnie istniejącym w wierszu aktorem, a aktorem wskazanym
    w argumencie main_actor_values"""
    columns = ["tconst", "titleType", "genres", "category"]
    main_columns = []
    for column in columns:
        main_columns.append(column + "_main")
        data = insert_main_actor_column_values(data, column, main_actor_values[column])
    similarities = list(data.apply(similarity_pandas, axis=1))
    data.drop(columns = main_columns, axis=1)
    return list(data["nconst"]), similarities


def normalized_manhattan_distance(list1: List[float], list2: List[float]) -> float:
    """metoda przyjmuje jako argumenty listy o wartościach liczbowych oraz zwraca liczbę która jest znormalizowaną (długością list)
    odległość Manhattan pomiedzy podanymi dwoma listami"""
    if not list1 or not list2:
        return 0
    else:
        length = len(list1)
        assert length == len(list2), "listy dla których liczona jest odległość są różnych długości"
        distance = sum(abs(value1 - value2) for value1, value2 in zip(list1, list2))
        return distance / length


def similarity_new(actor1: List[Any], actor2: List[Any], reduced_dataset: bool = False) -> float:
    """metoda licząca similarity pomiędzy dwoma aktorami;
    jej argumentami są dwie listy, a wartością wyjściową wartość z przedziału [-1, 1];
    parametr 'reduced_dataset' domyślnie ustawiony jest na False, jednak w przypadku gdy zbiór 
    danych na którym liczymy similarity ograniczamy do listy poniższych 12 kolumn:
    
    ["nconst", "tconst", "category", "primaryName", "knownForTitles", "no_nominations_oscars_norm", "no_nominations_globes_norm",
    "no_nominations_emmy_norm", "no_films_norm", "average_films_rating_norm", "genres_code", "types_code"]
    
    to należy zmienić wartość parametru 'reduced_dataset' na True;
    metoda jest przygotowana pod dane ze zbiorów treningowego, testowego i walidacyjnego"""
    weights = [0.18, 0.05, 0.14, 0.03, 0.03, 0.03, 0.03, 0.09, 0.21, 0.21]
    if reduced_dataset:
        values = [
            iou(actor1[1], actor2[1]),          # similarity ze względu na ilość wspólnych filmów
            1 if actor1[2] == actor2[2] else 0, # similarity ze względu na tę samą płeć
            iou(actor1[4], actor2[4]),          # similarity ze względu na wspólne produkcje z których są znani
            1 - abs(actor1[5] - actor2[5]),    # similarity ze względu na ilość nominacji do oscarów
            1 - abs(actor1[6] - actor2[6]),    # similarity ze względu na ilość nominacji do globów
            1 - abs(actor1[7] - actor2[7]),    # similarity ze względu na ilość nominacji do emmy
            1 - abs(actor1[8] - actor2[8]),   # similarity ze względu na ilość zagranych filmów
            1 - abs(actor1[9] - actor2[9]),   # similarity ze względu na średnią ocenę filmów w których grali aktorzy
            normalized_manhattan_distance(actor1[10], actor2[10]), # similarity ze względu na rodzaj granych produkcji
            normalized_manhattan_distance(actor1[11], actor2[11])  # similarity ze względu na gatunek granych produkcji
        ]
    else:
        values = [
            iou(actor1[1], actor2[1]),          # similarity ze względu na ilość wspólnych filmów
            1 if actor1[8] == actor2[8] else 0, # similarity ze względu na tę samą płeć
            iou(actor1[11], actor2[11]),        # silarity ze względu na wspólne produkcje z których są znani
            1 - abs(actor1[34] - actor2[34]),   # similarity ze względu na ilość nominacji do oscarów
            1 - abs(actor1[36] - actor2[36]),   # similarity ze względu na ilość nominacji do globów
            1 - abs(actor1[38] - actor2[38]),   # similarity ze względu na ilość nominacji do emmy
            1 - abs(actor1[40] - actor2[40]),   # similarity ze względu na ilość zagranych filmów
            1 - abs(actor1[41] - actor2[41]),   # similarity ze względu na średnią ocenę filmów w których grali aktorzy
            normalized_manhattan_distance(actor1[42], actor2[42]), # similarity ze względu na rodzaj granych produkcji
            normalized_manhattan_distance(actor1[43], actor2[43])  # similarity ze względu na gatunek granych produkcji
        ]
    length = len(weights)
    assert length == len(values)
    # TODO dodać linijkę uwzględniającą kolumnę knownForTitles za pomocą metody iou
    return sum(weights[i] * values[i] for i in range(length)) * 2 - 1


def similarity_one_vs_all_new(data: pd.DataFrame, main_actor: List[Any], reduced_dataset: bool = False) -> Tuple[List[str], List[float]]:
    """metoda liczy similarity pomiędzy aktorem main_actor podanym jako lista wartości, a wszystkimi aktorami obecnymi w ramce danych data;
    każdy wiersz ramki jest zamieniany na listę, a nastepnie do uzyskanej listy i main_actor przykładana jest
    funkcja similarity;
    parametr 'reduced_dataset' domyślnie ustawiony jest na False, jednak w przypadku gdy zbiór 
    danych na którym liczymy similarity ograniczamy do listy poniższych 12 kolumn:

    ["nconst", "tconst", "category", "primaryName", "knownForTitles", "no_nominations_oscars_norm", "no_nominations_globes_norm",
    "no_nominations_emmy_norm", "no_films_norm", "average_films_rating_norm", "genres_code", "types_code"]
    
    to należy zmienić wartość parametru 'reduced_dataset' na True"""
    actors = data.apply(prepare_pandas_row, axis=1)
    similarities = []
    for actor in actors:
        similarities.append(similarity_new(main_actor, actor, reduced_dataset))
    return list(data["nconst"]), similarities