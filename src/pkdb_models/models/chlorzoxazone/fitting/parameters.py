"""The fit parameters of the chlorzoxazone model.

The pharmacokinetics are fitted on plasma (serum) chlorzoxazone, total
6-hydroxychlorzoxazone in plasma and urine and free 6-hydroxychlorzoxazone in
plasma after oral doses. No study has intravenous data: the fraction absorbed
is fixed to 1 (`GU__F_czx_abs`, 71-74 % of the dose are recovered as
6-hydroxychlorzoxazone in the urine). Fixed are as well the liver partition
`LI__CZX_F_EX` (equivalent to the Km of CYP2E1 and the rate of the second
pathway), the blood to plasma ratio `BP_czx` (0.51, DeVries1994) and the
tissue distribution (`ftissue_czx`, `Kp_czx`, see the model: no study samples a
distribution phase, the fits put both at their lower bounds with flat
profiles). The fit adjusts the absorption and the dissolution of tablets, the
CYP2E1 6-hydroxylation (Vmax and Km, separated by the doses from 2.5 µg to
750 mg), the CYP2E1 independent elimination, the glucuronidation of
6-hydroxychlorzoxazone and the renal excretion of the glucuronide.

The ethanol parameters of the alcohol model are fitted on the blood ethanol of
Wilkinson1977 (`parameters_alcohol`); the Km of the ethanol elimination is not
identified by these data (flat profile likelihood from 0.05 to 5 mM) and is
fixed to the literature value (2.17 mM, Holford1987).
"""

from sbmlsim.fit import FitParameter

#: the pharmacokinetics of chlorzoxazone
parameters_pk: list[FitParameter] = [
    # absorption: solutions peak at about 0.5 hr (Hohmann2019, Witt2016), ka
    # 2.28 1/hr (Desiraju1983) and 2.0 1/hr (Leclercq1998)
    FitParameter(
        pid="GU__Ka_abs_czx",
        start_value=1.7,
        lower_bound=0.3,
        upper_bound=10,
        unit="1/hr",
    ),
    # dissolution and stomach passage of tablets, tmax 0.8-2 hr
    FitParameter(
        pid="Ka_dis_tablet_czx",
        start_value=3.1,
        lower_bound=0.2,
        upper_bound=20,
        unit="1/hr",
    ),
    # CYP2E1 6-hydroxylation: CL/F 612-805 ml/min after microdoses, 250-400
    # ml/min after 250-750 mg (Hohmann2019, Witt2016, Frye1998, Kharasch1993);
    # Km 14-110 µM in human liver microsomes (Yang2012, Emoto2003, Emoto2005)
    FitParameter(
        pid="LI__CZXOX_Vmax",
        start_value=0.0082,
        lower_bound=1e-4,
        upper_bound=1,
        unit="mmole/min/l",
    ),
    FitParameter(
        pid="LI__CZXOX_Km",
        start_value=0.0085,
        lower_bound=1e-4,
        upper_bound=0.5,
        unit="mM",
    ),
    # CYP2E1 independent elimination: 71-74 % of the dose recovered as
    # 6-hydroxychlorzoxazone (Desiraju1983, Kharasch1993), 58-70 % in most
    # studies, remaining clearance 158-191 ml/min (Frye1998)
    FitParameter(
        pid="LI__CZXOTHER_k",
        start_value=0.19,
        lower_bound=1e-3,
        upper_bound=2,
        unit="1/min",
    ),
    # glucuronidation: free 6-hydroxychlorzoxazone 1.4-3.3 % of chlorzoxazone
    # 0.5 hr after microdoses (Witt2016, Hohmann2019)
    FitParameter(
        pid="LI__CZXOGLU_k",
        start_value=100,
        lower_bound=1,
        upper_bound=1e4,
        unit="1/min",
    ),
    # renal excretion of the glucuronide relative to the GFR: renal clearance
    # of total 6-hydroxychlorzoxazone 464-506 ml/min (Frye1998)
    FitParameter(
        pid="KI__CZXOGLU_EX_f",
        start_value=10,
        lower_bound=0.5,
        upper_bound=50,
        unit="dimensionless",
    ),
]

#: the ethanol of the alcohol model
parameters_alcohol: list[FitParameter] = [
    # elimination 8.5 g/hr/70 kg (Holford1987), 0.044 mmole/min/kg
    FitParameter(
        pid="LI__ETHEL_VMAX",
        start_value=0.044,
        lower_bound=0.01,
        upper_bound=0.2,
        unit="mmole/min/kg",
    ),
    FitParameter(
        pid="GU__Ka_abs_eth",
        start_value=2.594,
        lower_bound=0.3,
        upper_bound=20,
        unit="1/hr",
    ),
    # Widmark factor 0.6-0.7 l/kg
    FitParameter(
        pid="Kp_ethanol",
        start_value=0.559,
        lower_bound=0.3,
        upper_bound=1.5,
        unit="dimensionless",
    ),
]
