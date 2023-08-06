from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import typer
from module_qc_data_tools import (
    convert_serial_to_name,
    outputDataFrame,
    qcDataFrame,
    save_dict_list,
)

from module_qc_analysis_tools import __version__
from module_qc_analysis_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)
from module_qc_analysis_tools.utils.analysis import (
    get_layer,
    perform_qc_analysis,
)
from module_qc_analysis_tools.utils.classification import (
    classify_pixels,
    count_pixels,
    format_pixel_input,
    print_pixel_classification,
)
from module_qc_analysis_tools.utils.misc import (
    bcolors,
    get_qc_config,
)

app = typer.Typer(context_settings=CONTEXT_SETTINGS)

log = logging.getLogger()


@app.command()
def main(
    input_yarr: Path = OPTIONS["input_yarr_config"],
    qc_criteria_path: Path = OPTIONS["qc_criteria"],
    pixel_classification_path: Path = OPTIONS["pixel_classification"],
    layer: str = OPTIONS["layer"],
    base_output_dir: Path = OPTIONS["output_dir"],
    permodule: bool = OPTIONS["permodule"],
    verbosity: LogLevel = OPTIONS["verbosity"],
):
    log.setLevel(verbosity.value)

    test_type = Path(__file__).stem
    qc_config = get_qc_config(qc_criteria_path, test_type)

    log.info("")
    log.info(" ====================================================")
    log.info(" \tPerforming minimum health test analysis")
    log.info(" ====================================================")
    log.info("")

    time_start = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = base_output_dir.joinpath(test_type).joinpath(f"{time_start}")
    output_dir.mkdir(parents=True, exist_ok=False)

    # TODO check contents of json in JSONchecker-like object
    input_data = json.loads(input_yarr.read_text())
    datadir = input_data["datadir"]

    # TODO check contents of json in JSONchecker-like object
    pixel_classification = json.loads(pixel_classification_path.read_text())

    alloutput = []
    for c in input_data["chip"]:
        chipSN = c["serialNumber"]
        chipName = convert_serial_to_name(chipSN)
        filepaths = c["filepaths"]
        results = {}

        # Initialize array to track pixel failures
        pix_fail = np.zeros(153600, dtype=np.uint16)

        # Initialize int to track which classifications have been checked
        record_fail = 0

        log.debug(
            f"Performing minimum health test analysis on chip {c['serialNumber']}"
        )

        if not pixel_classification.get(test_type):
            log.error(
                bcolors.BADRED
                + f"Pixel failure selection for {test_type} not found in {pixel_classification_path}! Please check. "
                + bcolors.ENDC
            )
            raise RuntimeError()

        """ Prepare output json file """
        outputDF = outputDataFrame()
        outputDF.set_test_type(test_type)
        outputDF.set_serial_num(chipSN)
        data = qcDataFrame()
        data.add_property(
            "ANALYSIS_VERSION",
            __version__,
        )
        data.add_meta_data("QC_LAYER", layer)

        # Loop through pixel failure tests from config file
        for test_name, params in pixel_classification.get(test_type).items():
            log.debug(f"Performing {test_name}")

            test_input = params.get("input")
            test_method = params.get("method")
            test_params = params.get("params")

            # Get layer-specific params if necessary
            if type(test_params) is dict:
                layer_name = get_layer(layer)
                layer_bounds = test_params.get(layer_name)
                if not layer_bounds:
                    log.error(
                        bcolors.ERROR
                        + f" QC selections for {test_name} and {layer_name} do not exist - please check! Skipping."
                        + bcolors.ENDC
                    )
                    continue
                test_params = layer_bounds

            # Check if we have data for that test
            if test_input not in filepaths.keys():
                log.warning(
                    bcolors.WARNING
                    + f"YARR data for {test_name} not found in {input_yarr} ({test_input}), skipping test"
                    + bcolors.ENDC
                )
                continue

            # Read input YARR scan
            input_data_path = datadir + "/" + filepaths[test_input]
            with Path(input_data_path).open() as serialized:
                input_data = json.load(serialized)

            pix_data, pix_index = format_pixel_input(input_data.get("Data"))

            # Calculate relevant quantities
            if test_method == "mean":
                results.update({"PIXEL_FAILURE_" + test_name: np.mean(pix_data)})
            elif test_method == "rms":
                results.update({"PIXEL_FAILURE_" + test_name: np.std(pix_data)})
            else:
                log.debug(f"Classifying pixels failing {test_name}")
                pix_fail, record_fail = classify_pixels(
                    pix_data, pix_fail, record_fail, test_name, test_method, test_params
                )
                if np.isscalar(pix_fail):
                    continue

        test_names = pixel_classification.get(test_type).keys()
        failure_summary = count_pixels(pix_fail, record_fail, test_names)
        for fname, nfail in failure_summary.items():
            data.add_parameter(
                "PIXEL_FAILURE_" + fname, round(nfail.get("dependent"), 3)
            )

        print_pixel_classification(failure_summary)
        total_electrically_failing = list(failure_summary.values())[-1].get(
            "integrated"
        )
        results.update({"ELECTRICALLY_FAILED": total_electrically_failing})
        data.add_parameter(
            "PIXEL_FAILURE_ELECTRICALLY_FAILED", total_electrically_failing
        )

        passes_qc = perform_qc_analysis(
            test_type, qc_config, layer, results, verbosity.value
        )
        if passes_qc == -1:
            log.error(
                bcolors.ERROR
                + f" QC analysis for {chipName} was NOT successful. Please fix and re-run. Continuing to next chip.."
                + bcolors.ENDC
            )
            continue
        log.info("")
        if passes_qc:
            log.info(
                f" Chip {chipName} passes QC? "
                + bcolors.OKGREEN
                + f"{passes_qc}"
                + bcolors.ENDC
            )
        else:
            log.info(
                f" Chip {chipName} passes QC? "
                + bcolors.BADRED
                + f"{passes_qc}"
                + bcolors.ENDC
            )
        log.info("")

        outputDF.set_results(data)
        outputDF.set_pass_flag(passes_qc)

        if permodule:
            alloutput += [outputDF.to_dict(True)]
        else:
            outfile = output_dir.joinpath(f"{chipName}.json")
            log.info(f" Saving output of analysis to: {outfile}")
            save_dict_list(outfile, [outputDF.to_dict(True)])

    if permodule:
        outfile = output_dir.joinpath("module.json")
        log.info(f" Saving output of analysis to: {outfile}")
        save_dict_list(
            outfile,
            alloutput,
        )


if __name__ == "__main__":
    typer.run(main)
