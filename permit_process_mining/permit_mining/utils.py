"""Helper functions shared by several analysis steps."""
import pandas as pd
import pm4py


def dfg_plotter(log_plot):
    """Build a directly-follows-graph visualisation for a log."""
    dfg_relations = pm4py.algo.discovery.dfg.algorithm.apply(log_plot)
    dfg_digraph = pm4py.visualization.dfg.visualizer.apply(dfg_relations, log=log_plot)
    return dfg_digraph


def simplify_activity_name(event_log):
    """Keep only the first two parts of each activity name, e.g. 01_HOOFD_010 -> 01_HOOFD."""
    for trace in event_log:
        sorted_events = sorted(trace, key=lambda x: x["time:timestamp"] if "time:timestamp" in x else 0)
        for i, event in enumerate(sorted_events):
            trace[i] = event
        for event in trace:
            event["concept:name"] = "_".join(event["concept:name"].split("_")[:2])
    return event_log


def simplify_and_map_activity_name(event_log, mapping):
    """Order events by timestamp, shorten the activity name and look it up in `mapping`.

    Names are first tried in the mapping in their full form (e.g. 01_HOOFD_010),
    then in their shortened form (e.g. 01_HOOFD). Unknown names keep the short form.
    """
    for trace in event_log:
        sorted_events = sorted(trace, key=lambda x: x["time:timestamp"] if "time:timestamp" in x else 0)
        for i, event in enumerate(sorted_events):
            trace[i] = event

        for event in trace:
            full_name = event["concept:name"]
            simplified_activity = "_".join(full_name.split("_")[:2])  # e.g. '01_BB'
            if full_name in mapping:
                event["concept:name"] = mapping[full_name]
            elif simplified_activity in mapping:
                event["concept:name"] = mapping[simplified_activity]
            else:
                event["concept:name"] = simplified_activity
    return event_log


def activities_timestamps_df(log, activity_col="activity", timestamp_col="timestamp"):
    """Return a DataFrame with one row per event: activity name and (UTC) timestamp."""
    rows = [
        {activity_col: event["concept:name"], timestamp_col: event["time:timestamp"]}
        for trace in log
        for event in trace
    ]
    df = pd.DataFrame(rows)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], utc=True)
    return df


def yearly_activity_table(log):
    """Activities (rows) x years (columns) table of event counts."""
    df = activities_timestamps_df(log)
    df["year"] = df["timestamp"].dt.year
    yearly_counts = df.groupby(["year", "activity"]).size().reset_index(name="count")
    return yearly_counts.pivot(index="activity", columns="year", values="count").fillna(0).astype(int)


def calculate_trend(row):
    """Compare the first and last year of a row: Upward, Downward or Stable."""
    first_year_count = row.iloc[0]
    last_year_count = row.iloc[-1]
    if last_year_count > first_year_count:
        return "Upward"
    elif last_year_count < first_year_count:
        return "Downward"
    return "Stable"
