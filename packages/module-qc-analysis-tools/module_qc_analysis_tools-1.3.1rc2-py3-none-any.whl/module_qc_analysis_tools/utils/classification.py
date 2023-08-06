#!/usr/bin/env python3
from __future__ import annotations

import logging

import numpy as np

from module_qc_analysis_tools.utils.misc import bcolors

log = logging.getLogger(__name__)
log.setLevel("INFO")


def format_text_short():
    return " {:^30}: {:^20}"


testbit_map = {
    "DEAD_DIGITAL": 0,
    "BAD_DIGITAL": 1,
    "DEAD_ANALOG": 2,
    "BAD_ANALOG": 3,
    "THRESHOLD_FAILED_FITS": 4,
    "TUNING_BAD": 5,
    "HIGH_ENC": 6,
    "HIGH_NOISE": 7,
    "TOT_MEM": 8,
    "HIGH_XTALK": 9,
}


def get_fail_bit(name):
    if name not in testbit_map:
        log.error(
            bcolors.BADRED
            + f"Asking for bit for {name}, but {name} not present in {testbit_map} - please check!"
            + bcolors.ENDC
        )
        raise RuntimeError()
    return testbit_map.get(name)


def get_name_from_bit(bit):
    try:
        index = list(testbit_map.values()).index(bit)
        name = list(testbit_map.keys())[index]
        return name
    except Exception as err:
        log.error(
            bcolors.BADRED
            + f"Problem finding test name for bit {bit}, please check test name - bit mapping"
            + bcolors.ENDC
        )
        raise RuntimeError() from err


def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def format_pixel_input(data):
    data = np.array(data).transpose()
    num_rows, num_cols = data.shape
    data = data.flatten()
    pix_index = np.empty(1)
    pix_index = np.arange(0, 400, dtype=int)
    for r in range(1, num_rows):
        pix_index = np.append(pix_index, np.arange(r * 400, r * 400 + 400, dtype=int))
    return data, pix_index


def format_config_input(config):
    data = config[0].get("TDAC")
    pix_index = np.arange(0, 384 * 400, 400, dtype=int)
    for c in range(1, len(config)):
        data = np.append(data, config[c].get("TDAC"))
        pix_index = np.append(pix_index, np.arange(c, 384 * 400 + c, 400, dtype=int))
    return data, pix_index


def check_test_method(test_method, test_params):
    if test_method == "MinBound":
        if len(test_params) != 1:
            log.error(
                bcolors.BADRED + "MinBound cut requested, but ",
                len(test_params),
                " params provided! Please only provide single lower bound"
                + bcolors.ENDC,
            )
            raise RuntimeError()
    elif test_method == "MaxBound":
        if len(test_params) != 1:
            log.error(
                bcolors.BADRED + "MaxBound cut requested, but ",
                len(test_params),
                " params provided! Please only provide single upper bound"
                + bcolors.ENDC,
            )
            raise RuntimeError()
    elif test_method == "MinMaxBound":
        if len(test_params) != 2:
            log.error(
                bcolors.BADRED + "MinMaxBound cut requested, but ",
                len(test_params),
                " params provided! Please only provide single lower and upper params"
                + bcolors.ENDC,
            )
            raise RuntimeError()
    elif test_method == "RemoveOneValue":
        if len(test_params) != 1:
            log.error(
                bcolors.BADRED + "RemoveOneValue cut requested, but ",
                len(test_params),
                " params provided! Please only provide single value to remove"
                + bcolors.ENDC,
            )
            raise RuntimeError()
    elif test_method == "Outlier":
        if len(test_params) != 1:
            log.error(
                bcolors.BADRED + "Outlier cut requested, but ",
                len(test_params),
                " params provided! Please only provide single value to determine outliers"
                + bcolors.ENDC,
            )
            raise RuntimeError()
    elif test_method == "percentile":
        if len(test_params) != 1:
            log.error(
                bcolors.BADRED + "Percentile cut requested, but ",
                len(test_params),
                " params provided! Please only provide single percentile"
                + bcolors.ENDC,
            )
            raise RuntimeError()
    else:
        log.error(
            bcolors.BADRED
            + f"Method {test_method} not recognized. Skipping"
            + bcolors.ENDC
        )
        return -1
    return 0


def check_record(record_fail, test_name):
    test_bit = set_bit(0, get_fail_bit(test_name))
    return record_fail & test_bit == test_bit


def count_pixels(fail, fail_record, test_names):
    log.info("")
    log.info("Classifying pixel failures!")
    log.info("")
    # Counts pixels that have been classified
    failures = {}
    total_failures = 0
    for t in testbit_map:
        # Skip tests that do not classify pixels
        if t not in test_names:
            log.debug(
                bcolors.WARNING
                + f"count_pixels: {t} not used to classify pixels, skipping "
                + bcolors.ENDC
            )
            continue

        # Only store results that were recorded
        if not check_record(fail_record, t):
            log.debug(
                bcolors.WARNING
                + f"count_pixels: {t} not checked, skipping "
                + bcolors.ENDC
            )
            continue

        failures.update({t: {}})
        fail_bit = set_bit(0, get_fail_bit(t))

        nfail_independent = len(fail[fail & fail_bit == fail_bit])
        failures.get(t).update({"independent": nfail_independent})

        # Count how many pixels have failed this test, and passed all previous tests
        test_bit = 0
        for i in range(0, get_fail_bit(t) + 1):
            if not check_record(fail_record, get_name_from_bit(i)):
                continue
            test_bit = set_bit(test_bit, i)
        nfail_dependent = len(fail[fail & test_bit == fail_bit])
        failures.get(t).update({"dependent": nfail_dependent})
        total_failures += nfail_dependent
        failures.get(t).update({"integrated": total_failures})
    return failures

    # Count failures
    test_bit = set_bit(0, fail_bit)
    return None


def classify_pixels(data, fail, record, test_name, test_method, test_params):
    pix_fail = np.copy(fail)
    fail_bit = get_fail_bit(test_name)

    # Check pixel classification
    error_code = check_test_method(test_method, test_params)
    if error_code:
        return error_code

    # Identify failures
    if test_method == "MinBound":
        failures = np.where(data < test_params[0])

    elif test_method == "MaxBound":
        failures = np.where(data > test_params[0])

    elif test_method == "MinMaxBound":
        failures = np.where((data < test_params[0]) | (data > test_params[1]))

    elif test_method == "RemoveOneValue":
        failures = np.where(data == test_params[0])

    elif test_method == "Outlier":
        mean = np.mean(data)
        failures = np.where(np.abs(data - mean) > test_params[0])

    # Record failures
    record = set_bit(record, fail_bit)
    for f in failures:
        pix_fail[f] = set_bit(fail[f], fail_bit)

    return pix_fail, record


def print_pixel_classification(failure_summary):
    txt = format_text_short()
    log.info(txt.format("Classification", "Number of pixels"))
    log.info("------------------------------------------------------------------")
    for criteria, failures in failure_summary.items():
        log.info(txt.format(criteria, round(failures.get("dependent"), 3)))
    log.info("------------------------------------------------------------------")
    log.info(
        txt.format(
            "TOTAL FAILING", list(failure_summary.values())[-1].get("integrated")
        )
    )
    log.info("------------------------------------------------------------------")
