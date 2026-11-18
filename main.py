"""Run the building permit process mining analysis (BPIC15_1, Municipality 1).

Usage:
    python main.py --log data/BPIC15_1.xes                 # run everything
    python main.py --log data/BPIC15_1.xes --sections 1 3  # only discovery + resources
"""
import argparse

import matplotlib.pyplot as plt  # noqa: F401  (backend initialisation)

from precess_mining import (
    backup,
    conformance,
    config,
    data_loading,
    discovery,
    filtering,
    log_statistics,
    resources,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log", default=config.LOG_PATH, help="path to the BPIC15_1.xes event log")
    parser.add_argument(
        "--sections",
        nargs="+",
        type=int,
        default=[1, 2, 3],
        choices=[1, 2, 3, 4],
        help="1 = discovery, 2 = conformance checking, 3 = resources, 4 = backup visualisations",
    )
    parser.add_argument("--dot-dir", default=None, help="folder containing Graphviz `dot` (if it is not on PATH)")
    args = parser.parse_args()

    if args.dot_dir:
        backup.add_graphviz_to_path(args.dot_dir)

    # ---- 0. Preparation ------------------------------------------------------------
    log, _log_copy = data_loading.load_log(args.log)
    data_loading.inspect_first_trace(log)

    # ---- 1. Discovery --------------------------------------------------------------
    # The filtered logs are needed by all later sections, so they are always built.
    log_filtered_threshold, low_frequency_activities = filtering.filter_low_frequency_activities(
        log, show=1 in args.sections
    )
    copy_A, copy_B, copy_C, copy_D, copy_E, _copy_F = filtering.make_log_copies(log_filtered_threshold)

    if 1 in args.sections:
        # 1.1 Log statistics
        activity_counts = log_statistics.print_log_statistics(log)
        log_statistics.plot_event_occurrence(activity_counts)
        log_statistics.plot_events_over_time(log)
        log_statistics.plot_cumulative_activity_usage(log)

        # 1.2 Filtering
        filtering.filter_top_variants(log)

        # 1.2.1 Whole process
        simplified_log_A = discovery.discover_log_A(copy_A)
        log_statistics.plot_cumulative_activity_usage(simplified_log_A, legend_below=False)
        discovery.discover_log_B(copy_B)
        discovery.discover_log_C(copy_C)

        # 1.2.2 Main process
        log_filtered_activities_D = filtering.filter_main_process(copy_D)
        discovery.discover_main_process(log_filtered_activities_D)
        discovery.plot_yearly_activity_usage(log_filtered_activities_D)
        discovery.heuristics_petri_net(copy_D)

        log_E = discovery.discover_log_E(copy_E)
        discovery.plot_yearly_activity_usage(log_E, exclude_year=config.EXCLUDED_YEAR)

        # 1.2.3 Further exploration
        windows = filtering.filter_by_time_windows(log_E)
        discovery.yearly_bpmn_models(windows)
    else:
        # Sections 2 and 3 still need the simplified logs A and E
        from precess_mining.utils import simplify_activity_name, simplify_and_map_activity_name

        simplified_log_A = simplify_activity_name(copy_A)
        log_E = simplify_and_map_activity_name(copy_E, config.ACTIVITY_CLASSIFICATION)

    # ---- 2. Conformance checking -----------------------------------------------------
    if 2 in args.sections:
        conformance.alignment_conformance(simplified_log_A)
        conformance.token_replay_conformance(simplified_log_A)  # token replay A
        conformance.token_replay_conformance(log_E)  # token replay E

    # ---- 3. Resources ------------------------------------------------------------------
    if 3 in args.sections:
        # Resource analysis runs on the event table of log E (simplified + grouped activities)
        data_df = data_loading.log_to_dataframe(log_E)
        resources.average_processing_time(data_df)
        resources.analyze_workload(data_df)

        _table, resource_activity_df = resources.resource_activity_table(log_E)
        resources.check_event_counts(log_E, resource_activity_df)

    # ---- Backup: alternative views of the unfiltered log -------------------------------
    if 4 in args.sections:
        backup.inductive_bpmn(log)
        backup.inductive_process_tree(log)
        backup.inductive_petri_net(log)
        backup.dfg_view(log)
        filtering.restore_case_attributes(log, _log_copy, low_frequency_activities)


if __name__ == "__main__":
    main()
