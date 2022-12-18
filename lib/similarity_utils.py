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