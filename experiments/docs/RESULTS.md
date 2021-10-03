## Results

This document contains preliminary results.

### Baseline: PostgreSQL

All experiments run on PostgreSQL 12 instance.

**Configuration 1: Intel NUC**

TODO: Hardware Stats

- Function 01 : 150.497 seconds
- Function 04 : 0.038 seconds
- Function 05 : 0.035 seconds
- Function 06 : 1821.367 seconds
- Function 11 : 0.039 seconds
- Function 13 : 21547.449 seconds
- Function 20a : 22.664 seconds

**Configuration 2: AWS `c4.8xlarge`**

TODO: Hardware Stats

- Function 01 : 184.587 seconds
- Function 04 : 0.0461 seconds
- Function 05 : 0.042 seconds
- Function 06 : 2198.184 seconds
- Function 11 : 0.048 seconds
- Function 13 : 26946.723 seconds
- Function 20a : 27.736 seconds

**Configuration 2: `dev12`**

TODO: Hardware Stats

- Function 01 : 166.194 seconds
- Function 04 : 0.086 seconds
- Function 05 : 0.077 seconds
- Function 06 : 2043.965 seconds
- Function 11 : 0.075 seconds
- Function 13 : 24027.222 seconds
- Function 20a : 23.806 seconds

### NoisePage

Averaged over 5 runs. Run on `dev12`. SQL ProcBench schema SF1.

System: POSTGRES
- Function 01 : 0.15 seconds
- Function 04 : 0.10 seconds
- Function 05 : 10.5 seconds
- Function 11 : 0.10 seconds
- Function 20a : 0.10 seconds

System: NOISEPAGE
- Function 01 : 52.8 seconds
- Function 04 : 0.10 seconds
- Function 05 : 3500.1 seconds
- Function 11 : 0.15 seconds
- Function 20a : 0.23 seconds
