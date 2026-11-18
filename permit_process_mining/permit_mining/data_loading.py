"""Loading the XES event log and flattening logs into DataFrames."""
import copy

import pandas as pd
import pm4py


def log_to_dataframe(log):
    """Flatten an event log into a DataFrame (trace attributes + event attributes, one row per event)."""
    data = []
    for trace in log:
        trace_attributes = trace.attributes
        for event in trace:
            event_data = {"case_id": trace_attributes.get("concept:name", "N/A")}
            event_data.update({key: value for key, value in trace_attributes.items()})
            event_data.update({key: value for key, value in event.items()})
            data.append(event_data)
    return pd.DataFrame(data)


def load_log(path_log):
    """Load the XES log.

    Returns (log, log_copy): the EventLog and an untouched deep copy of it.
    """
    log_df = pm4py.read_xes(path_log)
    log = pm4py.convert_to_event_log(log_df)
    log_copy = copy.deepcopy(log)
    return log, log_copy


def inspect_first_trace(log):
    """Print the first trace, its first event and that event's activity name."""
    print(log[0])
    print(log[0][0])
    print(log[0][0]["concept:name"])
