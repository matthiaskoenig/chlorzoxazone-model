# Chlorzoxazone

Physiologically based pharmacokinetic (PBPK) model of the muscle relaxant chlorzoxazone, the probe drug of CYP2E1: its oral absorption (the dissolution of tablets, a solution is absorbed directly), its distribution into the tissues (a fixed tissue partition, a volume of distribution of about 0.13 l/kg) and in the blood (blood to plasma ratio 0.51), its 6-hydroxylation by CYP2E1 and a CYP2E1 independent elimination in the liver, the glucuronidation of 6-hydroxychlorzoxazone and the renal excretion of the glucuronide relative to the GFR. The model describes the dose dependency (the saturation of CYP2E1), the effects of the CYP2E1 activity, of inhibitors of CYP2E1 (disulfiram, isoniazid, watercress, diosmin), of hepatic and renal impairment, and the absorption and elimination of ethanol with the induction of CYP2E1 by ethanol.

The model repository is [chlorzoxazone-model](https://github.com/matthiaskoenig/chlorzoxazone-model), its DOI [10.5281/zenodo.7760665](https://doi.org/10.5281/zenodo.7760665).

## Structure

- `__init__.py`: the paths of the model and its model object `MODEL` with its release metadata and its adopted fits, which the commands below run (pkpdsim).
- `models/`: the tissue models (`model_intestine.py`, `model_liver.py`, `model_kidney.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated and the ODEs in `models/output/models/` and the COMBINE archive in `models/output/`; the fitted values come from the adopted fits (`models/fits.py`, `models/output/fits/`).
- `experiments/`: the simulation experiments of the clinical studies (`studies/`), the dose dependency and the studies of Bedada in one figure (`misc/`), the scans of the CYP2E1 activity, of cirrhosis, of the body weight and of sampled populations (`scans/`) and the experiments of ethanol and of the induction of CYP2E1 by ethanol (`alcohol_model/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`.
- `fitting/`: the fit problems of the pharmacokinetics of chlorzoxazone (`PK`) and of ethanol (`ALCOHOL`), their parameters and the selection of the training, validation and outlier data.
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics.
- `chlorzoxazone_pk.py`: the pharmacokinetic parameters of chlorzoxazone and 6-hydroxychlorzoxazone in the scans, the non-compartmental analysis of `pkpdutils`.
- `cyp2e1_amounts/`: the CYP2E1 amounts of human liver microsomes and their distributions, which the sampling scans use; `pk_params/`: the pharmacokinetic parameters of the curated studies.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`).
- `publication.md`: the experiments of the figures of the publication.
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.chlorzoxazone --action factory
run_simulation pkdb_models.models.chlorzoxazone --action list_experiments
run_simulation pkdb_models.models.chlorzoxazone --action simulate --experiments all
run_simulation pkdb_models.models.chlorzoxazone --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.chlorzoxazone --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.chlorzoxazone --subset=ALCOHOL --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.chlorzoxazone --adopt PK_<fit id>
run_report pkdb_models.models.chlorzoxazone --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.chlorzoxazone --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.chlorzoxazone.sensitivity.sensitivity_analysis
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fits of the model,
not from numbers in the code. `run_fit pkdb_models.models.chlorzoxazone --adopt <fit id>`
copies the record of a finished fit (its parameters, problem, profile
likelihood and Fisher information) into `models/output/fits/<fit id>/`, which is
tracked; the ids of the adopted fits are listed in `fits` of the model object
(`__init__.py`). The factory takes the fitted values and their uncertainty from
the records (`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`; the
scans of sampled populations simulate fewer individuals, each with every draw,
and the large scans a coarser grid. A refit is: fit, adopt, replace the id in
`fits`, rebuild the model. See the documentation of the repository on fitting
(`docs/fitting.md`).
