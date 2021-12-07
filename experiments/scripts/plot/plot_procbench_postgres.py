# plot_procbench_postgres.py
# Plot benchmark results from SQL ProcBench queries.

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Results from PostgreSQL
RESULTS_POSTGRES = {"01": 0.15, "04": 0.10, "05": 10.5, "11": 0.10, "20a": 0.10}

# Results from NoisePage
RESULTS_NOISEPAGE = {"01": 52.8, "04": 0.10, "05": 3500.1, "11": 0.15, "20a": 0.23}

# The path to which results are saved
OUTPUT_PATH = os.path.join(os.getcwd(), "./plots")


def make_plot():
    pg_values = [math.log(v * 1000) for v in RESULTS_POSTGRES.values()]
    np_values = [math.log(v * 1000) for v in RESULTS_NOISEPAGE.values()]
    assert len(pg_values) == len(np_values), "Corrupt data"

    # The number of functions on X-axis
    N = len(pg_values)

    fig, ax = plt.subplots()
    ax.bar(np.arange(N), pg_values, width=0.4, label="PostgreSQL")
    ax.bar(np.arange(N) + 0.4, np_values, width=0.4, label="NoisePage")
    plt.xlabel("Function Identifier", fontsize=20)
    plt.ylabel("log(Query Runtime) (ms)", fontsize=20)
    plt.xticks(np.arange(N) + 0.4 / 2, RESULTS_POSTGRES.keys())
    fig.tight_layout()

    # Embedded legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="best", ncol=len(handles), frameon=True)

    # Standalone legend
    # handles, labels = ax.get_legend_handles_labels()
    # fig_legend = plt.figure(figsize=(10, 0.5))
    # fig_legend.tight_layout()
    # plt.figlegend(handles, labels, loc="center", ncol=len(handles), frameon=True)
    # fig_legend.savefig(os.path.join(OUTPUT_PATH, "procbench_legend.pdf"))
    # plt.close(fig_legend)

    plt.savefig(os.path.join(OUTPUT_PATH, "procbench.pdf"))
    plt.close(fig)


def main() -> int:
    make_plot()
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
