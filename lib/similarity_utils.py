from typing import List


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
def iou(lista1: list[any], lista2: list[any]) -> float:
  ''' metoda przyjmuje jako argument dwie listy i zwraca ich indeks Jaccarda, czyli liczbę z przedzialu [0,1]
  '''
  if not lista1 or not lista2:
    return 0
  else:
    intersection = []
    union = []
    intersection = set(lista1).intersection(set(lista2))
    union = set(lista1).union(set(lista2))
    return len(intersection)/len(union)
