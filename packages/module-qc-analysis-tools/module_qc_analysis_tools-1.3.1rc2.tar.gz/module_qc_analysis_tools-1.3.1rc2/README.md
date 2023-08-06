# module-qc-analysis-tools v1.3.1rc2

A general python tool for running ITkPixV1.1 module QC test analysis. An
overview of the steps in the module QC procedure is documented in the
[Electrical specification and QC procedures for ITkPixV1.1 modules](https://gitlab.cern.ch/atlas-itk/pixel/module/itkpix-electrical-qc/)
document and in
[this spreadsheet](https://docs.google.com/spreadsheets/d/1qGzrCl4iD9362RwKlstZASbhphV_qTXPeBC-VSttfgE/edit#gid=989740987).
The analysis scripts in this repository require input files with measurement
data. The measurement data should be collected using the
[module-qc-measurement-tools](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-tools)
package.

## Requirements

This tool requires users to have >python3.6 with the following packages
installed:

- `numpy`
- `scipy`
- `tabulate`
- `matplotlib`
- `jsonschema`

## Installation

This package may be accessed by cloning from gitlab or by installing it via pip.

### via clone

Use this method if you want to use the latest version of the package from
gitlab. First clone the project:

```
git clone https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-analysis-tools.git
```

Upon a successful checkout, `cd` to the new `module-qc-analysis-tools` directory
and run the following to install the necessary software:

```verbatim
$ python3 -m venv env
$ source env/bin/activate
$ python -m pip install --upgrade pip
$ python -m pip install -e .
```

### via pip

Use this method if you want to use the latest stable (versioned) release of the
package.

```
python -m venv venv
source venv/bin/activate
python -m pip install -U pip
python -m pip install -U pip module-qc-analysis-tools==1.3.1rc2
```

Note that users should use the latest python version (check python version via
`python3 -V`). Python3.7 is the minimum requirement for developers. See
[For Developer](#for-developer) section.

## Scripts

### `Analyze ADC Calibration`

This analysis script performs the ADC calibration. It produces several
diagnostic plots and an output file with the ADC calibration slope and offset.

<details> <summary> analysis-ADC-CALIBRATION --help </summary>

```
analysis-ADC-CALIBRATION --help
usage: analysis-ADC-CALIBRATION [-h] -i INPUT_MEAS [-o OUTPUT_DIR] [-q QC_CRITERIA] [-l LAYER] [--permodule]
                                [-f {root,numpy}] [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_MEAS, --input-meas INPUT_MEAS
                        path to the input measurement file or directory containing input measurement files.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory
  -q QC_CRITERIA, --qc-criteria QC_CRITERIA
                        path to json file with QC selection criteria (default: $(module-qc-analysis-tools --prefix)/analysis_cuts.json)
  -l LAYER, --layer LAYER
                        Layer of module, used for applying correct QC criteria settings. Options: L0, L1, L2
                        (default)
  --permodule           Store results in one file per module (default: one file per chip)
  -f {root,numpy}, --fit-method {root,numpy}
                        fitting method
  -v VERBOSITY, --verbosity VERBOSITY
                        Log level [options: DEBUG, INFO (default), WARNING, ERROR]
```

</details>

### `Analyze Analog Readback`

This analysis script performs the Analog Readback. It produces an output file
with the calculated internal biases, temperature from the internal and external
temperature sensor, and VDDA/VDDD vs Trim, including diagnostic plots with slope
and offset.

<details> <summary> analysis-ANALOG-READBACK --help </summary>

```
$ analysis-ANALOG-READBACK --help
usage: analysis-ANALOG-READBACK [-h] -i INPUT_MEAS [-o OUTPUT_DIR] [-q QC_CRITERIA] [-l LAYER] [--permodule]
                                [-f {root,numpy}] [-v VERBOSITY] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_MEAS, --input-meas INPUT_MEAS
                        path to the input measurement file or directory containing input measurement files.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory
  -q QC_CRITERIA, --qc-criteria QC_CRITERIA
                        path to json file with QC selection criteria (default: $(module-qc-analysis-tools --prefix)/analysis_cuts.json)
  -l LAYER, --layer LAYER
                        Layer of module, used for applying correct QC criteria settings. Options: L0, L1, L2
                        (default)
  --permodule           Store results in one file per module (default: one file per chip)
  -f {root,numpy}, --fit-method {root,numpy}
                        fitting method
  -v VERBOSITY, --verbosity VERBOSITY
                        Log level [options: DEBUG, INFO (default), WARNING, ERROR]
  --verbose             verbose mode

```

</details>

### `Analyze SLDO`

This script analyses the SLDO curve. It produces several diagnostic plots and an
output file with several parameters extracted from the SLDO curves.

<details> <summary> analysis-SLDO --help </summary>

```
$ analysis-SLDO --help
usage: analysis-SLDO [-h] -i INPUT_MEAS [-o OUTPUT_DIR] [-q QC_CRITERIA] [-l LAYER] [--permodule] [-n NCHIPS]
                     [-f {root,numpy}] [-v VERBOSITY] [--lp-enable]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_MEAS, --input-meas INPUT_MEAS
                        path to the input measurement file or directory containing input measurement files.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory
  -q QC_CRITERIA, --qc-criteria QC_CRITERIA
                        path to json file with QC selection criteria (default: $(module-qc-analysis-tools --prefix)/analysis_cuts.json)
  -l LAYER, --layer LAYER
                        Layer of module, used for applying correct QC criteria settings. Options: L0, L1, L2
                        (default)
  --permodule           Store results in one file per module (default: one file per chip)
  -n NCHIPS, --nChips NCHIPS
                        Number of chips powered in parallel (e.g. 4 for a quad module, 3 for a triplet, 1 for an
                        SCC.)
  -f {root,numpy}, --fit-method {root,numpy}
                        fitting method
  -v VERBOSITY, --verbosity VERBOSITY
                        Log level [options: DEBUG, INFO (default), WARNING, ERROR]
  --lp-enable           low power mode

```

</details>

### `Analyze VCal Calibration`

This analysis script performs the VCal calibration. It produces several
diagnostic plots and an output file with the VCal calibration slope and offset.

<details> <summary> analysis-VCAL-CALIBRATION --help </summary>

```
$ analysis-VCAL-CALIBRATION --help
usage: analysis-VCAL-CALIBRATION [-h] -i INPUT_MEAS [-o OUTPUT_DIR] [-q QC_CRITERIA] [-l LAYER] [--permodule]
                                 [-f {root,numpy}] [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_MEAS, --input-meas INPUT_MEAS
                        path to the input measurement file or directory containing input measurement files.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory
  -q QC_CRITERIA, --qc-criteria QC_CRITERIA
                        path to json file with QC selection criteria (default: $(module-qc-analysis-tools --prefix)/analysis_cuts.json)
  -l LAYER, --layer LAYER
                        Layer of module, used for applying correct QC criteria settings. Options: L0, L1, L2
                        (default)
  --permodule           Store results in one file per module (default: one file per chip)
  -f {root,numpy}, --fit-method {root,numpy}
                        fitting method
  -v VERBOSITY, --verbosity VERBOSITY
                        Log level [options: DEBUG, INFO (default), WARNING, ERROR]
```

</details>

### `Analyze Injection capacitance`

This analysis script performs the injection capacitance. It produces several
diagnostic plots and an output file with the measured pixel injection
capacitance.

<details> <summary> analysis-INJECTION-CAPACITANCE --help </summary>

```
$ analysis-INJECTION-CAPACITANCE
usage: analysis-INJECTION-CAPACITANCE [-h] -i INPUT_MEAS [-o OUTPUT_DIR] [-q QC_CRITERIA] [-l LAYER] [--permodule]
                                      [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_MEAS, --input-meas INPUT_MEAS
                        path to the input measurement file or directory containing input measurement files.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory
  -q QC_CRITERIA, --qc-criteria QC_CRITERIA
                        path to json file with QC selection criteria (default: $(module-qc-analysis-tools --prefix)/analysis_cuts.json)
  -l LAYER, --layer LAYER
                        Layer of module, used for applying correct QC criteria settings. Options: L0, L1, L2
                        (default)
  --permodule           Store results in one file per module (default: one file per chip)
  -v VERBOSITY, --verbosity VERBOSITY
                        Log level [options: DEBUG, INFO (default), WARNING, ERROR]
```

</details>

## Notes

### `Submit QC results`

To submit the QC results, supply the --submit option to the analysis. You also
need to supply the site where the testing took place, as written in production
DB (i.e. LBNL_PIXEL_MODULES for LBNL, IRFU for Paris-Saclay, ...). This will
generate a URL that is printed to the terminal and saved in "submit.txt" in the
same folder as the analysis output. To submit the results, you need to copy and
paste one URL for each chip / test into a browser. Once submitted, the results
can be viewed here:
https://docs.google.com/spreadsheets/d/1pw_07F94fg2GJQr8wlvhaRUV63uhsAuBt_S1FEFBzBU/view
. While all submitted results will be recorded, only the latest results for each
chip / test will be analyzed. If a mistake was realized in the submitted
results, one can re-run the analysis and re-submit the results to overwrite the
original results.

### `Example commands for a chip in a quad module (L2):`

```
analysis-ADC-CALIBRATION -i ../module-qc-tools/emulator/outputs/Measurements/ADC_CALIBRATION/1000000001/ --layer L2
analysis-SLDO -i ../module-qc-tools/emulator/outputs/Measurements/SLDO/1000000001/ --layer L2
analysis-ANALOG-READBACK -i ../module-qc-tools/emulator/outputs/Measurements/ANALOG_READBACK/1000000001/ --layer L2
analysis-VCAL-CALIBRATION -i ../module-qc-tools/emulator/outputs/Measurements/VCAL_CALIBRATION/1000000001/ --layer L2
analysis-INJECTION-CAPACITANCE -i ../module-qc-tools/emulator/outputs/Measurements/INJECTION_CAPACITANCE/1000000001/ --layer L2
```

### `Update Chip Config`

After each analysis, update the settings in the chip config by running:

```
analysis-update-chip-config -i <path to analysis output directory> -c <path to YARR config directory> -t <config type>
```

This script reads the analysis test type and update the corresponding parameters
in the chip config.

### `JsonChecker and DataExtractor`

Two classes are designed for general purposes of the module qc analysis tool.

1. `JsonChecker` a. Check whether the test type is implemented b. For a specific
   task, check if required keywords exist c. Check if lengths of measurements
   are identical d. Check if there are negative numbers of measurements

2. `DataExtractor` This class finds measurements by Vmux value and convert them
   to quantites.

## For Developer

### python version

A python version higher than 3.7 is needed for this repository. Check the local
python version with `python -V`.

If the local python version is lower, set up a virtual python environment
following the instructions
[here](https://itk.docs.cern.ch/general/Virtual_Environments/).

### versioning

In case you need to tag the version of the code, you need to have either `hatch`
or `pipx` installed.

1. Activate python environment, e.g. `source venv/bin/activate`.
2. Run `python -m pip install hatch` or `python -m pip install pipx`.

You can bump the version via:

```
pipx run hatch run tag x.y.z

# or

hatch run tag x.y.z
```

where `x.y.z` is the new version to use. This should be run from the default
branch (`main` / `master`) as this will create a commit and tag, and push for
you. So make sure you have the ability to push directly to the default branch.

### pre-commit

Install pre-commit to avoid CI failure. Once pre-commit is installed, a git hook
script will be run to identify simple issues before submission to code review.

Instruction for installing pre-commit in a python environment:

1. Activate python environment, e.g. `source venv/bin/activate`.
2. Run `python3 -m pip install pre-commit`.
3. Run `pre-commit install` to install the hooks in `.pre-commit-config.yaml`.

After installing pre-commit, `.pre-commit-config.yaml` will be run every time
`git commit` is done. Redo `git add` and `git commit`, if the pre-commit script
changes any files.
