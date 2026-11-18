"""Section 1.1 - basic log statistics and plots."""
import matplotlib.pyplot as plt
import pandas as pd
import pm4py

from .utils import activities_timestamps_df


def print_log_statistics(log):
    """Print event attributes, activity counts, number of activities and number of cases.

    Returns the dictionary of activity counts.
    """
    event_attributes = pm4py.get_event_attributes(log)
    print("Event attributes: ")
    print(event_attributes)

    event_attribute_values = pm4py.get_event_attribute_values(log, attribute="concept:name")
    print("Event attribute values: ")
    print(event_attribute_values)

    print("Number of events: " + str(len(event_attribute_values)))
    print("Number of traces: " + str(len(log)))
    return event_attribute_values


def plot_event_occurrence(event_attribute_values, top_n=50):
    """Horizontal bar chart of activity occurrences."""
    event_attribute_values = dict(sorted(event_attribute_values.items(), key=lambda item: item[1]))
    keys = list(event_attribute_values.keys())
    values = list(event_attribute_values.values())

    sorted_keys_values = sorted(zip(values, keys))
    sorted_values, sorted_keys = zip(*sorted_keys_values)

    top_keys = sorted_keys[:top_n]
    top_values = sorted_values[:top_n]

    plt.figure(figsize=(12, 16))
    plt.barh(top_keys, top_values, color="steelblue")
    plt.xlabel("Occurrences", fontsize=14)
    plt.ylabel("Activities", fontsize=14)
    plt.yticks(fontsize=10)
    plt.show()


def plot_events_over_time(log):
    """Print the covered timeframe and plot the cumulative number of events."""
    timestamps = []
    for trace in range(0, len(log)):
        for event in range(0, len(log[trace])):
            timestamps.append(log[trace][event]["time:timestamp"])

    print("First timestamp is: " + str(min(timestamps)))
    print("Last timestamp is: " + str(max(timestamps)))

    timestamps = pd.DataFrame(timestamps, columns=["timestamps"])
    timestamps["count"] = 1
    timestamps.timestamps = pd.to_datetime(timestamps.timestamps, utc=True)
    timestamps.set_index("timestamps", inplace=True)
    timestamps.sort_index(inplace=True)

    timestamps.cumsum().plot()
    plt.show()


def plot_cumulative_activity_usage(log, legend_below=True):
    """Cumulative (daily) usage of every activity over time."""
    df_activities = activities_timestamps_df(log)
    df_activities.set_index("timestamp", inplace=True)
    activity_counts = (
        df_activities.groupby([pd.Grouper(freq="D"), "activity"]).size().reset_index(name="count")
    )
    pivot_table = activity_counts.pivot(index="timestamp", columns="activity", values="count").fillna(0)

    pivot_table.cumsum().plot(figsize=(12, 6), title="Cumulative Activity Usage Over Time")
    if legend_below:
        plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=5, fontsize=10)
    plt.show()
