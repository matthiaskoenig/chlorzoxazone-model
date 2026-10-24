[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7760665.svg)](https://doi.org/10.5281/zenodo.7760665)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/chlorzoxazone-model)](https://github.com/matthiaskoenig/chlorzoxazone-model/releases)
[![Documentation](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/chlorzoxazone-model/)
[![CI](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/chlorzoxazone?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/chlorzoxazone)
[![Python](https://img.shields.io/badge/python-3.14%20%7C%203.15-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic (PBPK) model of chlorzoxazone

This repository provides the chlorzoxazone physiologically based pharmacokinetic (PBPK) model: the probe of CYP2E1, its oral absorption, its distribution in the tissues, its 6-hydroxylation by CYP2E1 and a second elimination in the liver, the glucuronidation of 6-hydroxychlorzoxazone and the renal excretion of the glucuronide, and the induction of CYP2E1 by ethanol.

Documentation: <https://matthiaskoenig.github.io/chlorzoxazone-model/>

## Quick start

```bash
git clone https://github.com/matthiaskoenig/chlorzoxazone-model.git && cd chlorzoxazone-model
uv sync
uv run run_simulation pkdb_models.models.chlorzoxazone --action all -r results
```

## How to cite

> Küttner, J. & König, M. (2026). *Physiologically based pharmacokinetic (PBPK) model of chlorzoxazone*. Zenodo. https://doi.org/10.5281/zenodo.7760665

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2022-2026 Jonas Küttner and Matthias König
