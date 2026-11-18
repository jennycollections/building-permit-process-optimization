# Building Permit Process Optimization (Process Mining, Municipality 1)

Process mining analysis of the BPIC15_1 building permit event log with [PM4Py](https://pm4py.fit.fraunhofer.de/).
Converted from the original Jupyter notebook into a small Python package.

## Setup

```bash
pip install -r requirements.txt
# Graphviz binaries are required for the visualisations (https://graphviz.org/download/)
```

Download the BPIC15_1 event log (`BPIC15_1.xes`) from the 4TU repository and place it in `data/`
(or pass its location with `--log` / the `PERMIT_LOG_PATH` environment variable).

## Run

```bash
python main.py --log data/BPIC15_1.xes                  # everything
python main.py --sections 1 3                            # discovery + resources only
python main.py --dot-dir /path/to/graphviz/bin           # if `dot` is not on PATH
```

Sections: `1` discovery, `2` conformance checking, `3` resources, `4` backup visualisations.
CSV exports are written to `output/`.

## Structure

| File | Content |
|---|---|
| `main.py` | Entry point, runs the analysis section by section |
| `permit_mining/config.py` | Paths, thresholds, activity mappings and groupings |
| `permit_mining/data_loading.py` | XES import, log-to-DataFrame conversion |
| `permit_mining/utils.py` | Activity renaming, DFG helper, yearly tables, trend calculation |
| `permit_mining/log_statistics.py` | 1.1 Log statistics and plots |
| `permit_mining/filtering.py` | 1.2 Variant, frequency, main-process and time-window filters |
| `permit_mining/discovery.py` | Petri nets, DFGs, BPMN models, yearly activity usage |
| `permit_mining/conformance.py` | 2. Alignments and token-based replay |
| `permit_mining/resources.py` | 3. Workload and resource/activity analysis |
| `permit_mining/backup.py` | Alternative visualisations of the unfiltered log |
