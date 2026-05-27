# Economic Structural Resilience — POSet Framework

A research project focused on the construction of a **Partial Order (POSet)** framework for the structural comparison of OECD economies under multidimensional resilience criteria.

The project studies whether certain structural economic configurations are associated with stronger adaptive capacity during major systemic shocks such as:

* the 2008 financial crisis,
* the COVID-19 crisis,
* and the recent inflation/energy shock.

---

# Project Objective

Traditional resilience rankings usually:

* aggregate many indicators into a single score,
* impose arbitrary weights,
* and force countries into linear rankings.

This project follows a different approach.

Instead of creating a composite index, we model OECD economies as a **partially ordered system** using:

* Pareto dominance,
* ε-dominance robustness,
* and Partial Order Theory (POSet).

The final goal is to identify:

* structurally dominant economies,
* structurally vulnerable economies,
* and incomparable economic configurations characterized by different trade-offs.

---

# Core Research Question

> Which structural economic configurations are associated with stronger resilience during systemic crises?

---

# Methodological Framework

The project is divided into two main layers:

## 1. Structural Ordering Layer (POSet)

A subset of structural variables is used to construct the partial order between countries.

### Ordering Variables

| Variable                      | Interpretation                     | Direction        |
| ----------------------------- | ---------------------------------- | ---------------- |
| R&D expenditure (% GDP)       | Innovation and adaptive capability | Higher is better |
| Trust in institutions         | Institutional robustness           | Higher is better |
| Public debt (% GDP)           | Financial fragility                | Lower is better  |
| Energy import dependency      | External vulnerability             | Lower is better  |
| Tertiary education attainment | Human capital adaptability         | Higher is better |

These variables define the multidimensional structural space of the POSet.

---

## 2. Validation Layer (Shock Analysis)

A separate set of variables is used to evaluate how countries behaved during crises.

### Validation Variables

* GDP growth/contraction
* Inflation dynamics
* Unemployment variation
* Productivity variation
* Recovery speed
* Volatility measures

These variables are NOT used to build the order itself.

They are used only to test whether structurally dominant countries exhibit:

* lower shock sensitivity,
* faster recovery,
* and stronger systemic stability.

---

# Data Source

All data are collected from the OECD Data Explorer.

The full dataset is downloaded first, cleaned, normalized, and only afterwards divided into:

* ordering variables,
* validation variables.

---

# POSet Construction

Each country is represented as a normalized multidimensional vector:

$$x = (x_1, x_2, x_3, x_4, x_5)$$

The project uses **ε-dominance** instead of strict Pareto dominance to avoid artificial comparisons caused by statistical noise.

Country A dominates country B if:

$$x_i(A) \ge x_i(B) - \varepsilon_i \quad \forall i$$

and:

$$x_j(A) > x_j(B) + \varepsilon_j$$

for at least one variable (j).

Where:

$$\varepsilon_i = 0.1 \cdot \sigma_i$$

and (\sigma_i) is the standard deviation of variable (i).

---

# Expected Outputs

The project produces:

* Dominance matrix
* Comparability matrix
* Hasse diagram
* Pareto frontier
* Structural hierarchy of OECD economies
* Shock-resilience validation analysis

---

# Key Conceptual Contribution

The framework avoids:

* arbitrary weighting systems,
* forced linear rankings,
* excessive dimensional reduction.

Instead, it explicitly models:

* multidimensionality,
* incomparability,
* and structural trade-offs between economic systems.

---

# Repository Structure

```text
project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── validation/
│
├── notebooks/
│   ├── preprocessing/
│   ├── poset_analysis/
│   └── shock_validation/
│
├── src/
│   ├── preprocessing/
│   ├── dominance/
│   ├── poset/
│   └── validation/
│
├── results/
│   ├── matrices/
│   ├── hasse_diagrams/
│   ├── plots/
│   └── reports/
│
├── paper/
│   └── draft/
│
└── README.md
```

---

# Workflow

## Step 1 — Data Collection

* Download OECD country-year indicators

## Step 2 — Preprocessing

* Cleaning
* Missing value handling
* Direction alignment
* Robust normalization

## Step 3 — POSet Construction

* Build ε-dominance relations
* Generate dominance matrix
* Compute comparability structure
* Extract Hasse diagram

## Step 4 — Shock Validation

* Build pre-shock POSet
* Compare against post-shock outcomes

---

# Academic Relevance

The project integrates:

* economic resilience theory,
* complexity economics,
* Pareto dominance,
* and Partial Order Theory.

The final result is not a ranking system, but a:

> structural topology of economic resilience across OECD economies.
