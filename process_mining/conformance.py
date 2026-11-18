"""Section 2 - conformance checking (alignments and token-based replay)."""
import pandas as pd
import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.discovery.alpha import algorithm as alpha_miner  # noqa: F401 (alternative miner)
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner


def alignment_conformance(log):
    """Inductive Miner model + alignments; prints a summary of fitness and cost."""
    process_tree = inductive_miner.apply(log)
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

    aligned_traces = alignments.apply_log(log, net, initial_marking, final_marking)
    print(aligned_traces)
    print(f"Number of traces: {len(aligned_traces)}")
    print("Sample of aligned traces:", aligned_traces[:5])

    for alignment in aligned_traces:
        print(alignment.keys())

    total_fitness = 0
    perfect_traces = 0
    total_cost = 0
    num_traces = len(aligned_traces)

    for alignment in aligned_traces:
        total_fitness += alignment["fitness"]
        total_cost += alignment["cost"]
        if alignment["fitness"] == 1.0:
            perfect_traces += 1

    if num_traces > 0:
        avg_fitness = total_fitness / num_traces
        perfect_traces_percentage = (perfect_traces / num_traces) * 100
        avg_cost = total_cost / num_traces
    else:
        avg_fitness = 0
        perfect_traces_percentage = 0
        avg_cost = 0

    summary_df = pd.DataFrame(
        {
            "Total number of traces": [num_traces],
            "Average fitness": [avg_fitness],
            "Perfectly aligned traces": [perfect_traces],
            "Percentage of perfect traces": [perfect_traces_percentage],
            "Average alignment cost": [avg_cost],
        }
    )
    print("Alignment Summary:")
    print(summary_df)
    print("Total fitness:", total_fitness)
    print("Total cost:", total_cost)
    print("Number of traces:", num_traces)
    return aligned_traces, summary_df


def token_replay_conformance(log):
    """Heuristics Miner model + token-based replay; returns the average trace fitness."""
    net, initial_marking, final_marking = heuristics_miner.apply(log)

    replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)
    print(replayed_traces)

    trace_fitness_sum = 0
    for replayed_trace in replayed_traces:
        if not replayed_trace["trace_is_fit"]:
            print(f"{replayed_trace}\n")
        trace_fitness_sum += replayed_trace["trace_fitness"]

    avg_trace_fitness = trace_fitness_sum / len(replayed_traces)
    print("\nTOKEN BASE REPLAY -> %f" % avg_trace_fitness)
    return avg_trace_fitness
