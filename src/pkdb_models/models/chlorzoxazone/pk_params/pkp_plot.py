"""Plot the dose-normalized AUC of the control groups of the studies against the dose."""

import matplotlib.pyplot as plt
from sbmlsim import Q

from pkdb_models.models.chlorzoxazone.pk_params.pk_parameters import (
    Pkps,
    load_pk_params,
)

#: unit of the AUC
AUC_UNIT = "µmole/ml*hr"

if __name__ == "__main__":
    pkps = load_pk_params("all_control")
    df = pkps[pkps["measurement"] == Pkps.auc_inf]
    fig, ax = plt.subplots(1, 1)
    doses, aucs = [], []
    for _, row in df.iterrows():
        doses.append(row["dose"])
        aucs.append(Q(row["mean"], row["unit"]) / Q(169.56, "g/mole"))

    aucs_per_dose = Q.from_list(aucs).to(AUC_UNIT) / Q(doses, "mg")
    ax.plot(doses, aucs_per_dose, linestyle="none", marker="o")
    plt.show()
