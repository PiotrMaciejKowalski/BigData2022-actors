def iou(lista1: list, lista2: list) -> float:
  # metoda przyjmuje jako argument dwie listy i zwraca ich indeks Jaccarda, czyli liczbę z przedzialu [0,1]
  if not lista1 or not lista2:
    return 0
  else:
    intersection = []
    union = []
    intersection = set(lista1).intersection(set(lista2))
    union = set(lista1).union(set(lista2))
    return len(intersection)/len(union)
    

# test jednostkowy dla metody iou
print('1st IOU ', iou([1, 3, 5, 7, 9], [1, 4, 7, 10]))
print('2nd IOU ', iou([], [3, 6]))
print('3rd IOU ', iou([], []))