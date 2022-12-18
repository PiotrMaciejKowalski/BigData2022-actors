import pytest
from lib.similarity_utils import iou


def test_iou_proper_lists():
    assert iou(["a", "b", "c", "d", "e", "f"], ["a", "c", "e", "g", "i"]) == (
        3 / 8
    ), f"should be {3/8}"


def test_iou_one_proper_list():
    assert iou(["a", "b", "c", "d", "e", "f"], []) == 0, "should be 0"


def test_iou_two_improper_lists():
    assert iou([], []) == 0, "should be 0"


def test_iou_the_same_lists():
    assert (
        iou(["a", "b", "c", "d", "e", "f"], ["a", "b", "c", "d", "e", "f"]) == 1
    ), "should be 1"
