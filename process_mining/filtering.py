"""Section 1.2 - filtering the log (variants, frequency, main process, time windows)."""
import copy

import pm4py
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.statistics.attributes.log import get as attributes_getter

from .config import FREQUENCY_THRESHOLD, MAIN_PROCESS_ACTIVITIES, NUMBER_OF_VARIANTS, TIME_WINDOWS
from .utils import dfg_plotter


def filter_top_variants(log, number_of_variants=NUMBER_OF_VARIANTS, show=True):
    """Keep the most common variants and (optionally) show their DFG."""
    variants = variants_filter.get_variants(log)
    print(len(variants))

    log_filtered = pm4py.filter_variants_top_k(log, number_of_variants)
    if show:
        dfg_digraph = dfg_plotter(log_filtered)
        pm4py.visualization.dfg.visualizer.view(dfg_digraph)
    return log_filtered


def filter_low_frequency_activities(log, frequency_threshold=FREQUENCY_THRESHOLD, show=True):
    """Remove activities that occur less often than `frequency_threshold`.

    Returns (filtered_log, list_of_removed_activities).
    """
    activity_frequencies = attributes_getter.get_attribute_values(log, "concept:name")
    low_frequency_activities = [
        activity for activity, freq in activity_frequencies.items() if freq < frequency_threshold
    ]

    log_filtered = attributes_filter.apply_events(
        log,
        low_frequency_activities,
        parameters={
            attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
            attributes_filter.Parameters.POSITIVE: False,  # exclude the listed activities
        },
    )

    print("Columns before filtering:", log[0][0].keys())
    print("Columns after filtering:", log_filtered[0][0].keys())

    if show:
        dfg_digraph = dfg_plotter(log_filtered)
        pm4py.visualization.dfg.visualizer.view(dfg_digraph)
    return log_filtered, low_frequency_activities


def make_log_copies(log, n=6):
    """Deep copies of a log. Renaming activities modifies a log in place, so every
    variant (A..F) of the analysis works on its own copy."""
    return [copy.deepcopy(log) for _ in range(n)]


def filter_main_process(log, activities=MAIN_PROCESS_ACTIVITIES):
    """Keep only the 01_HOOFD (main process) activities."""
    parameters = {
        attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
        attributes_filter.Parameters.POSITIVE: True,
    }
    return attributes_filter.apply(log, activities, parameters)


def filter_by_time_windows(log, windows=TIME_WINDOWS):
    """Return one log per time window (traces fully contained in the window)."""
    return [timestamp_filter.filter_traces_contained(log, start, end) for start, end in windows]


def restore_case_attributes(log, log_copy, low_frequency_activities):
    """Backup snippet: filter events while preserving case-level attributes."""
    case_attributes = {trace.attributes["concept:name"]: trace.attributes for trace in log}

    log_filtered = attributes_filter.apply_events(
        log_copy,
        low_frequency_activities,
        parameters={
            attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name",
            attributes_filter.Parameters.POSITIVE: False,
        },
    )

    for trace in log_filtered:
        case_id = trace.attributes["concept:name"]
        if case_id in case_attributes:
            trace.attributes.update(case_attributes[case_id])

    print("Case attributes (after filtering):", log_filtered[0].attributes.keys())
    print("Event attributes (after filtering):", log_filtered[0][0].keys())
    return log_filtered
