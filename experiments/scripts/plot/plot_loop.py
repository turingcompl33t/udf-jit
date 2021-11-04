# plot_loop.py
# Plot results of "Lightweight Loop" benchmark.

import os
import sys
import json
import math
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


def read_json(path: str) -> Tuple[List[float], List[float]]:
    """
    Read a JSON file containing results of the benchmark.
    :param path The path to the JSON file
    :return A tuple of (iterations, runtime) where
        - iterations is the number of iterations
        - runtime is the function runtime
    """
    with open(path, "r") as f:
        data = json.load(f)
        iterations = [math.log(int(float(k)), 10) for k in data.keys()]
        runtime = [v[0] * 1000 for v in data.values()]
        return (iterations, runtime)


def make_plot(
    iterations: List[float], np_runtime: List[float], tpl_runtime: List[float]
):
    """
    Plot benchmark results.
    :param iterations The data for table sizes
    :param pg_runtime The data for Postgres results
    :param np_runtime The data for NoisePage results
    """

    fig, ax = plt.subplots()
    ax.plot(iterations, np_runtime, label="NoisePage", marker="^", zorder=3)
    ax.plot(iterations, tpl_runtime, label="TPL", marker="D", zorder=3)
    plt.xlabel("log(Number of Iterations)", fontsize=20)
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
    # fig_legend.savefig(os.path.join(OUTPUT_PATH, f"loop_legend.pdf"))
    # plt.close(fig_legend)

    plt.savefig(os.path.join(OUTPUT_PATH, f"loop.png"))
    plt.close(fig)


def main() -> int:
    np_iterations, np_runtime = read_json(
        os.path.join(RESULTS_PATH, "loop_interpreted.json")
    )
    tpl_iterations, tpl_runtime = read_json(
        os.path.join(RESULTS_PATH, "loop_compiled.json")
    )

    assert len(tpl_iterations) == len(np_iterations), "Corrupt results data"
    assert all(
        tpl_iterations[i] == np_iterations[i] for i in range(len(np_iterations))
    ), "Corrupt results data"

    make_plot(np_iterations, np_runtime, tpl_runtime)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
