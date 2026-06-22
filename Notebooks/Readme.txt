# Notebook Pipeline Overview

This folder contains the full notebook pipeline for the project:

**Economic Resilience in OECD Countries: A Multidimensional Structural Framework**

The notebooks should be run in numerical order, from `00` to `13`. Each notebook handles one stage of the workflow, from raw data acquisition to final visuals.

Important project rule: the analysis does **not** create a final scalar Economic Resilience Index. The goal is to study structural resilience through a multidimensional POSet/Pareto-style framework.

---

## Notebook Descriptions

### `00_Data_Acquisition_Fixed.ipynb`

Acquires the raw datasets used in the project.

This notebook downloads or prepares the main raw input files, including OECD macroeconomic indicators, productivity data, GDP growth, public debt, energy dependency, and the WGI governance package. It also creates acquisition logs and records failed downloads, if any.

Main role:

* collect raw project data;
* save raw files into the project folder;
* create acquisition logs;
* check whether any files failed to download.

---

### `01_Make_Raw_Files_Comparable.ipynb`

Standardizes raw files into a comparable country-year-variable format.

This notebook converts differently structured raw files into a consistent long-format structure. It standardizes country codes, country names, years, variable names, and values. It also removes aggregate regions and checks for suspicious or unmapped country codes.

Main role:

* standardize raw datasets;
* create comparable country-year-variable data;
* remove non-country aggregates;
* run country-code diagnostics;
* prepare data for coverage analysis.

---

### `02_Raw_Files_Coverage_Diagnostics.ipynb`

Checks whether the standardized raw data is usable.

This notebook evaluates data availability by country, year, and variable. It identifies which countries have strong coverage, which countries need review, and which variables may cause coverage problems.

Main role:

* assess country coverage;
* assess variable coverage;
* assess country-year completeness;
* create keep/drop/review recommendations;
* identify weak data areas before analysis.

---

### `03_GDP_Recovery_Dynamic_Baseline.ipynb`

Constructs the GDP recovery outcome variable.

This notebook calculates how long each country took to recover after the 2007 financial crisis and the 2019/COVID shock. It uses a dynamic baseline, meaning the baseline depends on when each country first experienced negative growth in the shock window.

Main role:

* build `Recovery_2007`;
* build `Recovery_2019`;
* handle countries with no negative-growth shock;
* handle countries not recovered by available data;
* create recovery audit and problem-case files.

Important note:

Recovery is used only for validation. It is not used as a POSet ordering variable.

---

### `04_WGI_Governance_Compilation_v4.ipynb`

Compiles World Governance Indicators into project-ready governance variables.

This notebook extracts the official WGI score dimensions and creates a derived governance-capacity composite. It also checks WGI coverage and correlations between governance dimensions.

Main role:

* process WGI source files;
* extract six official WGI dimensions;
* create a derived governance-capacity score;
* check governance data coverage;
* check redundancy among WGI dimensions.

Important note:

The six WGI dimensions are official WGI variables. The governance composite used in the project is derived by us and should not be described as an official WGI indicator.

---

### `05_Volatility_Features.ipynb`

Creates pre-shock volatility and stability features.

This notebook calculates stability variables using only pre-shock windows. For example, the 2007 analysis uses pre-2007 data, while the 2019 analysis uses pre-2019 data.

Main role:

* calculate GDP growth stability;
* calculate additional volatility/stability diagnostics;
* ensure no post-shock leakage;
* create shock-specific stability features.

Important note:

GDP growth stability is treated as a sensitivity variable, not part of the main baseline POSet.

---

### `06_Master_Dataset_Build_v3.ipynb`

Builds the master analytical dataset.

This notebook merges standardized structural variables, governance data, recovery outcomes, and shock-specific volatility features. It creates both a country-year panel and a country-shock analysis snapshot.

Main role:

* merge structural variables;
* merge WGI governance data;
* merge recovery outcomes;
* attach shock-specific features correctly;
* create master datasets for POSet preparation.

Important note:

Shock-specific variables are attached only to their matching shock. Pre-2007 variables are used for the 2007 analysis, and pre-2019 variables are used for the 2019 analysis.

---

### `07_Pre_POSet_EDA_Checks_v2.ipynb`

Prepares variables for POSet analysis.

This notebook direction-aligns all candidate ordering variables so that higher values always mean better structural resilience. It also checks missingness, redundancy, and candidate variable sets.

Main role:

* convert variables to higher-is-better scores;
* check missingness;
* check correlations and redundancy;
* define the baseline variable set;
* create complete-case samples;
* prepare POSet-ready inputs.

Current baseline variables:

* debt capacity;
* employment strength;
* R&D intensity;
* tertiary human capital;
* energy security;
* governance capacity.

---

### `08_Profile_POSet_Main_v2.ipynb`

Runs the main profile-level POSet analysis.

This notebook discretizes structural variables into ordinal profiles and builds the partial order. It identifies Pareto/nondominated profiles, POSet layers, dominance relations, incomparability, and Hasse diagram edges.

Main role:

* create structural profiles;
* build dominance relations;
* identify Pareto profiles and countries;
* calculate POSet layers;
* create profile-country maps;
* create Hasse-ready outputs.

Important note:

POSet layers are not scalar rankings. They describe dominance structure within a partial order.

---

### `09_Epsilon_Sensitivity_Country_Level.ipynb`

Runs country-level epsilon tolerance sensitivity.

This notebook uses continuous scaled variables and tests how dominance relations change when small disadvantages are allowed within an epsilon tolerance.

Main role:

* run epsilon tolerance checks;
* track changes in dominance relations;
* track Pareto/frontier stability;
* detect cycles or invalid partial orders;
* test sensitivity of country-level dominance.

Important note:

This is a diagnostic stress test. Epsilon tolerance can increase comparability because it allows small disadvantages.

---

### `10_Epsilon_Margin_POSet_Robustness.ipynb`

Runs epsilon-margin robustness checks.

This notebook uses a stricter epsilon rule. A country cannot be worse in any dimension and must be better by more than epsilon in at least one dimension.

Main role:

* run epsilon-margin robustness;
* preserve the no-worse-in-any-dimension POSet logic;
* compare epsilon-margin results with epsilon tolerance;
* test frontier stability under stricter dominance.

Important note:

Epsilon-margin is the safer robustness method to report. Epsilon tolerance should be treated as diagnostic.

---

### `11_Recovery_Validation.ipynb`

Validates the structural POSet results against recovery outcomes.

This notebook checks whether structurally stronger countries or frontier/Pareto countries tend to recover faster. It compares recovery across Pareto vs non-Pareto countries, POSet layers, epsilon frontiers, and epsilon-margin frontiers.

Main role:

* compare structural strength with recovery time;
* validate Pareto/frontier countries;
* compare recovery across POSet layers;
* test multiple recovery variants;
* identify mismatch cases.

Important note:

This validation is descriptive and associational. It does not prove causality.

---

### `12_Sensitivity_Analysis.ipynb`

Consolidates all sensitivity checks.

This notebook summarizes sensitivity across variable selection, profile discretization, epsilon tolerance, epsilon-margin robustness, and recovery validation. It creates report-ready sensitivity tables and decision-support outputs.

Main role:

* summarize variable-set sensitivity;
* summarize 3/4/5-level profile sensitivity;
* summarize epsilon tolerance;
* summarize epsilon-margin robustness;
* summarize recovery validation;
* prepare final methodological decision tables.

---

### `13_Final_Visuals.ipynb`

Generates final figures and report-ready tables.

This notebook creates the final visual outputs for the report and presentation. It uses the selected visual configuration, currently a 4-level profile POSet, and exports figures, tables, and inventories.

Main role:

* create project pipeline diagram;
* create structural variable concept map;
* create Hasse diagrams;
* create profile sensitivity figures;
* create epsilon-margin robustness figures;
* create recovery validation visuals;
* export final figure and table inventories.

Current visual configuration:

* main set: `baseline_6_variables`;
* final profile level: `4`;
* epsilon-margin reference: `0.05`.

---

## Recommended Run Order

Run the notebooks in this order:

```text
00_Data_Acquisition_Fixed.ipynb
01_Make_Raw_Files_Comparable.ipynb
02_Raw_Files_Coverage_Diagnostics.ipynb
03_GDP_Recovery_Dynamic_Baseline.ipynb
04_WGI_Governance_Compilation_v4.ipynb
05_Volatility_Features.ipynb
06_Master_Dataset_Build_v3.ipynb
07_Pre_POSet_EDA_Checks_v2.ipynb
08_Profile_POSet_Main_v2.ipynb
09_Epsilon_Sensitivity_Country_Level.ipynb
10_Epsilon_Margin_POSet_Robustness.ipynb
11_Recovery_Validation.ipynb
12_Sensitivity_Analysis.ipynb
13_Final_Visuals.ipynb
```

---

## Methodological Guardrails

* Do not create a final scalar Economic Resilience Index.
* Do not treat POSet layers as a universal country ranking.
* Do not use recovery as an ordering variable.
* Use recovery only for validation after the POSet is constructed.
* Keep all ordering variables direction-aligned so higher means better.
* Treat epsilon-margin as the main robustness check.
* Treat epsilon tolerance as a diagnostic stress test.
* Explain incomparability as a feature of the method, not a failure.
