def iou(lista1: list, lista2: list) -> float:
  # metoda przyjmuje jako argument dwie listy i zwraca ich indeks Jaccarda, czyli liczbę z przedzialu [0,1]
  if not lista1 or not lista2:
    return 0
  else:
    intersection = []
    union = []
    for element in lista1:
      union.append(element)
      if element in lista2:
        intersection.append(element)
    for element in lista2:
      if element not in union:
        union.append(element)
    return len(intersection)/len(union)