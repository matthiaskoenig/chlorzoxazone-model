"""Base class of the chlorzoxazone simulation experiments."""

import warnings
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar, NamedTuple, override

import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.axes import Axes
from matplotlib.colors import to_hex
from matplotlib.lines import Line2D
from matplotlib.typing import ColorType
from numpy.typing import ArrayLike
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS_END_STAGE, RENAL_FUNCTION_GFR
from pkpdsim.metadata import ApplicationForm
from pkpdsim.scan import point_band, point_timecourse, state_after_changes
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Change, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.chlorzoxazone_pk import (
    calculate_chlorzoxazone_pk,
)


def required[T](value: T | None) -> T:
    """Get a value which is required at this point, e.g. an optional field.

    Raises:
        ValueError: if the value is `None`.
    """
    if value is None:
        raise ValueError("Required value is None.")
    return value


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data."""

    czx: Quantity
    czx6oh: Quantity
    czxoglu: Quantity
    ethanol: Quantity


@dataclass
class HelperMapping:
    """Information of a dataset of a study: its figure, data, unit and simulation.

    Every experiment sets the fields it uses.
    """

    study: str | None = None
    id: str | None = None
    measurement: str | None = None
    mr: Quantity | None = None
    plot_ylabel: str | None = None
    plot_legend_label: str | None = None
    sim_time_factor: float | None = None
    yid: str | None = None
    dset_yid: str | None = None
    unit: str | None = None
    dset_label: str | None = None
    excel_sheet: str | None = None
    dose: float | None = None
    task_id: str | None = None
    body_weight: float | None = None
    body_height: float | None = None
    unit_conversion: Quantity | None = None


#: the fraction of the clearance of chlorzoxazone by the CYP2E1
#: 6-hydroxylation: the formation clearance of 6-hydroxychlorzoxazone is 2.30 of
#: 3.28 ml/min/kg (Kharasch1993), 71-74 % of the dose are recovered as
#: 6-hydroxychlorzoxazone (Desiraju1983, Kharasch1993)
FM_CYP2E1 = 0.7


def cyp2e1_activity(auc_ratio: float) -> float:
    """Get the CYP2E1 activity (`LI__f_cyp2e1`) of an observed AUC ratio.

    The clearance of chlorzoxazone is the CYP2E1 part `FM_CYP2E1` and the
    CYP2E1 independent rest; an inhibitor or inducer of CYP2E1 changes the
    first, the ratio of the clearances, the inverse of the AUC ratio, is
    `FM_CYP2E1 * f + (1 - FM_CYP2E1)`.

    Args:
        auc_ratio: AUC with the interacting drug over the AUC without it.

    Returns:
        The activity of CYP2E1, at least 0.
    """
    return max(0.0, (1 / auc_ratio - (1 - FM_CYP2E1)) / FM_CYP2E1)


#: the transparency of the band of the draws of the fitted parameters
BAND_ALPHA = 0.25


@dataclass(frozen=True)
class LineStyle:
    """The style of a line of a matplotlib figure, the median of the draws."""

    color: ColorType | None = None
    label: str | None = None
    marker: str = ""
    markeredgecolor: ColorType | None = None
    linestyle: str = "-"
    markerfacecolor: ColorType | None = None
    zorder: float = 2


def hex_color(color: ColorType) -> str:
    """Get a color as a hex string, e.g. the RGBA tuple of a colormap.

    The curves of an sbmlsim figure become bands in a run over the draws
    (`pkpdsim.uncertainty`), which take the color of the curve as a string.
    """
    return to_hex(color, keep_alpha=False)


class Sids(StrEnum):
    """Selections of the model which the experiments plot and fit.

    Chlorzoxazone is measured in plasma or serum (`cpl_czx`), whole blood is
    `cbl_czx` (blood to plasma ratio `BP_czx` 0.51, DeVries1994). The
    metabolites are plasma concentrations: free 6-hydroxychlorzoxazone
    (`cve_czx6oh`), its glucuronide (`cve_czxoglu`) and the total
    6-hydroxychlorzoxazone after the hydrolysis of the glucuronide
    (`cve_czx6oh_all`); the urine has the glucuronide (`aurine_czxoglu`), which
    the methods measure as total 6-hydroxychlorzoxazone after hydrolysis.
    """

    time = "time"
    podose_czx = "PODOSE_czx"
    cpl_czx = "[Cveplasma_czx]"
    cbl_czx = "[Cve_czx]"
    cve_czx6oh = "[Cve_czx6oh]"
    aurine_czxoglu = "Aurine_czxoglu"
    cli_czx = "[LI__czx]"
    cli_czx6oh = "[LI__czx6oh]"
    cve_czx6oh_all = "Cve_czx6oh_all"
    cve_czxoglu = "[Cve_czxoglu]"
    cve_ethanol = "[Cve_ethanol]"
    cli_cyp2e1 = "LI__cyp2e1"
    cli_ethanol = "[LI__ethanol]"
    li_kd_cyp2e1 = "LI__kd_cyp2e1"
    # the cases
    f_renal_function = "KI__f_renal_function"
    f_cirrhosis = "f_cirrhosis"
    f_cyp2e1 = "LI__f_cyp2e1"
    f_czxother = "LI__f_czxother"


def metabolic_ratio(
    res: ScanResult, ds: xr.Dataset | None = None, sid: str = Sids.cve_czx6oh_all
) -> xr.DataArray:
    """Get the metabolic ratio of a metabolite and chlorzoxazone in plasma.

    The ratio is undefined before the first dose of chlorzoxazone, where both
    concentrations are 0: it is NaN where chlorzoxazone is 0.

    Args:
        res: the result, for the units.
        ds: the data of the result, e.g. at some times; the whole result by
            default.
        sid: the metabolite, 6-OH-CZX + CZX-Glu by default.

    Returns:
        The ratio of every point (and draw) of the data.
    """
    ds = res.ds if ds is None else ds
    czx = ds[Sids.cpl_czx]
    factor = Q(1, res.units[sid]).to(res.units[Sids.cpl_czx]).magnitude
    return ds[sid] / czx.where(czx != 0) * factor


class ChlorzoxazoneSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the chlorzoxazone simulation experiments."""

    pkpd_model = MODEL
    selections = tuple(sid.value for sid in Sids)

    units: ClassVar[Mapping[str, str]] = {
        Sids.time: "hr",
        Sids.podose_czx: "mg",
        Sids.cpl_czx: "µM",
        Sids.cbl_czx: "µM",
        Sids.cve_czx6oh: "µM",
        Sids.cve_czx6oh_all: "µM",
        Sids.cve_czxoglu: "µM",
        Sids.aurine_czxoglu: "mmole",
        Sids.cli_czx: "nM",
        Sids.cli_czx6oh: "nM",
        Sids.cli_ethanol: "mM",
        Sids.cve_ethanol: "mM",
        Sids.cli_cyp2e1: "dimensionless",
        Sids.li_kd_cyp2e1: "1/min",
        Sids.f_renal_function: "dimensionless",
        Sids.f_cirrhosis: "dimensionless",
        Sids.f_cyp2e1: "dimensionless",
        Sids.f_czxother: "dimensionless",
    }
    labels: ClassVar[Mapping[str, str]] = {
        Sids.time: "time",
        Sids.cpl_czx: "chlorzoxazone plasma",
        Sids.cbl_czx: "chlorzoxazone blood",
        Sids.cve_czx6oh: "6-OH-CZX plasma",
        Sids.cve_czxoglu: "6-OH-CZX-glucuronide plasma",
        Sids.cve_czx6oh_all: "6-OH-CZX (total) plasma",
        Sids.aurine_czxoglu: "6-OH-CZX (total) urine",
        Sids.cli_czx: "chlorzoxazone liver",
        Sids.cli_czx6oh: "6-OH-CZX liver",
    }
    label_czx: ClassVar[str] = "Chlorzoxazone"
    label_czx6oh: ClassVar[str] = "6-OH-CZX"
    label_time: ClassVar[str] = "Time"
    label_czx6oh_all: ClassVar[str] = "6-OH-CZX + 6-OH-CZX-Glu"
    label_czxoglu_urine: ClassVar[str] = "6-OH-CZX-Glu (urine)"

    # ----------- Renal function --------------
    #: the renal function relative to a GFR of 101 ml/min (`KI__f_renal_function`),
    #: a measured creatinine clearance of X ml/min is X/101
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS_END_STAGE

    # ----------- Interactions --------------
    #: the activities of CYP2E1 (`LI__f_cyp2e1`) and of the CYP2E1 independent
    #: elimination (`LI__f_czxother`) with an interacting drug: literature
    #: values which are not fitted, the arms are validation data. An AUC ratio
    #: is converted with `cyp2e1_activity`
    interactions: ClassVar[Mapping[str, Mapping[str, float]]] = {
        # disulfiram 500 mg 10 hr before: its metabolite diethyldithiocarbamate
        # inactivates CYP2E1 irreversibly; formation clearance of
        # 6-hydroxychlorzoxazone 0.17 of 2.30 ml/min/kg (7 %), the remaining
        # clearance 0.32 of 0.98 ml/min/kg (34 %), the clearance 15 % of the
        # control (Kharasch1993)
        "disulfiram": {"LI__f_cyp2e1": 0.074, "LI__f_czxother": 0.34},
        # isoniazid 300 mg/day for 7 days, the last dose 2 hr before: inhibition
        # of CYP2E1, AUC x2.25 (Leclercq1998)
        "isoniazid": {"LI__f_cyp2e1": cyp2e1_activity(2.25), "LI__f_czxother": 1.0},
        # watercress 50 g the evening before: phenethyl isothiocyanate inhibits
        # CYP2E1, AUC x1.52 (Leclercq1998)
        "watercress": {"LI__f_cyp2e1": cyp2e1_activity(1.52), "LI__f_czxother": 1.0},
        # diosmin 500 mg/day for 9 days: inhibition of CYP2E1, AUC x1.66
        # (Rajnarayana2008)
        "diosmin": {"LI__f_cyp2e1": cyp2e1_activity(1.66), "LI__f_czxother": 1.0},
    }

    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        czx=Q(169.56, "g/mole"),
        czx6oh=Q(185.56, "g/mole"),
        czxoglu=Q(361.69, "g/mole"),
        ethanol=Q(46.07, "g/mole"),
    )

    @override
    def default_changes(
        self, formulation: ApplicationForm = ApplicationForm.TABLET
    ) -> dict[str, Quantity]:
        """Changes of every simulation: the dissolution of the formulation.

        The fitted parameters are part of the model and are not changed in the
        simulations: a parameter which is fitted must not be set by a simulation,
        otherwise the fit problem cannot be written as PEtab. The formulation
        sets the dissolution of the dose, a solution or a tablet.

        Args:
            formulation: formulation of the dose, a tablet by default (the
                dissolution of the model, `application_form` 0).

        Returns:
            The changes.
        """
        return {
            "application_form": Q(
                1 if formulation == ApplicationForm.SOLUTION else 0, "dimensionless"
            ),
        }

    def calculate_chlorzoxazone_pk(
        self, scans: Iterable[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of the scans.

        Args:
            scans: keys of the simulations, all simulations by default.

        Returns:
            The parameters of every scan by simulation key, per draw of the
            fitted parameters in a run over them (`uncertainty`).
        """
        keys = self._simulations if scans is None else scans
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            key: calculate_chlorzoxazone_pk(
                experiment=self, res=self.results[f"task_{key}"], across=across
            )
            for key in keys
        }

    #: the dose states of the model, from which the doses are absorbed or infused
    dose_states: ClassVar[frozenset[str]] = frozenset(
        {"PODOSE_czx", "IVDOSE_czx", "PODOSE_ethanol", "GU__PODOSE_ethanol"}
    )

    def segments_simulation(
        self,
        durations: Sequence[float],
        changes: Sequence[Mapping[str, Any]],
        steps_per_segment: int | None = None,
        times: Sequence[float] | None = None,
    ) -> Simulation:
        """Get the simulation of consecutive segments, e.g. the days of a dosing.

        The changes of the first segment are applied before the initialization of
        the model, the changes of every other segment at its start. A dose of a
        later segment (a change of a dose state) adds to the dose state, so the
        rest of the earlier doses is kept (`add_doses`). The output is uniform
        with as many points as the segments had together, or at the given times.

        Args:
            durations: durations of the segments in hours.
            changes: changes of the segments, one per segment.
            steps_per_segment: output steps per segment.
            times: the output times in hours instead of the steps.

        Returns:
            The simulation of the segments.

        Raises:
            ValueError: if not exactly one of the steps and the times is given.
        """
        if (steps_per_segment is None) == (times is None):
            raise ValueError("Either the steps per segment or the times are given.")
        # the segments in minutes, the time unit of the model
        starts = np.cumsum([0.0, *(duration * 60 for duration in durations)])
        return Simulation(
            time_unit="min",
            end=float(starts[-1]),
            steps=None
            if steps_per_segment is None
            else steps_per_segment * len(durations),
            times=None if times is None else [60 * t for t in times],
            preinit_changes=dict(changes[0]),
            changes=[
                self.segment_change(float(start), change)
                for start, change in zip(starts[1:-1], changes[1:], strict=True)
                if change
            ],
        )

    def segment_change(self, start: float, change: Mapping[str, Any]) -> Change:
        """Get the change at the start of a segment, whose doses add to the states.

        Args:
            start: start of the segment in minutes.
            change: changes of the segment, doses and other values.

        Returns:
            The change, the doses as additions to their dose states.
        """
        doses = {sid: v for sid, v in change.items() if sid in self.dose_states}
        values = {sid: v for sid, v in change.items() if sid not in self.dose_states}
        if doses:
            values.update(self.add_doses(start, doses).values)
        return Change(start, values)

    def result_on_time_grid(self, task_id: str) -> ScanResult:
        """Get the result of a task on the grid of its time points, each once.

        The output of sbmlsim has the states before and after a change at its
        time; the figures of the experiments read the state after it, as
        sbmlsim 0.8 gave it (`pkpdsim.scan.state_after_changes`). The time is
        the dimension `time`; a scan of the steps of the integrator is on the
        time points of a figure, a few hundred, so the analyses of a figure
        (`at_time`, `mr_at`, the NCA) read the result of the task itself.

        Args:
            task_id: id of the task.

        Returns:
            The result on the grid of its time points.
        """
        return state_after_changes(self.results[self.to_sid(task_id)])

    @staticmethod
    def at_time(res: ScanResult, time: float) -> xr.Dataset:
        """Get the data of a result at a time, interpolated between its time points.

        The output of a simulation are the steps of the integrator, whose time
        points need not include the time.

        Args:
            res: the result of a task, or the result on the grid of its time
                points (`result_on_time_grid`).
            time: the time [min].

        Returns:
            The data of every point (and draw) of the result at the time.
        """
        return res.interpolate([time]).ds.isel(time=0)

    def mr_at(
        self, res: ScanResult, hr: float, sid: str = Sids.cve_czx6oh_all
    ) -> np.ndarray:
        """Get the metabolic ratio of every point of a result at a time, per draw.

        Args:
            res: the result of a task, or the result on the grid of its time
                points (`result_on_time_grid`).
            hr: the time [hr].
            sid: the metabolite, 6-OH-CZX + CZX-Glu by default.

        Returns:
            The ratio of every point of the scan, the draws as the last axis.
        """
        return self.draw_values(
            metabolic_ratio(res, self.at_time(res, hr * 60), sid=sid)
        )

    # ----------- Draws of the fitted parameters --------------
    # A run over the draws of the fitted parameters (`run_simulation
    # pkdb_models.models.chlorzoxazone --uncertainty`) adds the dimension of the
    # draws to every result. The figures of the experiments draw the median of
    # the draws with the band of their quantiles; a value of a figure is
    # calculated for every draw, the draws are the last axis of its array.
    @property
    def draws(self) -> str | None:
        """The dimension of the draws of the fitted parameters, `None` without."""
        return None if self.uncertainty is None else self.uncertainty.id

    def population(self, samples: np.ndarray, size: int) -> np.ndarray:
        """Get the individuals of a sampled population which are simulated.

        In a run over the draws every individual is simulated with every draw:
        the population of the figures is the first `size` individuals times the
        draws, so that the run keeps a size which the memory allows.

        Args:
            samples: the sampled values of the individuals.
            size: the individuals in a run over the draws.

        Returns:
            The values of the simulated individuals.
        """
        if self.draws is None:
            return samples
        return samples[:size]

    def draw_values(self, values: xr.DataArray) -> np.ndarray:
        """Get the values of an array with the draws as the last axis.

        Args:
            values: the values, e.g. a variable at a time of every point of a scan.

        Returns:
            The values with the draws as the last axis, an axis of one value
            without draws.
        """
        draws = self.draws
        if draws is None or draws not in values.dims:
            return np.asarray(values.values, dtype=float)[..., np.newaxis]
        return np.asarray(values.transpose(..., draws).values, dtype=float)

    def band(self, values: ArrayLike) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get the quantiles and the median of the draws, the last axis of the values.

        Args:
            values: the values with the draws as the last axis.

        Returns:
            The lower quantile, the median and the upper quantile; without draws
            the values themselves, three times.
        """
        array = np.asarray(values, dtype=float)
        low, high = (
            (0.5, 0.5) if self.uncertainty is None else self.uncertainty.quantiles
        )
        # a value which is NaN in every draw (e.g. a metabolic ratio before the
        # first dose) has no quantile, it is NaN
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            lower, median, upper = np.nanquantile(array, [low, 0.5, high], axis=-1)
        return lower, median, upper

    def plot_band(
        self, ax: Axes, x: ArrayLike, values: ArrayLike, style: LineStyle
    ) -> Line2D:
        """Plot the median of the draws with the band of their quantiles.

        Args:
            ax: the axes.
            x: the x values.
            values: the y values with the draws as the last axis.
            style: the style of the line of the median.

        Returns:
            The line of the median.
        """
        return self.plot_bands(ax, x, *self.band(values), style=style)

    def plot_bands(
        self,
        ax: Axes,
        x: ArrayLike,
        lower: np.ndarray,
        median: np.ndarray,
        upper: np.ndarray,
        style: LineStyle,
    ) -> Line2D:
        """Plot the median and, in a run over the draws, the band between the quantiles.

        Args:
            ax: the axes.
            x: the x values.
            lower: the lower quantile.
            median: the median, the line.
            upper: the upper quantile.
            style: the style of the line of the median.

        Returns:
            The line of the median.
        """
        (line,) = ax.plot(
            x,
            median,
            color=style.color,
            label=style.label,
            marker=style.marker,
            markeredgecolor=style.markeredgecolor,
            markerfacecolor=style.markerfacecolor,
            linestyle=style.linestyle,
            zorder=style.zorder,
        )
        if self.draws is not None:
            ax.fill_between(
                np.asarray(x, dtype=float),
                lower,
                upper,
                color=line.get_color(),
                alpha=BAND_ALPHA,
                linewidth=0,
                zorder=style.zorder - 0.1,
            )
        return line

    def timecourse_band(
        self,
        res: ScanResult,
        sid: str,
        units: tuple[str, str],
        point: Mapping[str, int] | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Get the timecourse of a variable, the median of the draws with their quantiles.

        Args:
            res: the result of a simulation or a scan.
            sid: the variable.
            units: the units of the time and of the variable.
            point: the position along the dimensions of a scan.

        Returns:
            The time, the lower quantile, the median and the upper quantile;
            without draws the timecourse three times.
        """
        time_unit, unit = units
        point = dict(point or {})
        run = self.uncertainty
        if run is None:
            time, values = point_timecourse(res, sid, **point)
            lower = median = upper = values
        else:
            time, lower, median, upper = point_band(
                res, sid, across=run.id, quantiles=run.quantiles, **point
            )
        lower, median, upper = (
            Q(v, res.units[sid]).to(unit).magnitude for v in (lower, median, upper)
        )
        return (
            Q(time, res.units["time"]).to(time_unit).magnitude,
            lower,
            median,
            upper,
        )

    def plot_timecourse(
        self,
        ax: Axes,
        res: ScanResult,
        sid: str,
        units: tuple[str, str],
        style: LineStyle,
        point: Mapping[str, int] | None = None,
    ) -> Line2D:
        """Plot the timecourse of a variable, the median of the draws with their band.

        Args:
            ax: the axes.
            res: the result of a simulation or a scan.
            sid: the variable.
            units: the units of the time and of the variable of the plot.
            style: the style of the line of the median.
            point: the position along the dimensions of a scan.

        Returns:
            The line of the median.
        """
        return self.plot_bands(
            ax, *self.timecourse_band(res, sid, units, point), style=style
        )
