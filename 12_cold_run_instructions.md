# Fresh-Environment Setup and Cold-Run Checklist

No third-party Python packages are required.

## Reproduce from a fresh clone

```bash
git clone YOUR_REPOSITORY_URL home_depot_project_1_rebuild
cd home_depot_project_1_rebuild
python3 -m venv .venv
./.venv/bin/python --version
./.venv/bin/python benchmark_validation.py
./.venv/bin/python home_depot_fcff_model.py
./.venv/bin/python part3_analysis.py
```

Windows PowerShell uses `.venv\Scripts\python.exe` instead of `./.venv/bin/python`.

Expected exit status is zero for each script. `benchmark_validation.py` must show twelve PASS lines and `Overall: PASS`; the company model must show the historical, accounting, DCF and bridge checks as PASS; Part 3 must show all three cases and its automated checks as PASS. Part 3 refreshes `05_part3_visible_output.txt`; the benchmark refreshes `14_training_benchmark_output.txt`.

## Cold-run recording checklist — not yet completed

- [ ] Start recording before opening the repository.
- [ ] Show the repository URL/commit and an actually fresh clone or clean environment.
- [ ] Show `python3 --version`; record operating system and architecture.
- [ ] Create the virtual environment without installing packages.
- [ ] Run the benchmark; show all twelve comparisons and exit status.
- [ ] Run the core company model; show FY2025 reconciliation, linked statements, bridge and checks.
- [ ] Run Part 3; show the three cases, sensitivity, reverse DCF, comps and checks.
- [ ] Show that `05_part3_visible_output.txt` and `14_training_benchmark_output.txt` were refreshed.
- [ ] Record the first failure exactly, if any, and the resolution or scoped limitation.
- [ ] Show one deliberate failure/boundary test and its unsuccessful status or invalid result.
- [ ] Confirm no credentials or private data are present.
- [ ] Record run date/time, commit hash, commands, exit codes, and video timestamp indices.
- [ ] Correct transcript terms and numbers after recording.

Do not check these boxes merely because the scripts ran in the development environment. The assignment requires a recorded cold run in a fresh environment.
