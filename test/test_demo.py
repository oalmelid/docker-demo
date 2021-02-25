import pytest
import pyranges as pr

from demo.demo import intersect
from pandas.testing import assert_frame_equal


def test_intersect_overlapping_frames():
    frame_1 = pr.from_dict({"Chromosome": [1, 2], "Start": [1, 10], "End": [4, 15]})
    frame_2 = pr.from_dict({"Chromosome": [1, 2], "Start": [2, 16], "End": [7, 18]})

    expected_result = pr.from_dict({"Chromosome": [1], "Start": [2], "End": [4]})
    intersection = intersect([frame_1, frame_2])

    assert_frame_equal(
        intersection.df, expected_result.df, check_dtype=False, check_categorical=False
    )
