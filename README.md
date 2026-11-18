# Building Permit Process Optimization (Process Mining, Municipality 1)

Process mining analysis of the BPI Challenge 2015 building permit event log (Municipality 1)
with [PM4Py](https://pm4py.fit.fraunhofer.de/). Converted from the original Jupyter notebook
into a small Python package.

## 1. Get the data

The code needs one input file: the event log **`BPIC15_1.xes`** (Municipality 1: 1,199 cases, 52,217 events).

- Download page (4TU.ResearchData): https://data.4tu.nl/articles/dataset/BPI_Challenge_2015_Municipality_1/12709154
- DOI: `10.4121/uuid:a0addfda-2044-4541-a450-fdcc9fe16d17`

Download the `.xes` file from that page and save it as `data/BPIC15_1.xes`
(the file is not included in this repository because of its size).

## 2. Install

```bash
pip install -r requirements.txt
```

### Graphviz (needed for the graphs)

PM4Py does not draw process models itself. It builds them and hands them to
[Graphviz](https://graphviz.org/download/), a separate free program, which renders the
Petri nets, directly-follows graphs (DFGs) and BPMN diagrams. This is different from Disco,
which is a standalone application with its own built-in drawing, so with Disco you never
had to install anything extra.

1. Install Graphviz itself (the `pip install graphviz` in `requirements.txt` is only a Python wrapper and is not enough):
   - macOS: `brew install graphviz`
   - Windows: installer from https://graphviz.org/download/ (tick "add to PATH")
   - Linux: `sudo apt install graphviz`
2. Check it works: `dot -V` should print a version number.
3. Only if that command is "not found": pass the folder that contains the `dot` program, e.g.
   `python main.py --dot-dir "/opt/homebrew/bin"` (macOS) or `--dot-dir "C:\Program Files\Graphviz\bin"` (Windows).
   Give the folder, not the path of `dot` itself.

## 3. Run

```bash
python main.py --log data/BPIC15_1.xes                  # everything
python main.py --sections 1 3                            # discovery + resources only
```

Sections: `1` discovery, `2` conformance checking, `3` resources, `4` backup visualisations.
The log path can also be set with the `PERMIT_LOG_PATH` environment variable.
CSV results are written to `output/` (created automatically, not tracked by git).

## Structure

| File | Content |
|---|---|
| `main.py` | Entry point, runs the analysis section by section |
| `precess_mining/config.py` | Paths, thresholds, activity mappings and groupings |
| `precess_mining/data_loading.py` | XES import, log-to-DataFrame conversion |
| `precess_mining/utils.py` | Activity renaming, DFG helper, yearly tables, trend calculation |
| `precess_mining/log_statistics.py` | 1.1 Log statistics and plots |
| `precess_mining/filtering.py` | 1.2 Variant, frequency, main-process and time-window filters |
| `precess_mining/discovery.py` | Petri nets, DFGs, BPMN models, yearly activity usage |
| `precess_mining/conformance.py` | 2. Alignments and token-based replay |
| `precess_mining/resources.py` | 3. Workload and resource/activity analysis |
| `precess_mining/backup.py` | Alternative visualisations of the unfiltered log |

## Output files

Written to `output/` by section 3:

- `average_processing_time_case_activity_resource.csv`
- `resource_activity_table.csv`
