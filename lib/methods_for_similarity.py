import numpy as np

def IOU(lista1, lista2):
  # metoda przyjmuje jako argument dwie listy i zwraca ich indeks Jaccarda, czyli liczbę z przedzialu [0,1]
  intersection = np.intersect1d(lista1, lista2)
  union = np.union1d(lista1, lista2)
  IOU = len(intersection)/len(union)
  return IOU