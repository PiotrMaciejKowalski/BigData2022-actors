def pokrycie_przedzialow(przedzial1: list[int], przedzial2: list[int]) -> float:
  ''' metoda przyjmuje jako argument dwie listy w postaci przedzialu liczbowego, tj. lista = [a, b], gdzie a <= b
  metoda zwraca liczbę z przedziału [0, 1] '''
  if len(przedzial1) != 2 or len(przedzial2) != 2:
    return 0
  elif przedzial1[1] <= przedzial1[0] or przedzial2[1] <= przedzial2[0]:
    return 0
  else:
    min_l = min(przedzial1[0], przedzial2[0])
    max_l = max(przedzial1[0], przedzial2[0])
    min_p = min(przedzial1[1], przedzial2[1])
    max_p = max(przedzial1[1], przedzial2[1])
    return (min_p - max_l)/(max_p - min_l)