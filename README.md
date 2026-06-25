# Economic Structural Resilience in OECD Countries
### A POSet-Based Framework for Multi-Dimensional Economic Comparison

> **Authors:** Colombini Francesco (944941) · Haider Ali (948092)  
> **Course:** Data Science Lab — Università degli Studi di Milano-Bicocca  
> **Contact:** {f.colombini4, a.haider16}@campus.unimib.it

---

## Overview

This project investigates whether pre-shock economic structures are associated with stronger resilience outcomes across OECD countries during systemic crises. Rather than constructing a composite resilience index, we apply **Partial Order Theory (POSet)** to compare countries across five structural dimensions without forcing arbitrary weighting or linear rankings.

The framework is validated against two major shocks:
- **Global Financial Crisis** — structural baseline 2007, validation window 2008–2012
- **COVID-19 Pandemic** — structural baseline 2019, validation window 2020–2023

**Key finding:** OECD economies are largely structurally incomparable (incomparability ratio: 0.68 in 2007, 0.77 in 2019). Frontier countries nevertheless recover faster and outperform non-frontier countries on 5 out of 6 post-shock macroeconomic indicators in both periods.

---

## Methodology

### Ordering Variables (pre-shock structural capacity)

| Variable | Interpretation | Direction |
|---|---|---|
| Debt Capacity | Lower fiscal fragility | ↑ |
| Employment Strength | Lower labour-market stress | ↑ |
| R&D Intensity | Innovation capability | ↑ |
| Tertiary Human Capital | Adaptive skills base | ↑ |
| Energy Security | Lower external energy exposure | ↑ |

### Validation Variables (post-shock outcomes)

GDP recovery time · Average GDP growth · Average unemployment · Unemployment change · Absolute inflation · Public debt change · Productivity change

### POSet Construction

1. Direction-align all variables (higher = better)
2. Discretize into 5 ordinal levels via within-sample quantile binning
3. Apply strict Pareto dominance: country A dominates B iff A ≥ B on all dimensions and A > B on at least one
4. Compute transitive reduction → Hasse diagram
5. Epsilon-margin robustness check (ε ∈ [0.00, 0.20])

---

## Data Sources

| Dataset | Source | Role |
|---|---|---|
| R&D expenditure (% GDP) | OECD SDMX | Ordering |
| Tertiary education attainment | OECD SDMX | Ordering |
| Unemployment rate | OECD SDMX | Ordering / Validation |
| GDP growth | OECD SDMX | Validation |
| Inflation (CPI) | OECD SDMX | Validation |
| Labour productivity | OECD SDMX | Validation |
| Public debt (% GDP) | Eurostat (primary) / World Bank (fallback) | Ordering / Validation |
| Energy import dependency | World Bank | Ordering |
| Worldwide Governance Indicators | World Bank | Context only |

All data is retrieved programmatically via official APIs. No manual downloads required (see acquisition notebooks).

---

## Results Summary

| Metric | GFC 2007 | COVID-19 2019 |
|---|---|---|
| Countries included | 25 | 35 |
| Distinct structural profiles | 25 | 34 |
| Pareto-frontier countries | 8 (32%) | 13 (37%) |
| Incomparability ratio | 0.68 | 0.77 |
| GDP recovery frontier advantage | 0.82 years | 0.26 years |
| Macro indicators favouring frontier | 5/6 | 5/6 |

---

## Project Structure

```text
project/
│
├── data/
│   ├── raw/                  # Original API responses and bulk downloads
│   ├── processed/            # Harmonized country-year panel, direction-aligned variables
│   └── validation/           # Post-shock outcome datasets (kept separate from ordering data)
│
├── notebooks/
│   ├── preprocessing/        # Data acquisition, harmonization, missing-data handling
│   ├── poset_analysis/       # Ordinal profiling, dominance computation, Hasse diagrams
│   └── shock_validation/     # GDP recovery, multi-indicator frontier vs non-frontier comparison
│
├── results/
│   ├── matrices/             # Dominance and comparability matrices
│   ├── hasse_diagrams/       # Exported Hasse diagram figures (per shock baseline)
│   ├── plots/                # Robustness, validation and sensitivity figures
│   └── reports/              # Summary tables and final output CSVs
│
├── paper/
│   └── draft/                # LaTeX source and compiled PDF
│
└── README.md
```

---

## Reproducing the Analysis

### Requirements

```bash
pip install -r requirements.txt
```

Core dependencies: `pandas`, `numpy`, `networkx`, `matplotlib`, `seaborn`, `requests`, `pandasdmx`

### Execution Order

Run the notebooks in sequence:

```
1. notebooks/preprocessing/    → produces data/processed/
2. notebooks/poset_analysis/   → produces results/matrices/ and results/hasse_diagrams/
3. notebooks/shock_validation/ → produces results/plots/ and results/reports/
```

Each notebook produces intermediate diagnostic outputs and final report-ready tables. Stages are modular and can be re-run independently after the processed data is in place.

---

## Key Design Choices

**Why POSet instead of a composite index?**  
Composite indicators assume all dimensions are tradeable and reduce heterogeneous profiles to a single number. A country strong in R&D but weak in debt capacity would appear comparable to a country with the opposite profile — hiding a structural difference that is meaningful for resilience. POSet reports this as incomparability rather than forcing a false ranking.

**Why single-year snapshots (2007, 2019)?**  
The ordering variables are slow-moving structural indicators. A single pre-shock snapshot preserves temporal priority between the structural order and the validation outcomes, preventing outcome leakage.

**Why exclude WGI from the ordering set?**  
WGI is itself a composite built from multiple underlying sources. Including it would reintroduce hidden aggregation inside the POSet — contradicting the project's core methodological commitment to transparency. Governance is retained as contextual material.

---

## AI Tools Declaration

Generative AI tools (Claude by Anthropic and ChatGPT by OpenAI) were used exclusively for code refinement and debugging during implementation of the data acquisition, preprocessing and POSet construction pipeline. All research design decisions, methodological choices, analytical interpretations and written content were produced independently by the authors.

---

## References

- Martin, R. (2012). Regional Economic Resilience, Hysteresis and Recessionary Shocks.
- Martin, R., Sunley, P. (2015). On the Notion of Regional Economic Resilience.
- Bruggemann, R., Carlsen, L. An Improved Estimation of Partial Order Ranking.
- Davey, B.A., Priestley, H.A. *Introduction to Lattices and Order*. Cambridge University Press.
- OECD (2008). Handbook on Constructing Composite Indicators.
- Cherp & Jewell (2014). The Concept of Energy Security.
- [OECD Data Explorer](https://data-explorer.oecd.org/) · [Eurostat](https://ec.europa.eu/eurostat) · [World Bank](https://data.worldbank.org/)