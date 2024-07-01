# Plastics Supplemental Scripts
Supporting scripts and graphics for documentation of the [Global Plastics AI Policy Tool](https://global-plastics-tool.org/).

## Purpose
A collection of small scripts used to support the preparation of derivative datasets and secondary graphs which complement the [Global Plastics AI Policy Tool](https://global-plastics-tool.org/). See also the [main tool repository](https://github.com/SchmidtDSE/plastics-prototype) that these scripts support.

## Usage
Simply install python dependencies (`pip install -r requirements.txt`) and execute the small pipeline (`bash run_pipeline.sh`). Note that this does not run the optional OpenRefine script to generate supplemental dataset 1 under the `refine` subdirectory.

## Local development environment
No additional steps beyond install of python dependencies (`pip install -r requirements.txt`) are required though users may consider building a [virtual environment](https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/virtualenv.html).

## Testing
As these are just small supporting scripts, there are not explicit style guidelines or separate automated tests which are enforced in the [upstream repository](https://github.com/SchmidtDSE/plastics-prototype).

## Deployment
Simply merging to `main` will cause the scripts to execute and their results packaged. Note that these are not permanent resources so there is no "deployment" location and, instead, are simply made available for the convienence of users as further supplementary material.

## License
This repository is made available under the [BSD 3-Clause License](https://opensource.org/license/bsd-3-clause) as further described in `LICENSE.md`.

## Open source
This repository uses the following open source resources:

 - [Matplotlib](https://matplotlib.org/) under the [PSF License](https://matplotlib.org/stable/project/license.html).
 - [NumPy](https://numpy.org/) under the [BSD License](https://github.com/numpy/numpy/blob/main/LICENSE.txt).
 - [OpenRefine](https://openrefine.org/) under the [BSD License](https://github.com/OpenRefine/OpenRefine/blob/master/LICENSE.txt).
 - [pandas](https://pandas.pydata.org/) under the [BSD License](https://github.com/pandas-dev/pandas/blob/main/LICENSE).
 - [Sketchingpy](https://sketchingpy.org/) under the [BSD License](https://codeberg.org/sketchingpy/Sketchingpy/src/branch/main/LICENSE.md).
 - [scikit-learn](https://scikit-learn.org/stable/) under the [BSD License](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING).
 - [PyToolz](https://toolz.readthedocs.io/en/latest/) under the [BSD License](https://github.com/pytoolz/toolz/blob/master/LICENSE.txt)

Some scripts also use:

 - [Color Brewer v2](https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3) under the [Apache v2 License](https://github.com/axismaps/colorbrewer/blob/master/LICENCE.txt).
 - [Public Sans](https://public-sans.digital.gov/) under the [CC0 License](https://github.com/uswds/public-sans/blob/develop/LICENSE.md).

We thank these projects for their contribution.
