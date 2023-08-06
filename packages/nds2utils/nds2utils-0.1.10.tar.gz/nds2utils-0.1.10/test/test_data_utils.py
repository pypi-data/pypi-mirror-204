"""test_data_utils.py

Tests the functions in nds2utils/data_utils.py
Does not test any nds2 functionality.
"""

# unintuitive import of nds2utils/data_utils.py :((
import os
import sys

import pytest

SCRIPT_PATH = os.path.dirname(__file__)  # full path to this script
GIT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, ".."))  # Get top git repo dir

sys.path.append(GIT_DIR)

import nds2utils as nu
import numpy as np

print(f"nds2utils.version == {nu.version}")
print()


# @pytest.fixture()
def set_up_basic_data_dict():
    """Sets up a basic data_dict for testing data_dict functions."""
    # Assemble
    fs = 2**4  # Hz
    fs_cc = 2 * fs

    duration = 10  # s

    number_of_samples = duration * fs
    number_of_samples_cc = duration * fs_cc

    aa = np.random.randn(number_of_samples)
    nn = np.random.randn(number_of_samples)
    bb = aa + 0.5 * nn

    cc = np.random.randn(number_of_samples_cc)

    data_dict = nu.load_data_to_dict_directly("aa", aa, fs, duration, data_dict=None)
    data_dict = nu.load_data_to_dict_directly(
        "bb", bb, fs, duration, data_dict=data_dict
    )
    data_dict = nu.load_data_to_dict_directly(
        "cc", cc, fs_cc, duration, data_dict=data_dict
    )

    return data_dict


### Tests
@pytest.mark.parametrize(
    ("db", "mag"),
    [(-40, 0.01), (-20, 0.1), (0, 1.0), (20, 10.0), (40, 100.0), (10, 3.162278)],
)
def test_db_to_mag(db, mag):
    assert np.isclose(nu.db_to_mag(db), mag, rtol=1e-6, atol=0)


@pytest.mark.parametrize(
    ("db", "mag"),
    [(-40, 0.01), (-20, 0.1), (0, 1.0), (20, 10.0), (40, 100.0), (10, 3.162278)],
)
def test_mag_to_db(db, mag):
    assert np.isclose(db, nu.mag_to_db(mag), rtol=1e-6, atol=0)


@pytest.mark.parametrize(
    ("qq", "f0"),
    [(100, 10)],
)
def test_complex_pole_pair_conjugates(qq, f0):
    poles = nu.complex_pole_pair(qq, f0)
    assert poles[0] == np.conjugate(poles[1])


@pytest.mark.parametrize(
    ("qq", "f0"),
    [(100, 10)],
)
def test_complex_pole_pair_frequencies(qq, f0):
    poles = nu.complex_pole_pair(qq, f0)
    # get imaginary part
    imag = np.abs(np.imag(poles[0]))
    assert np.isclose(f0, imag, rtol=1e-6, atol=0)


@pytest.mark.parametrize(
    ("qq", "f0"),
    [(100, 10)],
)
def test_complex_pole_pair_quality_factor(qq, f0):
    poles = nu.complex_pole_pair(qq, f0)
    # get imaginary part
    real = np.real(poles[0])
    assert np.isclose(1 / (2 * qq), real, rtol=1e-6, atol=0)


def test_save_load_pickle():
    # Assemble
    data_dict = set_up_basic_data_dict()

    # Act
    savefile = os.path.join(SCRIPT_PATH, "test_save_load_pickle.pkl")
    nu.save_pickle(data_dict, savefile)

    load_dict = nu.load_pickle(savefile)

    # Test
    bools = []
    for chan in data_dict.keys():
        for key in data_dict[chan].keys():
            if key == "data":
                temp = all(load_dict[chan][key] == data_dict[chan][key])
            else:
                temp = load_dict[chan][key] == data_dict[chan][key]
            bools.append(temp)

    # Cleanup
    os.remove(savefile)

    assert all(bools)


def test_save_load_hdf5():
    # Assemble
    data_dict = set_up_basic_data_dict()

    # Act
    savefile = os.path.join(SCRIPT_PATH, "test_save_load_hdf5.hdf5")
    nu.save_hdf5(data_dict, savefile)

    load_dict = nu.load_hdf5(savefile)

    # Test
    bools = []
    for chan in data_dict.keys():
        for key in data_dict[chan].keys():
            if key == "data":
                temp = all(load_dict[chan][key] == data_dict[chan][key])
            else:
                temp = load_dict[chan][key] == data_dict[chan][key]
            bools.append(temp)

    # Cleanup
    os.remove(savefile)

    assert all(bools)


@pytest.mark.parametrize(
    ("averages", "bandwidth", "overlap", "answer"),
    [
        (100, 1, 0, 100),
        (100, 0.1, 0, 1000),
        (100, 1, 0.5, 50.5),
        (100, 0.1, 0.5, 505),
        (200, 1, 0.5, 100.5),
    ],
)
def test_dtt_time(averages, bandwidth, overlap, answer):
    duration = nu.dtt_time(averages, bandwidth, overlap)
    assert duration == answer


@pytest.mark.parametrize(
    ("duration", "bandwidth", "overlap", "answer"),
    [
        (100, 1, 0, 100),
        (1000, 0.1, 0, 100),
        (50.5, 1, 0.5, 100),
        (505, 0.1, 0.5, 100),
        (100.5, 1, 0.5, 200),
        (10, 0.123, 0.3, 1),
        (10, 3, 0.5, 59),
    ],
)
def test_dtt_averages(duration, bandwidth, overlap, answer):
    averages = nu.dtt_averages(duration, bandwidth, overlap)
    assert averages == answer


@pytest.mark.parametrize(
    ("averages", "overlap", "answer"),
    [
        (10, 0, 0.1),
        (100, 0, 0.01),
        (1000, 0.5, 0.002),
    ],
)
def test_minimum_coherent_power(averages, overlap, answer):
    mcp = nu.minimum_coherent_power(averages, overlap)
    assert mcp == answer


@pytest.mark.parametrize(
    ("channels", "answer"),
    [
        (["aa", "bb", "cc"], True),
        (["aa", "bb", "cc", "dd"], False),
        (["aa", "bb"], True),
    ]
)
def test_check_loaded_data_dict_channels(channels, answer):
    # Assemble
    data_dict = set_up_basic_data_dict()

    # Test
    check = nu.check_loaded_data_dict(data_dict, channels)

    assert check == answer


def test_check_loaded_data_dict_is_none():
    # Assemble
    data_dict = None
    channels = ["aa", "bb", "cc"]

    # Test
    check = nu.check_loaded_data_dict(data_dict, channels)

    assert not check


def test_check_loaded_data_dict_is_nan():
    # Assemble
    data_dict = set_up_basic_data_dict()

    # change one data point to a nan
    data_dict["aa"]["data"][0] = np.nan

    # just some channels
    channels = ["aa", "bb", "cc"]

    # Test
    check = nu.check_loaded_data_dict(data_dict, channels)

    assert not check


###############################
#   Skip the nds2 functions   #
###############################


@pytest.mark.parametrize(
    "bandwidth",
    [
        1,
        3,
        0.123,
        0.01,
    ],
)
def test_check_sampling_frequency_vs_bandwidth(bandwidth):
    # Assemble
    data_dict = set_up_basic_data_dict()

    # Act
    new_bandwidth = nu.check_sampling_frequency_vs_bandwidth(data_dict, bandwidth)

    # Test
    test_pass = False
    if new_bandwidth == bandwidth:
        test_pass = True

    if not test_pass:
        # make sure the bandwidth is an integer multiple of the new_bandwidth
        fs = data_dict["aa"]["fs"]
        ratio = fs / new_bandwidth
        if int(ratio) == ratio:
            test_pass = True

    assert test_pass


@pytest.mark.parametrize(
    ("averages", "bandwidth", "overlap"),
    [
        (100, 1, 0),
        (1000, 0.1, 0),
        (50.5, 1, 0.5),
        (505, 0.1, 0.5),
        (100.5, 1, 0.5),
        (10, 0.123, 0.3),
        (10, 3, 0.5),
    ],
)
def test_check_duration(averages, bandwidth, overlap):
    # Assemble
    data_dict = set_up_basic_data_dict()
    actual_duration = data_dict["aa"]["duration"]

    # Act
    new_duration = nu.check_duration(data_dict, averages, bandwidth, overlap)

    # Test
    test_pass = False
    if new_duration == actual_duration:
        test_pass = True

    if not test_pass:
        requested_duration = nu.dtt_time(averages, bandwidth, overlap)
        if new_duration == requested_duration:
            test_pass = True

    assert test_pass


### Test calc_psds
@pytest.mark.parametrize(
    ("bandwidth", "overlap"),
    [
        (1, 0),
    ],
)
def test_calc_psds_keys(bandwidth, overlap):
    # Assemble
    data_dict = set_up_basic_data_dict()
    duration = data_dict["aa"]["duration"]
    averages = nu.dtt_averages(duration, bandwidth, overlap)

    # Act
    data_dict = nu.calc_psds(data_dict, averages, bandwidth, overlap)

    # Test
    intended_nested_keys = np.array(
        [
            "data",
            "fs",
            "gpsStart",
            "duration",
            "averages",
            "binwidth",
            "overlap",
            "ff",
            "PSD",
            "df",
            "fft_time",
            "nperseg",
        ]
    )
    bools = []
    for chan in data_dict.keys():
        for key in data_dict[chan].keys():
            temp = False
            if key in intended_nested_keys:
                temp = True
            bools.append(temp)

    assert all(bools)


@pytest.mark.parametrize(
    ("bandwidth", "overlap"),
    [
        (1, 0),
        (0.1, 0),
        (0.123, 0.3),
        (3, 0.5),
    ],
)
def test_calc_psds_binwidths(bandwidth, overlap):
    # Assemble
    data_dict = set_up_basic_data_dict()
    duration = data_dict["aa"]["duration"]
    averages = nu.dtt_averages(duration, bandwidth, overlap)

    # Act
    data_dict = nu.calc_psds(data_dict, averages, bandwidth, overlap)

    # Test
    bools = []
    for chan in data_dict.keys():
        temp = False
        # reset bandwidth if necessary
        new_bandwidth = nu.check_sampling_frequency_vs_bandwidth(data_dict, bandwidth)
        if np.isclose(data_dict[chan]["df"], new_bandwidth, rtol=1e-6):
            temp = True
        bools.append(temp)

    assert all(bools)


@pytest.mark.parametrize(
    ("bandwidth", "overlap"),
    [
        (2, 0),
    ],
)
def test_calc_psds_psds(bandwidth, overlap):
    # Assemble
    data_dict = set_up_basic_data_dict()

    duration = data_dict["aa"]["duration"]
    averages = nu.dtt_averages(duration, bandwidth, overlap)
    
    fs = data_dict["aa"]["fs"]
    fs_cc = data_dict["cc"]["fs"]

    psd_aa = 5.0 # V**2 / Hz
    psd_cc = 10.0 # V**2 / Hz

    std_aa = nu.convert_density_to_std(psd_aa, fs)
    std_cc = nu.convert_density_to_std(psd_cc, fs_cc)

    data_dict["aa"]["data"] *= std_aa
    data_dict["cc"]["data"] *= std_cc

    # Act
    data_dict = nu.calc_psds(data_dict, averages, bandwidth, overlap)

    # Test
    ff = data_dict["aa"]["ff"]
    indices = np.argwhere(ff >= fs / 4)[:,0]
    indices_cc = np.argwhere(ff >= fs_cc / 4)[:,0]

    index = indices[0]
    index_cc = indices_cc[0]

    estimated_psd_aa = data_dict["aa"]["PSD"][index]
    estimated_psd_cc = data_dict["cc"]["PSD"][index_cc]

    estimated_psd_variance_aa = estimated_psd_aa**2 / averages # Eq D.12 of my thesis
    estimated_psd_variance_cc = estimated_psd_cc**2 / averages # Eq D.12 of my thesis

    estimated_psd_std_aa = np.sqrt( estimated_psd_variance_aa )
    estimated_psd_std_cc = np.sqrt( estimated_psd_variance_cc )

    # Results
    bools = []
    temp = False
    # check if within 5 sigma
    if np.isclose(psd_aa, estimated_psd_aa, atol=5 * estimated_psd_std_aa):
        temp = True
    else:
        print(f"fs = {fs}")
        print(f"averages = {averages}")
        print(f"index = {index}")
        print(f"psd_aa = {psd_aa} V**2/Hz")
        print(f"estimated_psd_aa = {estimated_psd_aa} V**2/Hz")
        print(f"estimated_psd_std_aa = {estimated_psd_std_aa} V**2/Hz")
    bools.append(temp)

    temp = False
    if np.isclose(psd_cc, estimated_psd_cc, atol=5 * estimated_psd_std_cc):
        temp = True
    else:
        print(f"fs_cc = {fs_cc}")
        print(f"averages = {averages}")
        print(f"index_cc = {index_cc}")
        print(f"psd_cc = {psd_cc} V**2/Hz")
        print(f"estimated_psd_cc = {estimated_psd_cc} V**2/Hz")
        print(f"estimated_psd_std_cc = {estimated_psd_std_cc} V**2/Hz")
    bools.append(temp)

    assert all(bools)

@pytest.mark.parametrize(
    ("bandwidth", "overlap"),
    [
        (1, 0),
    ],
)
def test_calc_csds_keys(bandwidth, overlap):
    # Assemble
    data_dict = set_up_basic_data_dict()

    duration = data_dict["aa"]["duration"]
    averages = nu.dtt_averages(duration, bandwidth, overlap)

    # Act
    data_dict = nu.calc_csds(data_dict, averages, bandwidth, overlap, make_tfs=False)

    # Test
    channels = list(data_dict.keys())
    intended_nested_keys = np.array(
        [
            "data",
            "fs",
            "gpsStart",
            "duration",
            "averages",
            "binwidth",
            "overlap",
            "ff",
            "PSD",
            "df",
            "fft_time",
            "nperseg",
        ]
    )
    secondary_intended_nested_keys = np.array(
        [
            "ff",
            "CSD",
        ]
    )
    decimation_keys = np.array(
        [
            "fs",
            "ff",
            "PSD",
            "df",
        ]
    )


    bools = []
    for chan in data_dict.keys():
        print()
        print(f"chan = {chan}")
        for key in data_dict[chan].keys():
            print(f"key = {key}", end="  ")
            temp = False
            # Usual PSD keys
            if key in intended_nested_keys:
                temp = True
                
            # CSD keys
            elif key in channels:
                temp = True
                
                for key2 in data_dict[chan][key].keys():
                    print(f"key2 = {key2}", end="  ")
                    temp2 = False
                    if key2 in secondary_intended_nested_keys:
                        temp2 = True
                    bools.append(temp2)

            elif key == "decimation":
                for new_fs in data_dict[chan][key].keys():
                    print(f"new_fs = {new_fs}", end="  ")
                    for key3 in data_dict[chan][key][new_fs].keys():
                        temp3 = False
                        print(f"key3 = {key3}", end="  ")
                        if key3 in decimation_keys:
                            temp3 = True
                            bools.append(temp3)

                temp = True

            print()
            bools.append(temp)

    assert all(bools)
