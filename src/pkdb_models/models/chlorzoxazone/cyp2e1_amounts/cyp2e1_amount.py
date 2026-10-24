"""Figures of the CYP2E1 amounts and activities in human liver microsomes.

Literature research and digitization of the CYP2E1 content and the chlorzoxazone
6-hydroxylation activity in human liver microsomes (HLM), in `cyp2e1_amounts.xlsx`.
`fit_and_plot_cyp2e1` fits log-normal distributions to the CYP2E1 amounts and
saves them with `helper.save_result`, which the sampling scans read.

TODO: add figures and info to the google docs
TODO: literature research about factors affecting CYP2E1 content
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from scipy.stats import linregress, norm

from pkdb_models.models.chlorzoxazone.cyp2e1_amounts.helper import save_result

#: colors of the methods which measured the CYP2E1 amounts, grey for the others
METHOD_COLORS: dict[str, str] = {
    "LC−MS/MS": "cadetblue",
    "HPLC-MS/MS": "cadetblue",
    "ELISA": "skyblue",
    "Immunoblot": "steelblue",
}

#: colors of the ethnicities: caucasian, japanese, chinese
ETHNICITY_COLORS: dict[str, str] = {
    "ca": "mistyrose",
    "ja": "indianred",
    "ch": "maroon",
}


def load_data(sheet: str) -> pd.DataFrame:
    """Load a sheet of the CYP2E1 amounts and activities.

    Args:
        sheet: the sheet, `Data`, `Data1` or `Data2`.

    Returns:
        The data of the sheet.
    """
    file = Path(__file__).parent / "cyp2e1_amounts.xlsx"
    return pd.read_excel(file, sheet_name=sheet)


def get_colors(df: pd.DataFrame) -> dict[str, tuple[float, float, float, float]]:
    """Get the colors of the studies of the data.

    Args:
        df: data with the column `study`.

    Returns:
        The color by study.
    """
    studies = df["study"].unique()
    return {
        study: plt.cm.Spectral(i / (len(studies) - 1))
        for i, study in enumerate(studies)
    }


def coefficient_of_variation(log10_data: pd.Series) -> float:
    """Get the coefficient of variation of log-normal data (Canchola2017).

    Args:
        log10_data: the decadic logarithm of the data.

    Returns:
        The coefficient of variation in percent.
    """
    return np.sqrt(np.power(10, np.log(10) * np.var(log10_data)) - 1) * 100


def fit_and_plot_cyp2e1() -> None:
    """Fit log-normal distributions to the CYP2E1 amounts and plot them with the data.

    The distributions of the caucasian and the japanese donors are saved with
    `save_result`.
    """
    df_all = load_data("Data")
    fig, axes = plt.subplots(nrows=2, ncols=2, dpi=300, figsize=(12, 10))
    axes[1, 0].set_xlabel("Log(CYP2E1 content) (pmol/mg protein)")
    axes[1, 1].set_xlabel("CYP2E1 content (pmol/mg protein)")
    for ax in axes[:, 0]:
        ax.set_ylabel("Probability")

    axes[0, 0].set_title("CYP2E1 amounts in HLM (caucasian)")
    axes[1, 0].set_title("CYP2E1 amounts in HLM (japanese)")
    axes[0, 1].set_title("Log CYP2E1 amounts in HLM (caucasian)")
    axes[1, 1].set_title("Log CYP2E1 amounts in HLM (japanese)")
    all_colors = get_colors(df_all)

    plot_studies_colors = {}
    for i, ethnicity in enumerate(["caucasian", "japanese"]):
        df = df_all[df_all["ethnicity"].str.contains(ethnicity)]

        # fit normal distribution to log(data)
        mu, std = norm.fit(np.log(df["amount"]))

        # save fit results and used data points together
        save_result(df=df, mu=mu, sigma=std, identifier=ethnicity)

        x = np.linspace(0, 6, 100)
        p = norm.pdf(x, mu, std)

        # plot results
        data = []
        colors = []
        for study, df_study in df.groupby("study"):
            label = str(study)
            data.append(df_study["amount"].values)
            colors.append(all_colors[label])
            plot_studies_colors[label] = all_colors[label]

        log_data = [np.log(arr) for arr in data]
        axes[i, 0].hist(
            log_data,
            density=True,
            stacked=True,
            color=colors,
            edgecolor="black",
            alpha=0.7,
        )
        axes[i, 0].plot(
            x,
            p,
            label=f"log-normal fit:\n$\\mu$={mu:.2f}\n$\\sigma$={std:.2f}\n",
            color="black",
            linewidth=2.0,
        )
        axes[i, 1].hist(
            data, density=True, stacked=True, color=colors, edgecolor="black", alpha=0.7
        )

    handles = [Patch(color=c, label=study) for study, c in plot_studies_colors.items()]
    axes[0, 1].legend(
        frameon=False, handles=handles, loc="upper left", bbox_to_anchor=(1, 1)
    )

    for ax in axes[:, 0]:
        ax.legend(frameon=False)
        ax.set_xlim(left=0, right=6)

    for ax in axes[:, 1]:
        ax.set_xlim(left=0, right=200)

    fig.tight_layout()
    plt.show()


def plot_activity_vs_cyp2e1_amount() -> None:
    """Plot the 6-hydroxylation activity against the CYP2E1 amount by study.

    Prints the mean and the standard deviation of the logarithm of the activity
    of every study.
    """
    df_all = load_data(sheet="Data")
    df = df_all[~pd.isnull(df_all["czx6_hydroxylation"])]
    ax: Axes
    fig, ax = plt.subplots(1, 1, dpi=600)
    colors_all = get_colors(df_all)
    for study, df_study in df.groupby("study"):
        label = str(study)
        m, n, r, _, _ = linregress(df_study["amount"], df_study["czx6_hydroxylation"])
        x = np.linspace(df_study["amount"].min(), df_study["amount"].max(), 50)
        ax.plot(x, m * x + n, linestyle="-", color="black")
        ax.scatter(
            df_study["amount"],
            df_study["czx6_hydroxylation"],
            facecolor=colors_all[label],
            edgecolor="black",
            label=f"{label} r={r:.2f}",
        )
        print(
            label,
            np.mean(np.log(df_study["czx6_hydroxylation"])),
            np.std(np.log(df_study["czx6_hydroxylation"])),
        )

    ax.set_ylabel("6-hydroxylation activity [nmol/min/mg(protein)]")
    ax.set_xlabel("CYP2E1 [pmol/mg(protein)]")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1, 1))

    fig.tight_layout()
    plt.show()


def plot_cyp_amount_vs_bmi() -> None:
    """Plot the CYP2E1 amount against the BMI of the donors of Couto2019."""
    df_all = load_data("Data")
    df = df_all[df_all["study"] == "Couto2019"]
    ax: Axes
    fig, ax = plt.subplots(1, 1, dpi=600)
    colors_all = get_colors(df_all)
    for study, df_study in df.groupby("study"):
        label = str(study)
        m, n, r, _, _ = linregress(df_study["bmi"], df_study["amount"])
        x = np.linspace(df_study["bmi"].min(), df_study["bmi"].max(), 50)
        ax.plot(x, m * x + n, linestyle="-", color="black")
        ax.scatter(
            df_study["bmi"],
            df_study["amount"],
            facecolor=colors_all[label],
            edgecolor="black",
            label=f"{label} r={r:.2f}",
        )

    ax.set_xlabel("BMI [kg/m^2]")
    ax.set_ylabel("CYP2E1 [pmol/mg(protein)]")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1, 1))

    fig.tight_layout()
    plt.show()


def box_plot_protein_amount_distributions() -> None:
    """Box plots of the logarithm of the CYP2E1 amounts by study and ethnicity.

    The studies with at least 10 caucasian, chinese or japanese donors; the bars
    are the coefficients of variation, colored by the method of the measurement.
    """
    df_all = load_data("Data")
    df_ethnicities = df_all[
        df_all["ethnicity"].str.contains("caucasian")
        | df_all["ethnicity"].str.contains("chinese")
        | df_all["ethnicity"].str.contains("japanese")
    ]

    labels = []
    ax: Axes
    fig, ax = plt.subplots(1, 1, dpi=600)
    ax1: Axes = ax.twinx()
    ax1.set_zorder(0)
    ax.set_zorder(1)
    ax.patch.set_alpha(0)
    width = 1
    base_pos = 0

    for study, label_df in df_ethnicities.groupby("study"):
        if len(label_df) < 10:
            continue
        eth_groupby = label_df.groupby("ethnicity")
        labels.append(str(study))
        method = label_df["Method"].values[0]

        for k, (ethnicity, eth_df) in enumerate(eth_groupby):
            ethnicity = str(ethnicity)
            if len(eth_groupby) == 1:
                pos = base_pos
            if len(eth_groupby) == 2:
                if k == 0:
                    pos = base_pos - 1 / 4 * width
                if k == 1:
                    pos = base_pos + 1 / 4 * width
            data = np.log10(eth_df["amount"])

            box = ax.boxplot(
                x=data,
                positions=[pos],
                widths=0.7 * width / len(eth_groupby),
                patch_artist=True,
                medianprops={"color": "black"},
            )

            ax1.bar(
                x=pos,
                height=coefficient_of_variation(data),
                width=0.9 * width / len(eth_groupby),
                alpha=0.5,
                color=METHOD_COLORS.get(method, "grey"),
            )

            eth = "NR"
            if "caucasian" in ethnicity:
                eth = "ca"
            if "japanese" in ethnicity:
                eth = "ja"
            if "chinese" in ethnicity:
                eth = "ch"

            for patch in box["boxes"]:
                patch.set_facecolor(ETHNICITY_COLORS[eth])

        base_pos += 1

    ax.set_xticks(range(len(labels)), labels, rotation=90)
    ax.set_ylabel("log CYP2E1 amounts [pmol/mg(protein)]")
    ax1.set_ylabel("coefficient of variation [%]")
    fig.tight_layout()

    plt.show()


def plot_vmax_dist() -> None:
    """Plot the distribution of the logarithm of the 6-hydroxylation activity by study."""
    df_all = load_data("Data")
    df_all1 = load_data("Data1")
    df_all2 = load_data("Data2")
    df0 = df_all[~pd.isnull(df_all["czx6_hydroxylation"])]
    df1 = df_all1[df_all1["czx6_hydroxylation_unit"] == "nmol/min/mg(protein)"]
    df2 = df_all2[df_all2["czx6_hydroxylation_unit"] == "nmol/min/mg(protein)"]

    data = []
    labels = []
    for df in [df0, df1, df2]:
        for study, df_study in df.groupby("study"):
            data.append(df_study["czx6_hydroxylation"].values * 1000)
            labels.append(str(study))

    ax: Axes
    fig, ax = plt.subplots(1, 1, dpi=600)

    log_data = [np.log10(d) for d in data]
    colors = [plt.cm.Spectral(i / (len(labels) - 1)) for i in range(len(labels))]
    ax.hist(
        log_data,
        density=True,
        bins="sqrt",
        stacked=True,
        color=colors,
        edgecolor="black",
        alpha=0.7,
    )

    handles = [
        Patch(color=c, label=study) for study, c in zip(labels, colors, strict=True)
    ]
    ax.legend(frameon=False, handles=handles, loc="upper left", bbox_to_anchor=(1, 1))
    ax.set_ylabel("frequency")
    ax.set_xlabel("log 6-hydroxylation activity [pmol/min/mg(protein)]")
    fig.tight_layout()

    plt.show()


def plot_km_vmax_scatter() -> None:
    """Scatter plot of the 6-hydroxylation activity against the Km of Yang2012.

    Prints the mean Km of every ethnicity.
    """
    df_all = load_data("Data2")
    df = df_all[df_all["study"] == "Yang2012"]
    ax: Axes
    _, ax = plt.subplots(1, 1, dpi=600)
    for _, df_label in df.groupby("ethnicity"):
        print("mean")
        print(np.mean(df_label["Km"]))
        colors = [
            "white" if row["ethnicity"] == "caucasian" else "grey"
            for _, row in df_label.iterrows()
        ]
        ax.scatter(
            x=df_label["Km"],
            y=df_label["czx6_hydroxylation"],
            c=colors,
            edgecolor="black",
        )


def box_plot_vmax_distributions() -> None:
    """Box plots of the logarithm of the 6-hydroxylation activity by study and ethnicity.

    The studies with at least 10 caucasian, chinese or japanese donors; the bars
    are the coefficients of variation.
    """
    essentials = [
        df[["study", "czx6_hydroxylation", "czx6_hydroxylation_unit", "ethnicity"]]
        for df in [load_data("Data"), load_data("Data1"), load_data("Data2")]
    ]

    concat_df = pd.concat(essentials, ignore_index=True, axis=0)
    concat_df = concat_df[~pd.isnull(concat_df["czx6_hydroxylation"])]
    concat_df = concat_df[
        concat_df["czx6_hydroxylation_unit"] == "nmol/min/mg(protein)"
    ]

    concat_df = concat_df[
        concat_df["ethnicity"].str.contains("caucasian")
        | concat_df["ethnicity"].str.contains("chinese")
        | concat_df["ethnicity"].str.contains("japanese")
    ]
    labels = []
    ax: Axes
    fig, ax = plt.subplots(1, 1, dpi=600)
    ax1: Axes = ax.twinx()
    ax1.set_zorder(0)
    ax.set_zorder(1)
    ax.patch.set_alpha(0)
    width = 1
    base_pos = 0

    for study, label_df in concat_df.groupby("study"):
        if len(label_df) < 10:
            continue
        eth_groupby = label_df.groupby("ethnicity")
        labels.append(str(study))

        for k, (ethnicity, eth_df) in enumerate(eth_groupby):
            ethnicity = str(ethnicity)
            if len(eth_groupby) == 1:
                pos = base_pos
            if len(eth_groupby) == 2:
                if k == 0:
                    pos = base_pos - 1 / 4 * width
                if k == 1:
                    pos = base_pos + 1 / 4 * width
            data = np.log10(eth_df["czx6_hydroxylation"] * 1000)

            box = ax.boxplot(
                x=data,
                positions=[pos],
                widths=0.7 * width / len(eth_groupby),
                patch_artist=True,
                medianprops={"color": "black"},
            )

            ax1.bar(
                x=pos,
                height=coefficient_of_variation(data),
                width=0.9 * width / len(eth_groupby),
                alpha=0.5,
                color="grey",
            )

            eth = "NR"
            if "caucasian" in ethnicity:
                eth = "ca"
            if "japanese" in ethnicity:
                eth = "ja"
            if "chinese" in ethnicity:
                eth = "ch"

            for patch in box["boxes"]:
                patch.set_facecolor(ETHNICITY_COLORS[eth])

        base_pos += 1

    ax.set_xticks(range(len(labels)), labels, rotation=90)
    ax.set_ylabel("log CZX-6-hydroxalation [pmol/min/mg(protein)]")
    ax1.set_ylabel("coefficient of variation [%]")
    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    fit_and_plot_cyp2e1()
    plot_activity_vs_cyp2e1_amount()
    plot_cyp_amount_vs_bmi()
    plot_km_vmax_scatter()
    box_plot_protein_amount_distributions()
    plot_vmax_dist()
    box_plot_vmax_distributions()
