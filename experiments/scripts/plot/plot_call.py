# plot_call.py
# Plot results of "Overhead of Function Call" benchmark.

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple, List

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The path to the results directory
RESULTS_PATH = "./tmp"

# The path to which results are saved
OUTPUT_PATH = os.path.join(os.getcwd(), "./plots")

# The number of rows in `integers`
TABLE_SIZE = 1000


def read_json(path: str) -> Tuple[List[int], List[float], List[float], List[float]]:
    """
    Read a JSON file containing results of the benchmark.
    :param path The path to the JSON file
    :return A tuple of (sizes, baseline, inlined, function) where
        - sizes is the size of the table
        - baseline is the baseline results
        - inlined is the inlined results
        - function is the function call results
    """
    with open(path, "r") as f:
        data = json.load(f)
        sizes = [int((int(k) / 100.0) * TABLE_SIZE) for k in data.keys()]
        baseline = [v[0] * 1000 for v in data.values()]
        inlined = [v[1] * 1000 for v in data.values()]
        function = [v[2] * 1000 for v in data.values()]
        return (sizes, baseline, inlined, function)


def make_plot(
    sizes: List[int],
    baseline: List[float],
    inlined: List[float],
    function: List[float],
    prefix: str,
):
    """
    Plot benchmark results.
    :param sizes The data for table sizes
    :param baseline The data for baseline results
    :param inlined The data for inlined results
    :param function The data for function call results
    :prefix The prefix for figure saving
    """

    fig, ax = plt.subplots()
    ax.plot(sizes, baseline, label="Baseline", marker="D", zorder=3)
    ax.plot(sizes, inlined, label="Inlined", marker="^", zorder=3)
    ax.plot(sizes, function, label="Function", marker="o")
    plt.xlabel("Table Size (Number of Rows)", fontsize=20)
    plt.ylabel("Average Query Runtime (ms)", fontsize=20)
    fig.tight_layout()

    # Embedded legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="best", ncol=len(handles), frameon=True)

    # Standalone legend
    # handles, labels = ax.get_legend_handles_labels()
    # fig_legend = plt.figure(figsize=(10, 0.5))
    # fig_legend.tight_layout()
    # plt.figlegend(handles, labels, loc="center", ncol=len(handles), frameon=True)
    # fig_legend.savefig(os.path.join(OUTPUT_PATH, f"{prefix}_call_legend.pdf"))
    # plt.close(fig_legend)

    plt.savefig(os.path.join(OUTPUT_PATH, f"{prefix}_call.png"))
    plt.close(fig)


def main() -> int:
    np_sizes, np_baseline, np_inlined, np_function = read_json(
        os.path.join(RESULTS_PATH, "call_interpreted.json")
    )

    tpl_sizes, tpl_baseline, tpl_inlined, tpl_function = read_json(
        os.path.join(RESULTS_PATH, "call_compiled.json")
    )

    make_plot(np_sizes, np_baseline, np_inlined, np_function, "np")
    make_plot(tpl_sizes, tpl_baseline, tpl_inlined, tpl_function, "tpl")

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
