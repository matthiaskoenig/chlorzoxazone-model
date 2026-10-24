"""The models of chlorzoxazone and the matplotlib style of their figures."""

from typing import Any

from matplotlib.typing import RcKeyType

#: matplotlib style of the `figures_mpl`, applied with `matplotlib.rc_context`
rcParams: dict[RcKeyType, Any] = {
    "axes.labelsize": 18,
    "axes.labelweight": "bold",
    "axes.titlesize": 20,
    "figure.titlesize": 25,
    "figure.titleweight": "bold",
    "axes.titleweight": "bold",
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "legend.fontsize": 13,
}
