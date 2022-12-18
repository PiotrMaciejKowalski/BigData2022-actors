import pytest
from lib.similarity_utils import pokrycie_przedzialow


def test_pokr_przed_sub_interval():
    assert pokrycie_przedzialow([0, 10], [5, 10]) == 0.5, 'should be 0.5'


def test_pokr_przed_any_intervals():
    assert pokrycie_przedzialow([1500, 2000], [1000, 1700]) == 0.2, 'should be 0.2'


def test_pokr_przed_excluded_intervals():
    assert pokrycie_przedzialow([150, 200], [200, 300]) == 0, 'should be 0'


def test_pokr_przed_the_same_intervals():
    assert pokrycie_przedzialow([1000, 1100], [1000, 1100]) == 1, 'should be 1'