from __future__ import annotations

import json
import logging
from glob import glob
from pathlib import Path

import typer
from module_qc_data_tools import (
    convert_name_to_serial,
)

from module_qc_analysis_tools.cli.globals import (
    CONTEXT_SETTINGS,
    OPTIONS,
    LogLevel,
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

scans = {
    "digitalscan": ["OccupancyMap"],
    "analogscan": ["OccupancyMap"],
    "thresholdscan_hr": ["Chi2Map", "ThresholdMap", "NoiseMap", "Config"],
    "thresholdscan_hd": ["Chi2Map", "ThresholdMap", "NoiseMap", "Config"],
}


def findLatestResults(path):
    path = str(path.resolve())

    log.info(f"Searching for latest YARR scan results in {path}")
    alldirs = glob(path + "/*")
    alldirs.sort()

    # Make structure to hold location of results
    latest_results = {}
    for s in scans:
        latest_results.update({s: "null"})

    # Find latest YARR scans, assumes directories named with run numbers
    for d in alldirs:
        if "last_scan" in d:
            alldirs.remove(d)
        for s in latest_results:
            if s in d:
                latest_results.update({s: d})
                break
    return latest_results


def getDataFile(mname, latest_results, output):
    log.debug(f"Setting module SN to {mname}")
    # Setup structure of output
    config_file = {
        "datadir": output,  # Could be ""
        "module": {"serialNumber": mname, "chipType": "RD53B"},
        "chip": [],
    }

    # Collect necessary data from each scan
    chip_data = {}
    for key, value in scans.items():
        for v in value:
            if v == "Config":
                data = glob(latest_results.get(key) + "/0x*.json.before")
            else:
                data = glob(latest_results.get(key) + "/*" + v + "*.json")
            for d in data:
                log.debug(f"Found {d}")
                chipname = d.split("/")[-1].split("_")[0]
                if chip_data.get(chipname):
                    chip_data[chipname]["filepaths"].update(
                        {key + "_" + v: d.split(output + "/")[-1]}
                    )
                else:
                    chip_data[chipname] = {
                        "serialNumber": convert_name_to_serial(chipname),
                        "filepaths": {key + "_" + v: d.split(output + "/")[-1]},
                    }
    for r in chip_data:
        config_file["chip"].append(chip_data[r])
        log.info(
            f"Found {len(chip_data[r]['filepaths'])} YARR scans for chip {chip_data[r].get('serialNumber')}"
        )

    # Write to output
    with Path(output + "/info.json").open("w") as f:
        log.info("Writing " + output + "/info.json")
        json.dump(
            config_file,
            f,
            ensure_ascii=False,
            indent=4,
            sort_keys=False,
            separators=(",", ": "),
        )


app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def main(
    input_yarr: Path = OPTIONS["input_yarr_scans"],
    output_yarr: Path = OPTIONS["output_yarr"],
    module_sn: str = OPTIONS["moduleSN"],
    verbosity: LogLevel = OPTIONS["verbosity"],
    digitalscan: Path = OPTIONS["digitalscan"],
    analogscan: Path = OPTIONS["analogscan"],
    thresholdscan_hr: Path = OPTIONS["thresholdscan_hr"],
    thresholdscan_hd: Path = OPTIONS["thresholdscan_hd"],
):
    log.setLevel(verbosity.value)

    log.info("")
    log.info(" ==============================================================")
    log.info(f" \tCollecting YARR scan output for module {module_sn}")
    log.info(" ==============================================================")
    log.info("")

    # Find latest results if path to all YARR output is supplied
    latest_results = {}
    if input_yarr is not None:
        latest_results = findLatestResults(input_yarr)

    # Fill in user-supplied YARR output directories
    if digitalscan is not None:
        if input_yarr is not None:
            log.info("Overriding latest digitalscan results with user-supplied scan")
        latest_results.update({"digitalscan": str(digitalscan)})
    if analogscan is not None:
        if input_yarr is not None:
            log.info("Overriding latest analogscan results with user-supplied scan")
        latest_results.update({"analogscan": str(analogscan)})
    if thresholdscan_hr is not None:
        if input_yarr is not None:
            log.info(
                "Overriding latest thresholdscan_hr results with user-supplied scan"
            )
        latest_results.update({"thresholdscan_hr": str(thresholdscan_hr)})
    if thresholdscan_hd is not None:
        if input_yarr is not None:
            log.info(
                "Overriding latest thresholdscan_hd results with user-supplied scan"
            )
        latest_results.update({"thresholdscan_hd": str(thresholdscan_hd)})

    if len(latest_results.keys()) == 0:
        log.error(
            "No YARR results found. Please specify directory to latest YARR scan results, or supply each YARR scan output with appropriate flags. Type `analysis-load-yarr-scans -h` for help"
        )
        raise RuntimeError()

    if output_yarr is None:
        output_yarr = input_yarr if input_yarr is not None else "./"

    getDataFile(module_sn, latest_results, str(output_yarr))


if __name__ == "__main__":
    main()
