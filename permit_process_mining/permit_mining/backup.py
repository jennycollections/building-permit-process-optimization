"""Backup / alternative visualisations on the unfiltered log (need Graphviz `dot` on PATH)."""
import os

import pm4py


def add_graphviz_to_path(dot_dir):
    """Add the folder that contains Graphviz' `dot` executable to PATH (fixes 'dot not found')."""
    os.environ["PATH"] += os.pathsep + dot_dir


def inductive_bpmn(log):
    bpmn_model = pm4py.discover_bpmn_inductive(log)
    print(bpmn_model)
    pm4py.view_bpmn(bpmn_model)


def inductive_process_tree(log):
    tree = pm4py.algo.discovery.inductive.algorithm.apply_tree(log)
    print(tree)
    pm4py.view_process_tree(tree)


def inductive_petri_net(log):
    model = pm4py.algo.discovery.inductive.algorithm.apply(log)
    print(model)
    petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(model)
    pm4py.view_petri_net(petri_net, initial_marking, final_marking)


def dfg_view(log):
    dfg_relations = pm4py.algo.discovery.dfg.algorithm.apply(log)
    print(dfg_relations)
    dfg_digraph = pm4py.visualization.dfg.visualizer.apply(dfg_relations, log=log)
    print(dfg_digraph)
    pm4py.visualization.dfg.visualizer.view(dfg_digraph)
