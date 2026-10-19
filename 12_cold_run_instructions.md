# Fresh-Environment Setup and Cold-Run Checklist

No third-party Python packages are required.

## Repository and project path

- Repository: `https://github.com/Ethan-Todd/HD.git`
- Current working source: `/Users/ethantodd/Documents/Codex/2026-08-25/op/FIN 439/home_depot_project_1_rebuild`
- Project path after the clone command below: `HD` (the repository root)

## Reproduce from a fresh clone

```bash
git clone --branch main --single-branch https://github.com/Ethan-Todd/HD.git HD
cd HD
git rev-parse HEAD
python3 -m venv .venv
./.venv/bin/python --version
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python benchmark_validation.py
echo $?
./.venv/bin/python home_depot_fcff_model.py
echo $?
./.venv/bin/python part3_analysis.py
echo $?
git status --short
```

`requirements.txt` deliberately declares standard-library-only operation, so the requirements installation should add no project packages. The pip upgrade is environment setup, not a model dependency. Windows PowerShell uses `.venv\Scripts\python.exe` instead of `./.venv/bin/python`.

Expected exit status is zero for each script. `benchmark_validation.py` must show twelve PASS lines and `Overall: PASS`; the company model must show the historical, accounting, DCF and bridge checks as PASS; Part 3 must show all three cases and its automated checks as PASS. Part 3 refreshes `05_part3_visible_output.txt`; the benchmark refreshes `14_training_benchmark_output.txt`.

A refresh of the two tracked output files may make `git status --short` nonempty if formatting or environment metadata differs; explain and inspect any difference rather than hiding it.

## Required fresh-clone inventory

Before running, show that the clone contains at least:

- `README.md` and `requirements.txt`;
- `benchmark_validation.py`, `home_depot_fcff_model.py`, and `part3_analysis.py`;
- `edition_a_unchanged.md`;
- `00_architecture_audit.md` through `20_partner_challenge_status.md`, including the visible output and working validation records.

Verification on October 19, 2026 found that GitHub `main` was still at `dcc900b366f9e7d200e37d96cca31403cee2ecc4` and contained only the older course files. It did **not** contain the rebuild README, requirements file, or required scripts. Do not record the cold run or use that remote commit as submission evidence. First commit the complete rebuild, publish it at the repository root, clone it again, and confirm the inventory above.

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
- [ ] Keep visible: all twelve benchmark PASS lines; FY2025/base reconciliation; five-year balance and cash-tie checks; three operating cases; DCF bridge; sensitivity/reverse DCF; comparable references; recommendation and limitations.
- [ ] Confirm no credentials or private data are present.
- [ ] Record run date/time, commit hash, commands, exit codes, and video timestamp indices.
- [ ] Correct transcript terms and numbers after recording.

Do not check these boxes merely because the scripts ran in the development environment. The assignment requires a recorded cold run in a fresh environment.
