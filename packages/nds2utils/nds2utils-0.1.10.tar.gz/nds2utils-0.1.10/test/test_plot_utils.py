"""test_data_utils.py

Tests the functions in nds2utils/data_utils.py
Does not test any nds2 functionality.
"""

# unintuitive import of nds2utils/data_utils.py :((
import os
import sys

import pytest

SCRIPT_PATH = os.path.dirname(__file__)  # full path to this script
FIG_DIR = os.path.join(SCRIPT_PATH, "figures")
GIT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, ".."))  # Get top git repo dir

sys.path.append(GIT_DIR)

import matplotlib as mpl
import matplotlib.pyplot as plt
import nds2utils as nu
import numpy as np


# @pytest.fixture()
def set_up_basic_data_dict():
    """Sets up a basic data_dict for testing data_dict functions."""
    # Assemble
    fs = 2**4  # Hz
    duration = 10  # s
    number_of_samples = duration * fs

    aa = np.random.randn(number_of_samples)
    nn = np.random.randn(number_of_samples)
    bb = aa + 0.5 * nn

    data_dict = nu.load_data_to_dict_directly("aa", aa, fs, duration, data_dict=None)
    data_dict = nu.load_data_to_dict_directly(
        "bb", bb, fs, duration, data_dict=data_dict
    )

    return data_dict


@pytest.mark.parametrize(
    ("ylims", "answer"),
    [
        ([0.02, 123], np.array([1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3])),
        ([1e-1, 1e1], np.array([1e-1, 1e0, 1e1])),
        (
            [3e-7, 3e12],
            np.array(
                [
                    1e-07,
                    1e-06,
                    1e-05,
                    1e-04,
                    1e-03,
                    1e-02,
                    1e-01,
                    1e00,
                    1e01,
                    1e02,
                    1e03,
                    1e04,
                    1e05,
                    1e06,
                    1e07,
                    1e08,
                    1e09,
                    1e10,
                    1e11,
                    1e12,
                    1e13,
                ]
            ),
        ),
    ],
)
def test_good_ticks(ylims, answer):
    fig, s1 = plt.subplots(1)
    s1.set_ylim(ylims)
    yticks = nu.good_ticks(s1)

    assert all(yticks == answer)
