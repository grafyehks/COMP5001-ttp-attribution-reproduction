# Reproduction of "High Stakes, Low Certainty" (USENIX Security 2025)

Code and results for a course reproduction report (COMP5001).
The original paper, data and code are by van der Horst et al. (2025)
and are NOT included here. Download them from Zenodo:
https://doi.org/10.5281/zenodo.14732550

## Contents
- code/improvements.ipynb  checks and analyses (Sections 5-6 of the report), with outputs
- code/report_figures.py   draws Figures 1-3 of the report
- results/improvements/    all output tables (CSV), figures and REPRODUCE.md

## How to run
1. Download the authors' artifact from Zenodo and unzip it.
2. Copy code/improvements.ipynb and code/report_figures.py into its code/ folder.
3. Follow results/improvements/REPRODUCE.md (Python 3.11-3.13, Poetry).
4. Run improvements.ipynb (Run All), then: poetry run python report_figures.py

## AI use
Code was written with help from Claude (Anthropic); see the report's AI statement.
