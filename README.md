# 🏛️ Economic Structural Resilience in OECD Countries: A POSet-Based Framework

[![Language](https://img.shields.io/badge/Language-Jupyter%20Notebooks-orange?style=flat&logo=jupyter)](https://jupyter.org/)
[![Methodology](https://img.shields.io/badge/Methodology-Partial%20Order%20Theory%20(POSet)-blue)](#)
[![Validation](https://img.shields.io/badge/Validation-2008%20GFC%20%7C%20COVID--19-red)](#)
[![Report](https://img.shields.io/badge/Report-Complete%20Research%20Paper-red?logo=adobeacrobatreader)](Economic%20Structural%20Resilience%20in%20OECD%20Countries%20-%20Colombini,%20Haider.pdf)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> Evaluating macroeconomic shock resilience across OECD nations without arbitrary composite index weighting, using pure non-parametric discrete mathematics (POSet & Hasse Diagrams).

---

## 📌 Executive Summary

Conventional resilience scorecards suffer from a critical methodological flaw: they force diverse macroeconomic dimensions into a single linear ranking using arbitrary subjective weights. A nation with crushing fiscal debt can masquerade as "resilient" merely through high tertiary education scores.

This project introduces a **Partial Order Theory (POSet)** framework to compare national economic resilience across five structural dimensions:
- Eliminates subjective weighting and compensatory score aggregation.
- Models economic structure as a non-parametric mathematical poset (Hasse diagrams).
- Empirically validates pre-shock structural capacity across two global crises: the **2008 Global Financial Crisis** (baseline 2007) and the **COVID-19 Pandemic** (baseline 2019).

**Key Empirical Finding:** OECD economies are largely structurally incomparable (incomparability ratio of **0.68 in 2007** and **0.77 in 2019**). However, **frontier countries consistently outperform non-frontier countries on 5 out of 6 post-shock macroeconomic indicators** in both recovery windows.

---

## 🔍 Ordering Variables & Structural Dimensions

Pre-shock structural capacity is evaluated across five directional vectors:

| Variable | Structural Dimension | Optimization Direction |
|---|---|:---:|
| **Debt Capacity** | Lower fiscal fragility and sovereign default risk | ↑ |
| **Employment Strength** | Structural labor market absorption and resilience | ↑ |
| **R&D Intensity** | High-tech innovation and productivity ceiling | ↑ |
| **Tertiary Education** | Human capital sophistication and adaptive capacity | ↑ |
| **Gross Fixed Capital** | Long-term physical infrastructure investment | ↑ |

---

## 🛠️ Multi-Stage Analytical Architecture

The repository contains a fully reproducible 20-stage Jupyter analytics pipeline:

```
Economic_Structural_Resilience_in_OECD_Countries/
├── 00_Data_Acquisition.ipynb                   # Multi-source OECD microdata extraction
├── 01_Make_Raw_Files_Comparable.ipynb          # Harmonization of disparate OECD definitions
├── 02_Raw_Files_Coverage_Diagnostics.ipynb     # Missingness and country coverage audits
├── 03_GDP_Recovery_Dynamic_Baseline.ipynb      # Dynamic GDP recovery window indexing
├── 04_WGI_Governance_Compilation.ipynb         # World Bank governance indicators integration
├── 05_Volatility_Features.ipynb                # Historical macroeconomic shock metrics
├── 06_Master_Dataset_Build.ipynb               # Unified relational matrix construction
├── 07_Pre_POSet_EDA_Checks.ipynb               # Outlier and correlation diagnostics
├── 08_Profile_POSet_Main.ipynb                 # Core POSet ordering & Hasse diagram generation
├── 09-12_Sensitivity_and_Robustness.ipynb      # Epsilon-margin perturbation & stability testing
├── 13-18_Validation_and_Diagnostics.ipynb      # Multi-indicator post-shock recovery validation
└── 19_Profile_Similarity_Distance.ipynb        # High-dimensional profile distance matrices
```

---

**Authors:** Francesco Colombini & Ali Haider  
[GitHub Profile](https://github.com/FRA-0023) · [LinkedIn](https://www.linkedin.com/in/francescocolombini/)