def iou(lista1, lista2):
  # metoda przyjmuje jako argument dwie listy i zwraca ich indeks Jaccarda, czyli liczbę z przedzialu [0,1]
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

# test jednostkowy dla metody iou
lista1 = [1, 3, 5, 7, 9]
lista2 = [1, 4, 7, 10]

print(iou(lista1, lista2))