"""Process discovery: Petri nets, DFGs and BPMN models for the different log variants."""
import matplotlib.pyplot as plt
import pm4py

from .config import ACTIVITY_CLASSIFICATION, ACTIVITY_MAPPING, ACTIVITY_MAPPING_DETAILED, EXCLUDED_YEAR
from .utils import (
    calculate_trend,
    dfg_plotter,
    simplify_activity_name,
    simplify_and_map_activity_name,
    yearly_activity_table,
)


def discover_and_view(log, petri_net=True, dfg=True, bpmn=True):
    """Run the Inductive Miner on `log` and show Petri net, DFG and BPMN model."""
    if petri_net:
        model = pm4py.algo.discovery.inductive.algorithm.apply(log)
        net, initial_marking, final_marking = pm4py.convert_to_petri_net(model)
        pm4py.view_petri_net(net, initial_marking, final_marking)
    if dfg:
        dfg_digraph = dfg_plotter(log)
        pm4py.visualization.dfg.visualizer.view(dfg_digraph)
    if bpmn:
        bpmn_model = pm4py.discover_bpmn_inductive(log)
        pm4py.view_bpmn(bpmn_model)


# ---- 1.2.1 Whole process ------------------------------------------------------------

def discover_log_A(log_copy_A):
    """Log A: activity names without details (e.g. 01_HOOFD)."""
    simplified_log_A = simplify_activity_name(log_copy_A)
    discover_and_view(simplified_log_A)
    return simplified_log_A


def discover_log_B(log_copy_B):
    """Log B: simplified names replaced by readable descriptions."""
    log_B = simplify_and_map_activity_name(log_copy_B, ACTIVITY_MAPPING)
    discover_and_view(log_B)
    return log_B


def discover_log_C(log_copy_C):
    """Log C: simplified names plus description (\"code: description\")."""
    log_C = simplify_and_map_activity_name(log_copy_C, ACTIVITY_MAPPING_DETAILED)
    discover_and_view(log_C)
    return log_C


# ---- 1.2.2 Main process -------------------------------------------------------------

def discover_main_process(log_filtered_activities_D):
    """BPMN model (Inductive Miner) of the main process."""
    bpmn_model = pm4py.discover_bpmn_inductive(log_filtered_activities_D)
    pm4py.view_bpmn(bpmn_model)


def heuristics_petri_net(log_copy_D):
    """Heuristics Miner Petri net of the main process."""
    net, im, fm = pm4py.discover_petri_net_heuristics(log_copy_D)
    pm4py.view_petri_net(net, im, fm)


def discover_log_E(log_copy_E):
    """Log E: main-process activities manually grouped into categories."""
    log_E = simplify_and_map_activity_name(log_copy_E, ACTIVITY_CLASSIFICATION)
    discover_and_view(log_E)
    return log_E


# ---- yearly activity usage ----------------------------------------------------------

def plot_yearly_activity_usage(log, exclude_year=None):
    """Plot yearly event counts per activity and print them (with a trend column) as a
    tab-separated table that can be pasted into Excel.

    exclude_year: drop this year from the plot and the table (e.g. an incomplete year).
    Returns the yearly table including the trend column.
    """
    table = yearly_activity_table(log)
    if exclude_year is not None:
        table = table.loc[:, table.columns != exclude_year]

    plt.figure(figsize=(12, 6))
    for activity in table.index:
        plt.plot(table.columns, table.loc[activity], label=activity)
    plt.title("Activity Usage Over Time (Yearly)")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=5, fontsize=10)
    plt.show()

    table = table.copy()
    table["trend"] = table.apply(calculate_trend, axis=1)
    print(table.to_csv(sep="\t", index=True))
    return table


def yearly_bpmn_models(logs_by_window):
    """Discover and show a BPMN model for each time-window log."""
    models = []
    for window_log in logs_by_window:
        bpmn_model = pm4py.discover_bpmn_inductive(window_log)
        pm4py.view_bpmn(bpmn_model)
        models.append(bpmn_model)
    return models
