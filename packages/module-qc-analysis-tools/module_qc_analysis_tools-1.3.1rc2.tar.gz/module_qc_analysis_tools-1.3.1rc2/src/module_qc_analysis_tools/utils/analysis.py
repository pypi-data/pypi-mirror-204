#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np

from module_qc_analysis_tools.utils.misc import bcolors, getImuxMap, getVmuxMap

log = logging.getLogger(__name__)
log.setLevel("INFO")


def format_text():
    return " {:^30}: {:^20}: {:^20}: {:^5}"


def format_text_short():
    return " {:^30}: {:^20}:"


def print_output_pass(key, results, lower_bound, upper_bound):
    txt = format_text()
    log.info(
        bcolors.OKGREEN
        + txt.format(
            key,
            round(results, 4),
            f"[{lower_bound}, {upper_bound}]",
            "PASS",
        )
        + bcolors.ENDC
    )


def print_output_fail(key, results, lower_bound, upper_bound):
    txt = format_text()
    log.info(
        bcolors.BADRED
        + txt.format(
            key,
            round(results, 4),
            f"[{lower_bound}, {upper_bound}]",
            "FAIL",
        )
        + bcolors.ENDC
    )


def print_output_neutral(key, results):
    txt = format_text_short()
    log.info(bcolors.WARNING + txt.format(key, round(results, 4)) + bcolors.ENDC)


def get_layer(layer):
    layers = {"L0": "LZero", "L1": "LOne", "L2": "LTwo"}
    return layers.get(layer)


def check_layer(layer):
    possible_layers = ["L0", "L1", "L2"]
    if layer not in possible_layers:
        log.error(
            bcolors.ERROR
            + f" Layer '{layer}' not recognized or not provided. Provide the layer with the --layer [L0, L1, or L2] option."
            + bcolors.ENDC
        )
        sys.exit(-1)


def get_n_chips(layer):
    check_layer(layer)
    chips_per_layer = {"L0": 3, "L1": 4, "L2": 4}
    return chips_per_layer.get(layer)


# The following hardcoded values are from https://gitlab.cern.ch/atlas-itk/pixel/module/itkpix-electrical-qc
def get_nominal_current(layer, nchips):
    check_layer(layer)
    # Assumes triplets for L0, quads for L1-L2
    currents_per_chip = {
        "L0": 1.85,
        "L1": 1.65,
        "L2": 1.47,
    }
    return currents_per_chip.get(layer) * nchips


def get_nominal_Voffs(layer, lp_mode=False):
    check_layer(layer)
    Voffs = {
        "L0": 1.1,
        "L1": 1.0,
        "L2": 1.0,
    }
    Voffs_lp = {
        "L0": 1.38,
        "L1": 1.38,
        "L2": 1.38,
    }
    if lp_mode:
        return Voffs_lp.get(layer)

    return Voffs.get(layer)


def get_nominal_RextA(layer):
    check_layer(layer)
    RextA = {
        "L0": 511,
        "L1": 732,
        "L2": 866,
    }
    return RextA.get(layer)


def get_nominal_RextD(layer):
    check_layer(layer)
    RextD = {"L0": 407, "L1": 549, "L2": 590}
    return RextD.get(layer)


# Function to get key from value in muxMaps
def get_key(mydict, val):
    for key, value in mydict.items():
        if val == value:
            return key
    return -1


def perform_qc_analysis_AR_NOMINAL_SETTINGS(
    _test_type, qc_config, _layer_name, results, verbosity="INFO"
):
    log.setLevel(verbosity)
    # QC analysis for AR_NOMINAL_SETTINGS

    passes_qc_overall = True
    VmuxMap = getVmuxMap()
    ImuxMap = getImuxMap()
    if len(VmuxMap.keys()) + len(ImuxMap.keys()) != len(results):
        log.error(
            bcolors.ERROR
            + " Number of entries in AR_NOMINAL_SETTINGS results does not match number of entries in VmuxMap and ImuxMap - there should be one entry for every Vmux and Imux in those maps. Please fix and re-run!"
            + bcolors.ENDC
        )
        return -1
    for key, value in qc_config.items():
        log.debug(f" QC selections for {key}: {value}")
        try:
            lower_bound = value[0]
            upper_bound = value[1]
        except Exception:
            log.error(
                bcolors.ERROR
                + f" QC selections for {key} are ill-formatted, should be list of length 2! Please fix: {value} . Skipping."
                + bcolors.ENDC
            )
            continue

        passes_qc_test = True
        if get_key(ImuxMap, key) != -1:
            index = get_key(ImuxMap, key)
        elif get_key(VmuxMap, key) != -1:
            index = get_key(VmuxMap, key) + len(ImuxMap.keys())
        else:
            log.error(
                bcolors.ERROR
                + f"Did not find {key} in VmuxMap or ImuxMap - please check!"
                + bcolors.ENDC
            )
            continue
        log.debug(f" Key is {key}, value is {value}, index is {index}")

        if (results[index] < lower_bound) or (results[index] > upper_bound):
            passes_qc_test = False
        if passes_qc_test:
            print_output_pass(key, results[index], lower_bound, upper_bound)
        else:
            print_output_fail(key, results[index], lower_bound, upper_bound)
        passes_qc_overall = passes_qc_overall and passes_qc_test

    return passes_qc_overall


def perform_qc_analysis_AR_VDD_Trim(
    _test_type, qc_config, _layer_name, results, key, verbosity="INFO"
):
    log.setLevel(verbosity)
    # QC analysis for VDDA_VS_TRIM and VDDD_VS_TRIM
    pass_vdd_vs_trim_test = True

    # Fist VDD value must satisfy requirements
    tmp_pass_qc = True
    lower_bound_vdd = qc_config.get("VDD_TRIM_0")[0]
    upper_bound_vdd = qc_config.get("VDD_TRIM_0")[1]
    if (results[0] < lower_bound_vdd) or (results[0] > upper_bound_vdd):
        tmp_pass_qc = False
    if tmp_pass_qc:
        print_output_pass(f"{key}_0", results[0], lower_bound_vdd, upper_bound_vdd)
    else:
        print_output_fail(f"{key}_0", results[0], lower_bound_vdd, upper_bound_vdd)
    pass_vdd_vs_trim_test = pass_vdd_vs_trim_test and tmp_pass_qc

    # The trim step size (change in voltage per DAC step) must satisfy requirements
    VDD_dV_list = np.diff(np.array(results))
    lower_bound_dv = qc_config.get("VDD_step_size")[0]
    upper_bound_dv = qc_config.get("VDD_step_size")[1]
    dV_fail = (VDD_dV_list < lower_bound_dv) | (VDD_dV_list > upper_bound_dv)
    pass_vdd_vs_trim_test = pass_vdd_vs_trim_test and np.any(dV_fail)
    for i in range(len(VDD_dV_list)):
        tmp_pass_qc = not dV_fail[i]
        if tmp_pass_qc:
            print_output_pass(
                f"{key}_{i+1}_STEP_SIZE", VDD_dV_list[i], lower_bound_dv, upper_bound_dv
            )
        else:
            print_output_fail(
                f"{key}_{i+1}_STEP_SIZE", VDD_dV_list[i], lower_bound_dv, upper_bound_dv
            )

    return pass_vdd_vs_trim_test


def perform_qc_analysis(test_type, qc_config, layer_name, results, verbosity="INFO"):
    log.setLevel(verbosity)
    log.info("")
    log.info("Performing QC analysis!")
    log.info("")

    qc_selections = qc_config[test_type]
    check_qc_selections = qc_selections.copy()

    check_layer(layer_name)
    layer = get_layer(layer_name)

    passes_qc_overall = True
    txt = format_text()
    log.info(txt.format("Parameter", "Analysis result", "QC criteria", "Pass"))
    log.info(
        "--------------------------------------------------------------------------------------"
    )

    for key in results:
        if not qc_selections.get(key):
            log.debug(
                bcolors.WARNING
                + f" Selection for {key} not found in QC file! Skipping."
                + bcolors.ENDC
            )
            print_output_neutral(key, results.get(key))
            continue
        check_qc_selections.pop(key)

        # Handle AR_NOMINAL_SETTINGS in completely different function, for now...
        if key == "AR_NOMINAL_SETTINGS":
            passes_qc_test = perform_qc_analysis_AR_NOMINAL_SETTINGS(
                test_type,
                qc_selections.get(key),
                layer_name,
                results.get(key),
                verbosity,
            )
            passes_qc_overall = passes_qc_overall and passes_qc_test
            continue

        # Handle AR_VDDA_VS_TRIM and AR_VDD_VS_TRIM separately
        if ("AR_VDDA_VS_TRIM" in key) or ("AR_VDDD_VS_TRIM" in key):
            passes_qc_test = perform_qc_analysis_AR_VDD_Trim(
                test_type,
                qc_selections.get(key),
                layer_name,
                results.get(key),
                key,
                verbosity,
            )
            passes_qc_overall = passes_qc_overall and passes_qc_test
            continue

        log.debug(f" QC selections for {key}: {qc_selections.get(key)}")
        if type(qc_selections.get(key)) is list:
            if len(qc_selections.get(key)) != 2:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} are ill-formatted, should be list of length 2! Please fix: {qc_selections.get(key)} . Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = qc_selections.get(key)[0]
            upper_bound = qc_selections.get(key)[1]
        elif type(qc_selections.get(key)) is dict:
            layer_bounds = qc_selections.get(key).get(layer)
            if not layer_bounds:
                log.error(
                    bcolors.ERROR
                    + f" QC selections for {key} and {layer} do not exist - please check! Skipping."
                    + bcolors.ENDC
                )
                continue
            lower_bound = layer_bounds[0]
            upper_bound = layer_bounds[1]

        passes_qc_test = True
        if (results.get(key) < lower_bound) or (results.get(key) > upper_bound):
            passes_qc_test = False
        if passes_qc_test:
            print_output_pass(key, results.get(key), lower_bound, upper_bound)
        else:
            print_output_fail(key, results.get(key), lower_bound, upper_bound)
        passes_qc_overall = passes_qc_overall and passes_qc_test
    if len(check_qc_selections) > 0:
        for key in check_qc_selections:
            log.error(
                bcolors.ERROR
                + f" Parameter from chip for QC selection of {key} was not passed to analysis - please fix!"
                + bcolors.ENDC
            )
        passes_qc_overall = False
    log.info(
        "--------------------------------------------------------------------------------------"
    )

    return passes_qc_overall


def submit_results(
    outputDF, timestamp, site="Unspecified", outputfile="submit.txt", layer="Unknown"
):
    results = outputDF.get("results")

    # Temporary solution to avoid error when indexing array that doesn't exist
    if not results.get("AR_VDDA_VS_TRIM"):
        results.update({"AR_VDDA_VS_TRIM": [-1] * 16})
    if not results.get("AR_VDDD_VS_TRIM"):
        results.update({"AR_VDDD_VS_TRIM": [-1] * 16})
    if not results.get("AR_NOMINAL_SETTINGS"):
        results.update({"AR_NOMINAL_SETTINGS": [-1] * 72})
    analysis_version = results.get("property").get("ANALYSIS_VERSION")
    meas_version = results.get("Metadata").get("MEASUREMENT_VERSION")

    url = {
        "ADC_CALIBRATION": f"https://docs.google.com/forms/d/e/1FAIpQLSegDYRQ1Foe5eTuSOVZUXe0d1f_Bh5v3rhsffCnu9DUDFR69A/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.1282466276={outputDF.get('passed')}\
	&entry.141409196={analysis_version}\
	&entry.1579707472={meas_version}\
	&entry.913205750={layer}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.802167553={site}\
	&entry.1592726943={results.get('ADC_CALIBRATION_SLOPE')}\
	&entry.422835427={results.get('ADC_CALIBRATION_OFFSET')}",
        "VCAL_CALIBRATION": f"https://docs.google.com/forms/d/e/1FAIpQLSenLUdLpaHLssp-jdUf1YvqiWvR8WOAkhrpQgfBlZYTWWRNog/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.796846737={outputDF.get('passed')}\
	&entry.1436190418={analysis_version}\
	&entry.463035701={meas_version}\
	&entry.74191116={layer}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.802167553={site}\
	&entry.1592726943={results.get('VCAL_MED_SLOPE')}\
	&entry.422835427={results.get('VCAL_MED_OFFSET')}\
	&entry.424316677={results.get('VCAL_MED_SLOPE_SMALL_RANGE')}\
	&entry.2055663117={results.get('VCAL_MED_OFFSET_SMALL_RANGE')}\
	&entry.1630084203={results.get('VCAL_HIGH_SLOPE')}\
	&entry.1107555352={results.get('VCAL_HIGH_OFFSET')}\
	&entry.1994936328={results.get('VCAL_HIGH_SLOPE_SMALL_RANGE')}\
	&entry.524584120={results.get('VCAL_HIGH_OFFSET_SMALL_RANGE')}",
        "INJECTION_CAPACITANCE": f"https://docs.google.com/forms/d/e/1FAIpQLSfHpq9pjuzgYvjUU8ZHapzCOrIHzyJx3xirJunGEtBO2COYGw/formResponse?usp=pp_url\
	&entry.1920584355={timestamp}\
	&entry.346685867={outputDF.get('passed')}\
	&entry.2076657244={analysis_version}\
	&entry.2143111336={meas_version}\
	&entry.1736672890={layer}\
	&entry.104853658={outputDF.get('serialNumber')}\
	&entry.802167553={site}\
	&entry.1714546984={results.get('INJ_CAPACITANCE')}",
        "SLDO": f"https://docs.google.com/forms/d/e/1FAIpQLSf3NC84OaYYjJ-DgQ29RvMV2dDQnUI0nxBFdnCUVMby7RXOFQ/formResponse?usp=pp_url\
	&entry.910646842={outputDF.get('serialNumber')}\
	&entry.1225658339={outputDF.get('passed')}\
	&entry.2052956027={analysis_version}\
	&entry.314862968={meas_version}\
	&entry.137143573={layer}\
	&entry.507508481={site}\
	&entry.1425106615={timestamp}\
	&entry.613380586={results.get('SLDO_VI_SLOPE')}\
	&entry.2009791679={results.get('SLDO_VI_OFFSET')}\
	&entry.1877869140={results.get('SLDO_NOM_INPUT_CURRENT')}\
	&entry.1380637801={results.get('SLDO_VDDA')}\
	&entry.959013471={results.get('SLDO_VDDD')}\
	&entry.427742248={results.get('SLDO_VINA')}\
	&entry.1100117192={results.get('SLDO_VIND')}\
	&entry.411324334={results.get('SLDO_VOFFS')}\
	&entry.257023545={results.get('SLDO_IINA')}\
	&entry.172777573={results.get('SLDO_IIND')}\
	&entry.2138863081={results.get('SLDO_IREF')}\
	&entry.1216431295={results.get('SLDO_ISHUNTA')}\
	&entry.825886502={results.get('SLDO_ISHUNTD')}\
	&entry.298426805={results.get('SLDO_ANALOG_OVERHEAD')}\
	&entry.187142037={results.get('SLDO_DIGITAL_OVERHEAD')}\
	&entry.844801892={results.get('SLDO_LINEARITY')}\
	&entry.812048396={results.get('SLDO_VINA_VIND')}",
        "ANALOG_READBACK": f"https://docs.google.com/forms/d/e/1FAIpQLScsfVAnZokYd-CDef1WZGgdNEY-AdqeS3erRF1mzy6Bl37eYg/formResponse?usp=pp_url\
	&entry.910646842={outputDF.get('serialNumber')}\
	&entry.351877676={outputDF.get('passed')}\
	&entry.2065736414={analysis_version}\
	&entry.1608510255={meas_version}\
	&entry.1353243899={layer}\
	&entry.507508481={site}\
	&entry.1425106615={timestamp}\
	&entry.613380586={results.get('AR_NOMINAL_SETTINGS')[0]}\
	&entry.2091108240={results.get('AR_NOMINAL_SETTINGS')[1]}\
	&entry.1308096676={results.get('AR_NOMINAL_SETTINGS')[2]}\
	&entry.1616657488={results.get('AR_NOMINAL_SETTINGS')[3]}\
	&entry.303689355={results.get('AR_NOMINAL_SETTINGS')[4]}\
	&entry.1299197252={results.get('AR_NOMINAL_SETTINGS')[5]}\
	&entry.337124367={results.get('AR_NOMINAL_SETTINGS')[6]}\
	&entry.539725220={results.get('AR_NOMINAL_SETTINGS')[7]}\
	&entry.174520567={results.get('AR_NOMINAL_SETTINGS')[8]}\
	&entry.2077557631={results.get('AR_NOMINAL_SETTINGS')[9]}\
	&entry.1152177529={results.get('AR_NOMINAL_SETTINGS')[10]}\
	&entry.1170074988={results.get('AR_NOMINAL_SETTINGS')[11]}\
	&entry.1695410680={results.get('AR_NOMINAL_SETTINGS')[12]}\
	&entry.1683989630={results.get('AR_NOMINAL_SETTINGS')[13]}\
	&entry.637795568={results.get('AR_NOMINAL_SETTINGS')[14]}\
	&entry.1796334891={results.get('AR_NOMINAL_SETTINGS')[15]}\
	&entry.1192471500={results.get('AR_NOMINAL_SETTINGS')[16]}\
	&entry.1037413000={results.get('AR_NOMINAL_SETTINGS')[17]}\
	&entry.1731827348={results.get('AR_NOMINAL_SETTINGS')[18]}\
	&entry.1788264831={results.get('AR_NOMINAL_SETTINGS')[19]}\
	&entry.1271298835={results.get('AR_NOMINAL_SETTINGS')[20]}\
	&entry.294928269={results.get('AR_NOMINAL_SETTINGS')[21]}\
	&entry.1752002697={results.get('AR_NOMINAL_SETTINGS')[22]}\
	&entry.1789768564={results.get('AR_NOMINAL_SETTINGS')[23]}\
	&entry.19338211={results.get('AR_NOMINAL_SETTINGS')[24]}\
	&entry.1373225730={results.get('AR_NOMINAL_SETTINGS')[25]}\
	&entry.1288561285={results.get('AR_NOMINAL_SETTINGS')[26]}\
	&entry.993587744={results.get('AR_NOMINAL_SETTINGS')[27]}\
	&entry.1225105463={results.get('AR_NOMINAL_SETTINGS')[28]}\
	&entry.2014795413={results.get('AR_NOMINAL_SETTINGS')[29]}\
	&entry.814046228={results.get('AR_NOMINAL_SETTINGS')[30]}\
	&entry.1206599091={results.get('AR_NOMINAL_SETTINGS')[31]}\
	&entry.1046023025={results.get('AR_NOMINAL_SETTINGS')[32]}\
	&entry.125849508={results.get('AR_NOMINAL_SETTINGS')[33]}\
	&entry.278665318={results.get('AR_NOMINAL_SETTINGS')[34]}\
	&entry.1317511634={results.get('AR_NOMINAL_SETTINGS')[35]}\
	&entry.799431715={results.get('AR_NOMINAL_SETTINGS')[36]}\
	&entry.1032356051={results.get('AR_NOMINAL_SETTINGS')[37]}\
	&entry.206739602={results.get('AR_NOMINAL_SETTINGS')[38]}\
	&entry.47441728={results.get('AR_NOMINAL_SETTINGS')[39]}\
	&entry.887166253={results.get('AR_NOMINAL_SETTINGS')[40]}\
	&entry.290527652={results.get('AR_NOMINAL_SETTINGS')[41]}\
	&entry.1481344879={results.get('AR_NOMINAL_SETTINGS')[42]}\
	&entry.155322339={results.get('AR_NOMINAL_SETTINGS')[43]}\
	&entry.556597681={results.get('AR_NOMINAL_SETTINGS')[44]}\
	&entry.1293797041={results.get('AR_NOMINAL_SETTINGS')[45]}\
	&entry.1984481605={results.get('AR_NOMINAL_SETTINGS')[46]}\
	&entry.1633430606={results.get('AR_NOMINAL_SETTINGS')[47]}\
	&entry.1430993123={results.get('AR_NOMINAL_SETTINGS')[48]}\
	&entry.526213623={results.get('AR_NOMINAL_SETTINGS')[49]}\
	&entry.1631275305={results.get('AR_NOMINAL_SETTINGS')[50]}\
	&entry.975590254={results.get('AR_NOMINAL_SETTINGS')[51]}\
	&entry.1474828103={results.get('AR_NOMINAL_SETTINGS')[52]}\
	&entry.1495459865={results.get('AR_NOMINAL_SETTINGS')[53]}\
	&entry.1128496051={results.get('AR_NOMINAL_SETTINGS')[54]}\
	&entry.367477458={results.get('AR_NOMINAL_SETTINGS')[55]}\
	&entry.1466626922={results.get('AR_NOMINAL_SETTINGS')[56]}\
	&entry.631124052={results.get('AR_NOMINAL_SETTINGS')[57]}\
	&entry.946981503={results.get('AR_NOMINAL_SETTINGS')[58]}\
	&entry.571213202={results.get('AR_NOMINAL_SETTINGS')[59]}\
	&entry.688702844={results.get('AR_NOMINAL_SETTINGS')[60]}\
	&entry.431853336={results.get('AR_NOMINAL_SETTINGS')[61]}\
	&entry.1724286670={results.get('AR_NOMINAL_SETTINGS')[62]}\
	&entry.2112361286={results.get('AR_NOMINAL_SETTINGS')[63]}\
	&entry.1689766951={results.get('AR_NOMINAL_SETTINGS')[64]}\
	&entry.2142543004={results.get('AR_NOMINAL_SETTINGS')[65]}\
	&entry.1946421005={results.get('AR_NOMINAL_SETTINGS')[66]}\
	&entry.707341702={results.get('AR_NOMINAL_SETTINGS')[67]}\
	&entry.1328302698={results.get('AR_NOMINAL_SETTINGS')[68]}\
	&entry.1022788500={results.get('AR_NOMINAL_SETTINGS')[69]}\
	&entry.973739200={results.get('AR_NOMINAL_SETTINGS')[70]}\
	&entry.1279705270={results.get('AR_NOMINAL_SETTINGS')[71]}\
	&entry.1637225517={results.get('AR_TEMP_NTC')}\
	&entry.1793217377={results.get('AR_TEMP_EXT')}\
	&entry.2135558015={results.get('AR_TEMP_ASLDO')}\
	&entry.1505388309={results.get('AR_TEMP_DSLDO')}\
	&entry.363112736={results.get('AR_TEMP_ACB')}\
	&entry.1942035528={results.get('AR_TEMP_ACB')}\
	&entry.1251896209={results.get('AR_VDDA_VS_TRIM')[0]}\
	&entry.896618670={results.get('AR_VDDA_VS_TRIM')[1]}\
	&entry.60914654={results.get('AR_VDDA_VS_TRIM')[2]}\
	&entry.961303064={results.get('AR_VDDA_VS_TRIM')[3]}\
	&entry.448329889={results.get('AR_VDDA_VS_TRIM')[4]}\
	&entry.1155979196={results.get('AR_VDDA_VS_TRIM')[5]}\
	&entry.412804010={results.get('AR_VDDA_VS_TRIM')[6]}\
	&entry.949350985={results.get('AR_VDDA_VS_TRIM')[7]}\
	&entry.307370261={results.get('AR_VDDA_VS_TRIM')[8]}\
	&entry.409514081={results.get('AR_VDDA_VS_TRIM')[9]}\
	&entry.2001782359={results.get('AR_VDDA_VS_TRIM')[10]}\
	&entry.10329903={results.get('AR_VDDA_VS_TRIM')[11]}\
	&entry.1636667111={results.get('AR_VDDA_VS_TRIM')[12]}\
	&entry.685698936={results.get('AR_VDDA_VS_TRIM')[13]}\
	&entry.537201174={results.get('AR_VDDA_VS_TRIM')[14]}\
	&entry.1053736177={results.get('AR_VDDA_VS_TRIM')[15]}\
	&entry.1435921809={results.get('AR_VDDD_VS_TRIM')[0]}\
	&entry.1499425666={results.get('AR_VDDD_VS_TRIM')[1]}\
	&entry.1890145904={results.get('AR_VDDD_VS_TRIM')[2]}\
	&entry.383115039={results.get('AR_VDDD_VS_TRIM')[3]}\
	&entry.398663489={results.get('AR_VDDD_VS_TRIM')[4]}\
	&entry.1566918433={results.get('AR_VDDD_VS_TRIM')[5]}\
	&entry.1555345873={results.get('AR_VDDD_VS_TRIM')[6]}\
	&entry.1092876262={results.get('AR_VDDD_VS_TRIM')[7]}\
	&entry.1293594936={results.get('AR_VDDD_VS_TRIM')[8]}\
	&entry.2099215210={results.get('AR_VDDD_VS_TRIM')[9]}\
	&entry.413539179={results.get('AR_VDDD_VS_TRIM')[10]}\
	&entry.1080321692={results.get('AR_VDDD_VS_TRIM')[11]}\
	&entry.259801418={results.get('AR_VDDD_VS_TRIM')[12]}\
	&entry.2100743637={results.get('AR_VDDD_VS_TRIM')[13]}\
	&entry.1600042255={results.get('AR_VDDD_VS_TRIM')[14]}\
	&entry.50695564={results.get('AR_VDDD_VS_TRIM')[15]}",
    }
    log.info(
        bcolors.WARNING
        + "Copy the following URL into a browser to submit these results: \n"
        + url.get(outputDF.get("testType")).replace("\t", "")
        + "\n"
        + "View submitted results at: https://docs.google.com/spreadsheets/d/1pw_07F94fg2GJQr8wlvhaRUV63uhsAuBt_S1FEFBzBU/view"
        + bcolors.ENDC
    )
    with Path(outputfile).open("a") as fpointer:
        fpointer.writelines(url.get(outputDF.get("testType")).replace("\t", "") + "\n")
