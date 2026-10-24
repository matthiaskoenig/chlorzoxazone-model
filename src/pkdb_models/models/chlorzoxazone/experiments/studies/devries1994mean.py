"""Simulation experiment of DeVries1994, the mean of the individual data.

Chlorzoxazone (250 mg po, tablet); the individual chlorzoxazone time courses in
whole blood of 17 subjects are interpolated linearly to the reference time
points of the study and averaged.

The mean is derived from the subjects of DeVries1994 (the same data counted
twice) and is biased: values below the plotted range are missing, not zero, so
the means at 15 and 480 min are means of the subjects with a value. It is an
aggregate, not data of a fit.
"""

from collections.abc import Callable, Sequence
from typing import ClassVar, override

import numpy as np
import pandas as pd
import scipy.stats
from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


def create_lin_fun(
    xs: tuple[float, float], ys: tuple[float, float]
) -> Callable[[float], float]:
    """Get the linear function through two points.

    Args:
        xs: x values of the points.
        ys: y values of the points.

    Returns:
        The linear function.
    """
    m = (ys[1] - ys[0]) / (xs[1] - xs[0])
    n = ys[0] - m * xs[0]

    def lin(x: float) -> float:
        return m * x + n

    return lin


def get_start_end_index(
    time_vec: np.ndarray, ref_times: Sequence[float]
) -> tuple[int, int]:
    """Get the reference time points closest to the start and end of a time course.

    Args:
        time_vec: time points of the time course.
        ref_times: reference time points.

    Returns:
        The indices of the reference time points closest to the first and to the
        last time point.
    """
    start = np.argmin(np.abs(np.array(ref_times) - time_vec[0]))
    end = np.argmin(np.abs(np.array(ref_times) - time_vec[-1]))
    return int(start), int(end)


def interpolate_series(
    time_vec: np.ndarray, value_vec: np.ndarray, ref_times: Sequence[float]
) -> np.ndarray:
    """Interpolate a time course linearly to the reference time points.

    Only the reference time points between the ones closest to the start and the
    end of the time course get a value, the others are NaN.

    Args:
        time_vec: time points of the time course.
        value_vec: values of the time course.
        ref_times: reference time points.

    Returns:
        The values at the reference time points.
    """
    t_intervals = [(time_vec[i], time_vec[i + 1]) for i in range(len(time_vec) - 1)]
    y_intervals = [(value_vec[i], value_vec[i + 1]) for i in range(len(value_vec) - 1)]

    # linear functions between the interval boundaries (measured values)
    lin_functions = [
        create_lin_fun(xs, ys) for xs, ys in zip(t_intervals, y_intervals, strict=True)
    ]
    start, end = get_start_end_index(time_vec, ref_times)

    interpol = np.full(len(ref_times), np.nan)
    calc_values(start, end, interpol, ref_times, t_intervals, lin_functions)
    return interpol


def calc_values(
    start: int,
    end: int,
    interpol: np.ndarray,
    ref_times: Sequence[float],
    t_intervals: Sequence[tuple[float, float]],
    lin_functions: Sequence[Callable[[float], float]],
) -> None:
    """Set the interpolated values of the reference time points from start to end.

    A reference time point gets the value of the linear function of the interval
    it is in; left of the first interval the function of the first interval is
    extrapolated, right of the last interval the one of the last interval.

    Args:
        start: index of the first reference time point.
        end: index of the last reference time point.
        interpol: values at the reference time points, set in place.
        ref_times: reference time points.
        t_intervals: time intervals of the time course.
        lin_functions: linear functions of the intervals.
    """
    for i in range(start, end + 1):
        for k, ts in enumerate(t_intervals):
            if ts[0] < ref_times[i] <= ts[1]:
                interpol[i] = lin_functions[k](ref_times[i])
                break
        else:
            if ref_times[i] < t_intervals[0][0]:
                interpol[i] = lin_functions[0](ref_times[i])
            else:
                interpol[i] = lin_functions[-1](ref_times[i])


def calc_counts(array: np.ndarray) -> list[int]:
    """Get the number of values (not NaN) of every column."""
    return [
        int(np.count_nonzero(~np.isnan(array[:, i]))) for i in range(array.shape[1])
    ]


class DeVries1994Mean(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of DeVries1994 with the mean of the individual data.

    The individual chlorzoxazone time courses in whole blood after a single oral
    250 mg dose of 17 subjects are mapped to the reference time points of the
    study (15, 30, 45, 60, 90, 120, 150, 180, 240, 360, 480) [min], of which the
    mean, standard deviation and standard error are calculated. The 600 min
    sample of subjects 1-7 is left out: only subject 4 has a value there.
    """

    #: the number of subjects
    n_subjects: ClassVar[int] = 17

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        interpolated_serieses = []
        ref_time_points = [15, 30, 45, 60, 90, 120, 150, 180, 240, 360, 480]
        for fig_id in ["Fig1", "Fig2"]:
            df = self.load_dataframe(fig_id, study="DeVries1994")
            interpolated_serieses.append(
                np.vstack(
                    [
                        interpolate_series(
                            df_individual["t_actual"].to_numpy(),
                            df_individual["value"].to_numpy(),
                            ref_time_points,
                        )
                        for _, df_individual in df.groupby("individual")
                    ]
                )
            )
        interpol = np.concatenate(interpolated_serieses, axis=0)
        means = np.nanmean(interpol, axis=0)
        stds = np.nanstd(interpol, axis=0)
        stds[stds == 0] = np.nan
        # the number of subjects with a value at the time point
        counts = calc_counts(interpol)
        # the standard error of a single value is not defined (the last time
        # point has one subject), it is NaN as its standard deviation
        sems = np.full(means.size, np.nan)
        several = np.array(counts) > 1
        sems[several] = scipy.stats.sem(interpol[:, several], axis=0, nan_policy="omit")
        units = ["µg/ml" for _ in range(means.size)]
        time_units = ["min" for _ in range(means.size)]

        pkdb_dummy = pd.DataFrame(
            {
                "time": ref_time_points,
                "mean": means,
                "sd": stds,
                "se": sems,
                "unit": units,
                "time_unit": time_units,
                "count": counts,
            }
        )
        dset = DataSet.from_df(pkdb_dummy, self.ureg)
        dset.unit_conversion("mean", 1 / self.Mr.czx)
        dsets["dset_interpol"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["interpol"] = Simulation(
            time_unit="min",
            end=10 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(250, "mg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        mappings["fm_interpol_250"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="dset_interpol",
                xid="time",
                yid="mean",
                count=self.n_subjects,
                yid_sd="mean_sd",
                yid_se="mean_se",
            ),
            observable=FitData(
                self, task="task_interpol", xid="time", yid=Sids.cbl_czx
            ),
            metadata=PKPDMappingMetaData(
                tissue=Tissue.BLOOD,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                data_type=DataType.MEAN,
            ),
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1&2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=1,
            name=f"DeVries1994 {name}",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)

        plots[0].set_yaxis(label=f"{self.label_czx} (blood)", unit="µM", scale="linear")

        # simulation
        plots[0].add_data(
            task="task_interpol",
            xid="time",
            yid=Sids.cbl_czx,
            label="Sim",
            color=plot_colors_sid[Sids.cbl_czx],
        )

        plots[0].add_data(
            dataset="dset_interpol",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            label="Data",
            color=plot_colors_sid[Sids.cbl_czx],
            count=self.n_subjects,
        )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(DeVries1994Mean, output_dir="test")
