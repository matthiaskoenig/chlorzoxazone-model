"""Parameter fit problems for chlorzoxazone.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the training data a fit is evaluated on but
not fitted to. The metadata of a mapping describes its curve, what a fit does
with the curve is decided here.

The training data are the mean data of healthy subjects after a single oral
dose without an interacting drug, solutions and solid formulations together
(the dissolution of tablets separates them). The validation data has four
parts, each a different question: the interactions (`INTERACTION_VALIDATION`,
the arms with a coadministered drug whose interaction the model describes with
factors of CYP2E1 and of the CYP2E1 independent elimination which are not
fitted), the doses (`DOSE_VALIDATION`, single subjects over the dose range,
which the mean data of the training predict), the populations
(`POPULATION_VALIDATION`, obesity and diabetes, which the model describes by
the body weight alone, and the variability of single subjects) and the
limitations (`LIMITATION_VALIDATION`, the induction of CYP2E1 by alcohol and
by fasting, which the model does not describe). The summaries of data which is
fitted one by one and the same subjects counted twice are excluded
(`AGGREGATE_MAPPINGS`).

The subsets: the pharmacokinetics of chlorzoxazone (`PK`) and the ethanol data
of the alcohol model (`ALCOHOL`).
"""

from collections.abc import Callable, Sequence

from pkpdsim.fit import mapping_metadata
from pkpdsim.metadata import Coadministration, DataType, Health
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.chlorzoxazone import CHLORZOXAZONE_PATH, DATA_PATHS
from pkdb_models.models.chlorzoxazone.experiments.alcohol_model import (
    Wilkinson1977Mean,
)
from pkdb_models.models.chlorzoxazone.experiments.studies import (
    Bedada2016,
    Bedada2017,
    Bedada2018,
    Benowitz2003,
    Burckart1998,
    Chalasani2003,
    Desiraju1983,
    DeVries1994,
    DeVries1994Mean,
    Dreisbach1995,
    Eap1998,
    Frye1998,
    Gade2018,
    Girre1994,
    He2019,
    Hohmann2019,
    Hukkanen2010,
    Kharasch1993,
    LaMaza2000,
    Leclercq1998,
    Liangpunsakul2005,
    Lucas1993,
    Mishin1998,
    OShea1994,
    Park2006,
    Puris2019,
    Rajnarayana2008,
    Vesell1995,
    Wang2003,
    Witt2016,
)

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share, so a named mapping is named with
#: its study
type NamedMappings = dict[str, set[str]]

#: the chlorzoxazone studies
EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
    Bedada2016,
    Bedada2017,
    Bedada2018,
    Benowitz2003,
    Burckart1998,
    Chalasani2003,
    Desiraju1983,
    DeVries1994,
    DeVries1994Mean,
    Dreisbach1995,
    Eap1998,
    Frye1998,
    Gade2018,
    Girre1994,
    He2019,
    Hohmann2019,
    Hukkanen2010,
    Kharasch1993,
    LaMaza2000,
    Leclercq1998,
    Liangpunsakul2005,
    Lucas1993,
    Mishin1998,
    OShea1994,
    Park2006,
    Puris2019,
    Rajnarayana2008,
    Vesell1995,
    Wang2003,
    Witt2016,
]

#: the ethanol studies of the alcohol model
ALCOHOL_EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [Wilkinson1977Mean]

#: health of the training data: healthy or not reported
CONTROL_HEALTH: frozenset[Health] = frozenset({Health.HEALTHY, Health.NR})

#: coadministrations without an interaction with chlorzoxazone: their arms are
#: training data like the arms without a coadministration. `COCKTAIL` is
#: chlorzoxazone as one of the probe drugs of a phenotyping cocktail, whose
#: doses are chosen to not interact; acetaminophen (Desiraju1983) neither
#: inhibits nor induces CYP2E1 at a single therapeutic dose
NO_INTERACTION: frozenset[Coadministration] = frozenset(
    {
        Coadministration.NONE,
        Coadministration.COCKTAIL,
        Coadministration.ACETAMINOPHEN,
    }
)

#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {
    # the free 6-hydroxychlorzoxazone of the three studies of Bedada is one
    # figure in the three papers (the curves of the inhibitor arms are
    # identical as well) and contradicts their tables (Cmax 0.31, 0.22 and
    # 0.20 µg/ml against a mean peak of 0.17 µg/ml)
    "Bedada2016": {"fm_bedada2016_czx6oh_250"},
    "Bedada2017": {"fm_bedada2017_czx6oh_250"},
    "Bedada2018": {"fm_bedada2018_czx6oh_250"},
    # the reference arm: an exposure 2.8 times below the other studies of 250
    # to 500 mg, the concentrations are below the lowest calibrator of 2 µg/ml
    "Rajnarayana2008": {"fm_Fig1_250"},
    # subject W.S.: a delayed renal elimination of 6-hydroxychlorzoxazone
    # (urinary half-life 3.1 hr), a mechanism the model does not have
    "Vesell1995": {"fm_Fig1_WS_250"},
}

#: the validation of the interactions: the arms with a coadministered drug,
#: simulated with factors of CYP2E1 (`LI__f_cyp2e1`) and of the CYP2E1
#: independent elimination (`LI__f_czxother`) from the observed ratios, which
#: are not fitted (`interactions` of the base experiment)
INTERACTION_VALIDATION: NamedMappings = {
    # chlormethiazole in alcoholics in withdrawal, CL/F ratio 0.315
    "Eap1998": {"fm_Fig1_czx_250_alcoholics", "fm_Fig1_czx6oh_250_alcoholics"},
    # disulfiram, CL ratio 0.15 (subject 5 and the urinary recovery of the
    # group)
    "Kharasch1993": {"fm_Fig2_dsf", "fm_Tab2Mean_dsf"},
    # watercress (AUC ratio 1.52) and isoniazid (AUC ratio 2.25), subject 4
    "Leclercq1998": {
        "fm_Fig1_czx_watercress_500",
        "fm_Fig1_czx6oh_watercress_500",
        "fm_Fig1_czx_isoniazid_500",
        "fm_Fig1_czx6oh_isoniazid_500",
    },
    # aspirin, no interaction (AUC ratio 0.95)
    "Park2006": {"fm_Fig1_czx_asa_400", "fm_Fig1_czx6oh_asa_400"},
    # diosmin, AUC ratio 1.66: the factor is derived from the ratio of the
    # study, the validation is the ratio, not the level
    "Rajnarayana2008": {"fm_Fig1_diosmin_250"},
}

#: the validation of the doses: single subjects over the dose range, which the
#: mean data of the training predict
DOSE_VALIDATION: NamedMappings = {
    # plasma of single subjects after 250 and 500 mg
    "Vesell1995": {
        "fm_Fig3_JR_500",
        "fm_Fig3_TG_500",
        "fm_Fig3_CM_500",
        "fm_Fig3_EG_500",
        "fm_Fig3_JW_500",
        "fm_Fig3_WS_250",
    },
    # one subject from 2.5 µg to 5 mg (solutions): the linear range and the
    # half-life of solutions
    "Witt2016": {
        *(f"fm_CZX{k}_chlorzoxazone" for k in range(1, 9)),
        *(f"fm_CZX{k}_6_hydroxychlorzoxazone" for k in range(2, 9)),
    },
}

#: the validation of populations which the model describes by the body weight
#: alone (obesity, diabetes) and of the variability of single subjects
POPULATION_VALIDATION: NamedMappings = {
    # obesity, BMI 31
    "Chalasani2003": {"fm_Fig1", "fm_Tab1"},
    # whole blood of single subjects, 250 mg
    "DeVries1994": {f"fm_Subject_{k}_po_CZX250" for k in range(1, 18)},
    # one representative subject, 500 mg
    "Dreisbach1995": {"fm_Fig4_czx", "fm_Fig4_czx6oh"},
    # obese children and adolescents
    "Gade2018": {"fm_Fig1_o_czx", "fm_Fig1_o_czx6oh"},
    # subject 5, the control of the disulfiram arm
    "Kharasch1993": {"fm_Fig2"},
    # obese nonalcoholics
    "LaMaza2000": {"fm_Fig1_na_o_750"},
    # subject 4, the control of the watercress and isoniazid arms
    "Leclercq1998": {"fm_Fig1_czx_500", "fm_Fig1_czx6oh_500"},
    # single control subjects and an obese woman
    "OShea1994": {
        "fm_Fig1_control_czx",
        "fm_Fig1_control_czx6oh",
        "fm_Fig2_control_czx",
        "fm_Fig2_control_czx6oh",
        "fm_Fig2_obese_czx",
        "fm_Fig2_obese_czx6oh",
    },
    # obesity with fatty liver disease
    "Puris2019": {"fm_Fig1_obese_62p5"},
    # type 1 and (obese) type 2 diabetes
    "Wang2003": {
        "fm_Fig1_DT1",
        "fm_Tab3_recovery_DT1",
        "fm_Fig1_DT2",
        "fm_Tab3_recovery_DT2",
    },
}

#: the validation of the limitations of the model: valid data of the induction
#: of CYP2E1 by alcohol and by fasting, which the model does not describe and
#: which would distort the fitted parameters of the processes it does describe
LIMITATION_VALIDATION: NamedMappings = {
    # alcoholics, normal weight and obese
    "LaMaza2000": {"fm_Fig1_a_nw_750", "fm_Fig1_a_o_750"},
    # moderate drinkers
    "Liangpunsakul2005": {"fm_Fig1_alcohol", "fm_Tab2_alcohol"},
    # alcoholics
    "Lucas1993": {
        "fm_Fig2_czx_alcoholics_500",
        "fm_Fig2_czx6oh_alcoholics_500",
        "fm_Tab5_czx6oh_alcoholics_500",
    },
    # recently drinking and abstinent alcoholics
    "Mishin1998": {
        "fm_Fig1_rda_750",
        "fm_Fig1_aa_750",
        "fm_Fig2_rda_750",
        "fm_Fig2_aa_750",
        "fm_Fig7_750",
        "fm_Fig8_750",
    },
    # subject 5 after a fast of 38 hr
    "OShea1994": {"fm_Fig1_fasting_czx", "fm_Fig1_fasting_czx6oh"},
}

#: the summaries of data which the fits use one by one and the same subjects
#: counted twice, excluded from every fit
AGGREGATE_MAPPINGS: NamedMappings = {
    # the mean of the single subjects of DeVries1994
    "DeVries1994Mean": {"fm_interpol_250"},
    # 250 mg of the 6 subjects of the crossover with 750 mg, who are part of
    # the 16 subjects of Fig1
    "Frye1998": {"fm_Fig3A_250", "fm_Fig3B_250", "fm_Fig4_250"},
    # the test tablet of the crossover, the same 20 subjects as the reference
    "He2019": {"fm_CZX400_TEST_400"},
    # the five normal subjects of the mean `fm_Fig1_mean`
    "Vesell1995": {
        "fm_Fig1_BL_250",
        "fm_Fig1_EG_250",
        "fm_Fig1_SM_250",
        "fm_Fig1_MF_250",
        "fm_Fig1_CN_250",
    },
}

#: the validation data by the question it answers
VALIDATION_QUESTIONS: dict[str, NamedMappings] = {
    "interactions": INTERACTION_VALIDATION,
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}

#: the validation data
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(mappings.get(study, set()) for mappings in VALIDATION_QUESTIONS.values())
    )
    for mappings in VALIDATION_QUESTIONS.values()
    for study in mappings
}


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_control(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """The mean data of healthy subjects without an interacting drug.

    The named validation data and outliers pass; every other mapping of a
    population, of a single subject or with an interacting drug stays out of
    the selection altogether.
    """
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping) or named(
        OUTLIER_MAPPINGS, fit_mapping_key, fit_mapping
    ):
        return True
    metadata = mapping_metadata(fit_mapping)
    return (
        metadata.health in CONTROL_HEALTH
        and metadata.coadministration in NO_INTERACTION
        and metadata.data_type != DataType.INDIVIDUAL
    )


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    experiment_classes: Sequence[type[SimulationExperiment]] = EXPERIMENT_CLASSES,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`). The outliers are `OUTLIER_MAPPINGS`, the
    validation data is `VALIDATION_MAPPINGS`. Neither kind enters the cost;
    both are simulated and evaluated with the training data, so a report says
    how the fitted parameters describe data they were not fitted on.

    Args:
        filters: filters of the training data.
        experiment_classes: the experiments whose mappings are selected; the
            named mappings are checked against the chlorzoxazone studies.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=experiment_classes,
        base_path=CHLORZOXAZONE_PATH,
        data_path=DATA_PATHS,
    )
    if experiment_classes is EXPERIMENT_CLASSES:
        for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, VALIDATION_MAPPINGS]:
            check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {
        key
        for sid, keys in OUTLIER_MAPPINGS.items()
        if sid in fit_mappings.experiments
        for key in keys
    }
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(
            VALIDATION_MAPPINGS, key, fit_mapping
        ),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in VALIDATION_QUESTIONS.items()
        )
    )
    return selection.collections


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """Pharmacokinetic data of chlorzoxazone."""
    return mapping_collections([filter_control])


def f_collections_alcohol() -> dict[str, list[FitMappingCollection]]:
    """Blood ethanol of the alcohol model."""
    return mapping_collections([], experiment_classes=ALCOHOL_EXPERIMENT_CLASSES)


#: the data of the fit problems, the keys are the subsets of the fits
COLLECTIONS: dict[str, Callable[[], dict[str, list[FitMappingCollection]]]] = {
    # the pharmacokinetics of chlorzoxazone
    "PK": f_collections_pk,
    # ethanol
    "ALCOHOL": f_collections_alcohol,
}


if __name__ == "__main__":
    for subset, f_collections in COLLECTIONS.items():
        console.rule(title=subset, align="left", style="white")
        f_collections()
