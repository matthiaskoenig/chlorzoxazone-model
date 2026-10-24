"""Simulation experiment of the study OShea1994."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, override

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
from sbmlsim.plot.plotting import AxisScale
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


@dataclass(frozen=True)
class Subject:
    """A simulated subject: body weight (kg), height (cm) if reported, label."""

    bw: float
    height: float | None
    label: str


class OShea1994(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of OShea1994.

    Chlorzoxazone single 250 mg tablet (Pioneer Pharmaceutical); plasma and
    urine after hydrolysis with Helix pomatia juice (total chlorzoxazone and
    6-hydroxychlorzoxazone).

    Fasting study: 6 healthy men (75-93 kg, 83 kg) after an overnight fast
    (8-14 hr) and at least 7 days later after a 38 hr fast; Fig. 1 subject 5
    (80 kg, height not reported) in both arms, Tables I and II the means
    (urinary 6-hydroxychlorzoxazone 62.7 % of the dose in 24 hr).

    Obesity study: 9 obese (119 kg, BMI 44.0) and 9 age-matched control women
    (72 kg, BMI 25.6) after an overnight fast; Fig. 2 control subject 2 (54 kg,
    BMI 21.3) and obese subject 2 (102 kg, BMI 40.0) of Table III, the height
    sqrt(BW/BMI).

    The model has no effect of a prolonged fast on CYP2E1 (CL/F 0.64 of the
    overnight fast) and no induction by obesity besides the scaling with the
    body weight.
    """

    subjects: ClassVar[Mapping[str, Subject]] = {
        "subject5": Subject(80.0, None, "subject 5"),
        "control_woman2": Subject(54.0, 159.0, "control woman 2"),
        "obese_woman2": Subject(102.0, 160.0, "obese woman 2"),
        # the mean of the men of the fasting study, the urinary recovery
        "mean_man": Subject(83.0, None, "men"),
        # the mean of the control women (Table III), the PK of the women
        "mean_woman": Subject(72.0, 168.0, "control women"),
    }

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their id, one per figure, arm and substance."""
        meta = {}
        for fig_id, sheet, prefix, task_id in [
            ("Fig1_control", "Fig1", "Tab1_Healthy_5_healthy", "subject5"),
            ("Fig1_fasting", "Fig1", "Tab1_Healthy_5_fasting", "subject5_fasting"),
            (
                "Fig2_control",
                "Fig2",
                "Tab1_TC_control_1_control_women",
                "control_woman2",
            ),
            ("Fig2_obese", "Fig2", "Tab1_TC_obsese_1_obese_women", "obese_woman2"),
        ]:
            for substance, yid, label, mr in [
                ("czx", Sids.cpl_czx, self.label_czx, self.Mr.czx),
                ("czx6oh", Sids.cve_czx6oh_all, self.label_czx6oh_all, self.Mr.czx6oh),
            ]:
                dset_substance = (
                    "chlorzoxazone" if substance == "czx" else "6-hydroxychlorzoxazone"
                )
                meta[f"{fig_id}_{substance}"] = HelperMapping(
                    id=sheet,
                    plot_ylabel=label,
                    yid=yid,
                    sim_time_factor=9,
                    unit="µM",
                    dset_label=f"{prefix}_{dset_substance}",
                    unit_conversion=1 / mr,
                    dset_yid="value",
                    task_id=task_id,
                )
        # the urinary recovery in percent of the dose, as mmole of the dose
        meta["Tab1_2Mean"] = HelperMapping(
            id="Tab1_2Mean",
            plot_ylabel=self.label_czxoglu_urine,
            yid=Sids.aurine_czxoglu,
            sim_time_factor=25,
            unit="mmole",
            dset_label="Tab1Mean_recovery_healthy",
            unit_conversion=Q(250, "mg") / self.Mr.czx,
            dset_yid="mean",
            task_id="mean_man",
        )
        return meta

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, hm in self.FigMeta.items():
            df = self.load_dataframe(required(hm.id))
            df = df[df["label"] == hm.dset_label]
            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion(hm.dset_yid, required(hm.unit_conversion))
            dsets[f"dset_{fig_id}"] = dset
        return dsets

    def changes(self, subject: Subject) -> dict[str, Quantity]:
        """Get the changes of the simulation of a subject."""
        changes: dict[str, Quantity] = {
            **self.default_changes(ApplicationForm.TABLET),
            "PODOSE_czx": Q(250, "mg"),
            "BW": Q(subject.bw, "kg"),
        }
        if subject.height is not None:
            changes["HEIGHT"] = Q(subject.height, "cm")
        return changes

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {
            task_id: Simulation(
                time_unit="min",
                end=25 * 60,
                preinit_changes=self.changes(subject),
            )
            for task_id, subject in self.subjects.items()
        }
        # the 38 hr fast: no effect of fasting in the model, the subject as
        # after the overnight fast
        tcsims["subject5_fasting"] = Simulation(
            time_unit="min",
            end=25 * 60,
            preinit_changes=self.changes(self.subjects["subject5"]),
        )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, hm in self.FigMeta.items():
            individual = hm.dset_yid == "value"
            mappings[f"fm_{fig_id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{fig_id}",
                    xid="time",
                    yid=required(hm.dset_yid),
                    count="count",
                    yid_sd=None if individual else "mean_sd",
                ),
                observable=FitData(
                    self, task=f"task_{hm.task_id}", xid="time", yid=required(hm.yid)
                ),
                metadata=PKPDMappingMetaData(
                    # single subjects (Fig1, Fig2), mean urinary recovery (Tab1_2Mean)
                    tissue=Tissue.PLASMA if individual else Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.OBESE
                    if fig_id.startswith("Fig2_obese")
                    else Health.HEALTHY,
                    # overnight fast, or 38 hr without food (Fig1_fasting)
                    fasting=Fasting.FASTED,
                    data_type=DataType.INDIVIDUAL if individual else DataType.MEAN,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for fig_name, arms in [
            ("Fig1", ["Fig1_control", "Fig1_fasting"]),
            ("Fig2", ["Fig2_control", "Fig2_obese"]),
        ]:
            fig = Figure(
                experiment=self,
                sid=fig_name,
                num_rows=1,
                num_cols=2,
                name=f"{self.__class__.__name__} {fig_name} (250 mg)",
            )
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr", max=9), legend=True
            )
            for plot, substance in zip(plots, ["czx", "czx6oh"], strict=True):
                for arm, color in zip(arms, [None, "tab:red"], strict=True):
                    hm = self.FigMeta[f"{arm}_{substance}"]
                    yid = required(hm.yid)
                    plot.set_yaxis(
                        label=required(hm.plot_ylabel),
                        unit=hm.unit,
                        scale=AxisScale.LINEAR,
                    )
                    task_id = required(hm.task_id)
                    label = (
                        "subject 5, 38 hr fast"
                        if task_id == "subject5_fasting"
                        else self.subjects[task_id].label
                    )
                    plot.add_data(
                        task=f"task_{task_id}",
                        xid="time",
                        yid=yid,
                        label=f"Sim {label}",
                        color=color or plot_colors_sid[yid],
                    )
                    plot.add_data(
                        dataset=f"dset_{arm}_{substance}",
                        xid="time",
                        yid="value",
                        count="count",
                        label=f"Data {label}",
                        color=color or plot_colors_sid[yid],
                    )
            figures[f"fig_{fig_name}"] = fig

        hm = self.FigMeta["Tab1_2Mean"]
        fig = Figure(
            experiment=self,
            sid="Tab1_2Mean",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} Table II (250 mg)",
        )
        plot = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", max=hm.sim_time_factor),
            yaxis=Axis(required(hm.plot_ylabel), unit=hm.unit, scale=AxisScale.LINEAR),
            legend=True,
        )[0]
        yid = required(hm.yid)
        plot.add_data(
            task=f"task_{hm.task_id}",
            xid="time",
            yid=yid,
            label="Sim men",
            color=plot_colors_sid[yid],
        )
        plot.add_data(
            dataset="dset_Tab1_2Mean",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="Data men",
            color=plot_colors_sid[yid],
        )
        figures["fig_Tab1_2Mean"] = fig
        return figures


if __name__ == "__main__":
    MODEL.run_experiments(OShea1994, output_dir="test")
