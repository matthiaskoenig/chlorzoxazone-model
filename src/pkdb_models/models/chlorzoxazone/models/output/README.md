[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7760665.svg)](https://doi.org/10.5281/zenodo.7760665)
[![GitHub Action](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/python.yml/badge.svg)](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/python.yml)
[![GitHub Action](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/docker.yml/badge.svg)](https://github.com/matthiaskoenig/chlorzoxazone-model/actions/workflows/docker.yml)

# chlorzoxazone model
This repository provides the chlorzoxazone physiologically based pharmacokinetic (PBPK) model: the oral absorption of chlorzoxazone, the probe drug of CYP2E1, its distribution into the tissues, its 6-hydroxylation by CYP2E1 and a CYP2E1 independent elimination in the liver, the glucuronidation of 6-hydroxychlorzoxazone and the renal excretion of the glucuronide relative to the GFR. The model describes the effects of the dose (the saturation of CYP2E1), of the CYP2E1 activity, of inhibitors of CYP2E1 (disulfiram, isoniazid), of hepatic and renal impairment, and the absorption and elimination of ethanol with the induction of CYP2E1 by ethanol.

The model is distributed in [SBML](http://sbml.org) format available from [`chlorzoxazone_body_flat.xml`](./models/chlorzoxazone_body_flat.xml) with 
corresponding [SBML4humans model report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fchlorzoxazone-model%2Fmain%2Fmodels%2Fchlorzoxazone_body_flat.xml) and [model equations](./models/chlorzoxazone_body_flat.md).

The COMBINE archive is available from [`chlorzoxazone_model.omex`](./chlorzoxazone_model.omex).

![model overview](./figures/chlorzoxazone_model.png)

### Comp submodels
* **liver** submodel [`chlorzoxazone_liver.xml`](./models/chlorzoxazone_liver.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fchlorzoxazone-model%2Fmain%2Fmodels%2Fchlorzoxazone_liver.xml) and [equations](./models/chlorzoxazone_liver.md).
* **kidney** submodel [`chlorzoxazone_kidney.xml`](./models/chlorzoxazone_kidney.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fchlorzoxazone-model%2Fmain%2Fmodels%2Fchlorzoxazone_kidney.xml) and [equations](./models/chlorzoxazone_kidney.md).
* **intestine** submodel [`chlorzoxazone_intestine.xml`](./models/chlorzoxazone_intestine.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fchlorzoxazone-model%2Fmain%2Fmodels%2Fchlorzoxazone_intestine.xml) and [equations](./models/chlorzoxazone_intestine.md).
* **whole-body** submodel [`chlorzoxazone_body.xml`](./models/chlorzoxazone_body.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fchlorzoxazone-model%2Fmain%2Fmodels%2Fchlorzoxazone_body.xml) and [equations](./models/chlorzoxazone_body.md).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7760665.svg)](https://doi.org/10.5281/zenodo.7760665)

> Küttner, J. & König, M. (2026).
> *Physiologically based pharmacokinetic (PBPK) model of chlorzoxazone.*   
> Zenodo. [https://doi.org/10.5281/zenodo.7760665](https://doi.org/10.5281/zenodo.7760665)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

## Run simulations
### python
Clone the repository 
```bash
git clone https://github.com/matthiaskoenig/chlorzoxazone-model.git
cd chlorzoxazone-model
```

#### uv
Setup environment with uv (https://docs.astral.sh/uv/getting-started/installation/)
```bash
uv sync
```
Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.chlorzoxazone -a all -r results
```

#### pip
If you use pip install the package via
```bash
pip install -e .
```
Run the complete analysis in the environment via:
```bash
run_simulation pkdb_models.models.chlorzoxazone -a all -r results
```

### docker
Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/chlorzoxazone:latest /bin/bash
```

Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.chlorzoxazone -a all -r /results
```
The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:
```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```

## Funding
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2022-2026 Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)

