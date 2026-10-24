"""The simulation experiments of the chlorzoxazone model and their groups.

They are the registry of `MODEL`, the experiments its commands simulate.
"""

from sbmlsim.experiment import SimulationExperiment

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.alcohol_model import (
    AlcoholDosing,
    AlcoholInduction,
    AlcoholMetabolism,
    Mishin1998Induction,
    Mishin1998Sampling,
    Oneta2002Induction,
    Oneta2002Sampling,
    Wilkinson1977,
    Wilkinson1977Mean,
)
from pkdb_models.models.chlorzoxazone.experiments.misc import (
    ApplicationExperiment,
    Bedada,
)
from pkdb_models.models.chlorzoxazone.experiments.scans import (
    CirrhosisScan,
    CZXDoseCyp2e1ActivityScan,
    Ernstgard2004,
    EthnicitySampling,
    MetabolicRatiosScan,
    Mishin1998Scan,
    Orellana2006,
    PKPScan,
    VariabilitySampling,
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

EXPERIMENTS: dict[str, list[type[SimulationExperiment]]] = {
    "studies": [
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
    ],
    "misc": [
        # oral doses of 50 mg to 750 mg chlorzoxazone
        ApplicationExperiment,
        # the three studies of Bedada in one figure
        Bedada,
    ],
    "scans": [
        # pharmacokinetics against the CYP2E1 activity and its affinity
        PKPScan,
        # metabolic ratios against the parameters of metabolism and absorption
        MetabolicRatiosScan,
        # CYP2E1 activity and liver cirrhosis
        CirrhosisScan,
        # CYP2E1 activities sampled from the amounts in human liver microsomes
        CZXDoseCyp2e1ActivityScan,
        EthnicitySampling,
        VariabilitySampling,
        # scans against the data of studies
        Ernstgard2004,
        Mishin1998Scan,
        Orellana2006,
    ],
    "alcohol": [
        # ethanol pharmacokinetics
        AlcoholMetabolism,
        Wilkinson1977,
        Wilkinson1977Mean,
        # induction of CYP2E1 by ethanol
        AlcoholDosing,
        AlcoholInduction,
        Mishin1998Induction,
        Mishin1998Sampling,
        Oneta2002Induction,
        Oneta2002Sampling,
    ],
}
EXPERIMENTS["all"] = (
    EXPERIMENTS["studies"]
    + EXPERIMENTS["misc"]
    + EXPERIMENTS["scans"]
    + EXPERIMENTS["alcohol"]
)


if __name__ == "__main__":
    MODEL.run_simulation_experiments(EXPERIMENTS["all"], MODEL.simulation_dir / "all")
