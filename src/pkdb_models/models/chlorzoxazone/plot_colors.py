"""Colors of the figures of the chlorzoxazone experiments."""

from matplotlib.colors import LinearSegmentedColormap, to_rgb

from pkdb_models.models.chlorzoxazone.experiments.base_experiment import Sids

plot_colors_sid: dict[str, str] = {
    Sids.cpl_czx: "#252525",
    Sids.cbl_czx: "#252525",
    Sids.cve_czx6oh: "#3690c0",  # "royalblue",
    Sids.cve_czx6oh_all: "#fe9929",  # "navy",
    Sids.aurine_czxoglu: "#b30000",
}

plot_colors: dict[str, str] = {
    "czx": "#252525",
    "czx6oh": "#3690c0",  # "royalblue"
}

greys = ["#d9d9d9", "#bdbdbd", "#969696", "#737373", "#525252", "#252525"]
blues = ["#d0d1e6", "#a6bddb", "#74a9cf", "#3690c0", "#0570b0", "#034e7b"]

cmap_greys = LinearSegmentedColormap.from_list("greys", [to_rgb(x) for x in greys])
cmap_blues = LinearSegmentedColormap.from_list("oranges", [to_rgb(x) for x in blues])
