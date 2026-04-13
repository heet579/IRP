# Future Plan of Action

## Objective
Convert the current notebook into a final, presentation-ready and report-ready cybersecurity research submission.

## Current Status (already completed)
1. Basic EDA completed (shape, samples, missing values, label checks).
2. Industry-style EDA completed (feature audit, outliers, correlation, drift/PSI, shortlist).
3. Baseline models completed (Logistic Regression, Random Forest, Isolation Forest).
4. Paper-style evaluation added (advanced metrics, threshold tuning, ablation, multiclass).

## Step-by-Step Next Actions

### Step 1: Re-run end-to-end and lock reproducibility
- Re-run all notebook cells from top to bottom once.
- Verify CSV outputs are regenerated correctly.
- Keep seed and environment details documented.

### Step 2: Final metric decision with professor
- Confirm primary metric (F1 vs PR-AUC vs recall at low FPR).
- Confirm whether binary-only or binary + multiclass is required.
- Confirm whether confidence intervals / significance tests are expected.

### Step 3: Add interpretation layer for report writing
- Add 1 short interpretation paragraph after each Phase 4 table.
- Highlight operational trade-offs (false alarms vs missed attacks).
- Clearly state best model and why it is preferred.

### Step 4: Add limitations and validity notes
- Mention dataset constraints (synthetic traffic, domain shift risk).
- Mention deployment assumptions and generalization risk.
- Add a brief "threats to validity" subsection in notebook/report.

### Step 5: Prepare final presentation narrative
- Build a 7-step speaking flow:
  1) Problem
  2) Data
  3) EDA insights
  4) Baseline models
  5) Paper-style evaluation
  6) Key findings
  7) Future work
- Keep one key result table and one key confusion matrix ready for explanation.

### Step 6: Optional advanced extension (if time permits)
- Add explainability (permutation importance or SHAP).
- Add runtime benchmarks (train time, inference latency).
- Add repeated-run confidence intervals.

## Deliverables Checklist
- [ ] Final notebook executed end-to-end
- [ ] Final CSV tables exported
- [ ] Professor decisions documented
- [ ] Report draft aligned with notebook outputs
- [ ] Slide summary aligned with 7-step speaking flow

## Proposed Timeline
- **Day 1:** Reproducibility run + professor metric decisions
- **Day 2:** Interpretation text + limitations section
- **Day 3:** Final report polish + presentation slides
