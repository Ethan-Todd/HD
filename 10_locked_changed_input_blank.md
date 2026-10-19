# Locked Changed-Input Record — Blank AI-Off Template

Do **not** fill this prediction with AI open. The completed terminal-growth test remains separately preserved in `08_locked_changed_input_record.md`; this blank form is for any additional required test.

## Instructions

1. Close AI and choose one economically meaningful independent input.
2. Write the prediction below in your own words **before** running the model. Include old/new values, units, expected direction, rough magnitude, and expected recommendation effect.
3. Save this file.
4. In Terminal, from this rebuild folder, run:

   ```bash
   git add 10_locked_changed_input_blank.md
   git commit -m "Lock changed-input prediction"
   git show -s --format='%H%n%cI%n%s' HEAD
   ```

5. Copy the displayed commit hash and timestamp into the table. Do not amend or rewrite the prediction after seeing output.
6. Run base and changed cases with only the named independent input changed. Preserve both outputs and failed checks.
7. Complete the post-run table. If the model or command fails, record the failure and diagnosis.

## Pre-run record — complete AI-off

| Field | Human entry before execution |
|---|---|
| Model file/version or hash |  |
| Precommit timestamp |  |
| Repository commit |  |
| Material independent input |  |
| Old value and units |  |
| New value and units |  |
| Other independent inputs held fixed |  |
| Expected output direction |  |
| Expected rough magnitude |  |
| Expected recommendation effect |  |
| Human-authored prediction, exact wording |  |

## Post-run record — complete only after committed prediction

| Field | Actual result |
|---|---|
| Base output and units |  |
| Changed output and units |  |
| Signed dollar/unit change |  |
| Signed percentage change |  |
| Validation results |  |
| Actual recommendation effect |  |
| Comparison with original prediction |  |
| Failure diagnosis or no-change reason |  |
| Output/evidence path |  |

Do not invent or backdate any entry. A blank field remains incomplete evidence.
