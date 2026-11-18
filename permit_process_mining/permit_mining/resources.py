"""Section 3 - resource analysis (workload, processing time, resource/activity matrix)."""
import os

import matplotlib.pyplot as plt
import pandas as pd

from .config import OUTPUT_DIR


def _prepare_duration(data_df):
    data_df["startDate"] = pd.to_datetime(data_df["startDate"])
    data_df["endDate"] = pd.to_datetime(data_df["endDate"])
    data_df["org:resource"] = data_df["org:resource"].astype(str)
    # duration of each event in days
    data_df["duration"] = (data_df["endDate"] - data_df["startDate"]).dt.total_seconds() / 86400
    return data_df


def average_processing_time(data_df, output_dir=OUTPUT_DIR):
    """Average processing time per case, activity and resource; exported to CSV."""
    data_df = _prepare_duration(data_df)

    average_duration_case_activity = (
        data_df.groupby(["org:resource", "concept:name", "case_id"])["duration"]
        .mean()
        .unstack(fill_value=0)
    )
    average_duration_case_activity.reset_index(inplace=True)
    average_duration_case_activity.rename(
        columns={"org:resource": "Resource", "concept:name": "Activity", "case_id": "Case"},
        inplace=True,
    )

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "average_processing_time_case_activity_resource.csv")
    average_duration_case_activity.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Average processing times per case, activity, and resource exported to '{output_file}'.")

    print("\nPreview of average processing times:")
    print(average_duration_case_activity.head(10))
    return average_duration_case_activity


def analyze_workload(data_df):
    """Workload per resource: counts, durations, overlaps, Gantt chart."""
    data_df = _prepare_duration(data_df)

    # 1. number of activities per resource
    activity_count = data_df.groupby("org:resource").size().sort_values(ascending=False)
    print("Number of activities per resource:")
    print(activity_count)

    # 2. average processing time per resource
    average_duration = data_df.groupby("org:resource")["duration"].mean().sort_values(ascending=False)
    print("\nAverage processing time (in days) per resource:")
    print(average_duration)

    # 3. total processing time (workload) per resource
    total_duration = data_df.groupby("org:resource")["duration"].sum().sort_values(ascending=False)
    print("\nTotal processing time (in days) per resource:")
    print(total_duration)

    # 4. overlapping activities per resource
    print("\nNumber of overlapping activities per resource:")
    for resource, activities in data_df.groupby("org:resource"):
        activities = activities.sort_values("startDate")
        activities["overlap"] = activities["startDate"] < activities["endDate"].shift()
        overlap_count = activities["overlap"].sum()
        print(f"Resource: {resource}, Overlapping activities: {overlap_count}")

    # 5. Gantt chart
    print("\nGenerating Gantt chart...")
    plt.figure(figsize=(12, 8))
    for i, (resource, activities) in enumerate(data_df.groupby("org:resource")):
        plt.barh(
            [i] * len(activities),
            (activities["endDate"] - activities["startDate"]).dt.total_seconds(),
            left=(activities["startDate"] - data_df["startDate"].min()).dt.total_seconds(),
            label=resource,
        )
    plt.xlabel("Time (seconds from start)")
    plt.ylabel("Resources")
    plt.title("Gantt Chart of Resource Activities")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small", title="Resources")
    plt.tight_layout()
    plt.show()

    # 6. performance by activity type (only if such a column exists)
    if "activity_type" in data_df.columns:
        performance_by_type = data_df.groupby(["activity_type", "org:resource"])["duration"].mean().unstack()
        print("\nPerformance (average duration) by activity type and resource:")
        print(performance_by_type)
    else:
        print("\nNo 'activity_type' column found in the dataset to analyze performance by activity type.")


def resource_activity_table(log, output_dir=OUTPUT_DIR):
    """Resource x activity count table for every resource column; exported to CSV.

    Returns (combined_table, resource_activity_df).
    """
    # Propagate the case-level 'Responsible_actor' to the event level
    for trace in log:
        responsible_actor = trace.attributes.get("Responsible_actor", None)
        for event in trace:
            event["Responsible_actor"] = responsible_actor

    resource_columns = ["org:resource", "monitoringResource", "Responsible_actor"]
    resource_activity_count = {}
    resource_activity_df = None

    for col in resource_columns:
        if col in log[0][0]:
            pairs = [(event[col], event["concept:name"]) for trace in log for event in trace]
            resource_activity_df = pd.DataFrame(pairs, columns=["Resource", "Activity"])
            resource_activity_count[col] = (
                resource_activity_df.groupby(["Resource", "Activity"]).size().unstack(fill_value=0)
            )

    combined = pd.concat(resource_activity_count.values(), keys=resource_activity_count.keys())
    print(combined.to_csv(sep="\t", index=True))

    os.makedirs(output_dir, exist_ok=True)
    combined.to_csv(os.path.join(output_dir, "resource_activity_table.csv"), index=True, sep=",", encoding="utf-8")
    return combined, resource_activity_df


def check_event_counts(log, resource_activity_df):
    """Sanity check: events in the log vs. events counted in the DataFrame."""
    total_events = sum(len(trace) for trace in log)
    counted_events = resource_activity_df.shape[0]
    print(f"Total events in the log: {total_events}")
    print(f"Total events counted in the DataFrame: {counted_events}")
