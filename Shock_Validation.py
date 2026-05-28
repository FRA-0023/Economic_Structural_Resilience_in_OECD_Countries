# ============================================================
# POSET SHOCK VALIDATION FRAMEWORK
# ============================================================
# PURPOSE
# Validate whether countries occupying higher POSet levels
# exhibit stronger resilience during systemic shocks.
#
# ASSUMPTION:
# The POSet construction has already been completed.
#
# INPUT FILES:
#   1. poset_results.csv
#   2. shock_validation_data.csv
#
# REQUIRED POSET COLUMNS:
#   Country
#   Poset_Level
#
# REQUIRED SHOCK COLUMNS:
#   Country
#   Year
#   GDP_Growth
#   Inflation
#   Unemployment
#   Productivity
#
# OUTPUT:
#   - country_resilience_scores.csv
#   - level_validation_results.csv
#   - statistical_validation.csv
# ============================================================

import pandas as pd
import numpy as np

from scipy.stats import (
    spearmanr,
    kruskal
)

from sklearn.preprocessing import RobustScaler

# ============================================================
# CONFIGURATION
# ============================================================

PRE_SHOCK_YEAR = 2019
SHOCK_START = 2020
SHOCK_END = 2022

MISSING_THRESHOLD = 0.30

# ============================================================
# LOAD DATA
# ============================================================

poset_df = pd.read_csv("poset_results.csv")
shock_df = pd.read_csv("shock_validation_data.csv")

# ============================================================
# REMOVE HIGH-MISSING COUNTRIES
# ============================================================

def remove_high_missing_countries(df, threshold):

    missing_ratio = (
        df.groupby("Country")
        .apply(lambda x: x.isna().mean().mean())
    )

    valid_countries = (
        missing_ratio[
            missing_ratio <= threshold
        ].index
    )

    return df[df["Country"].isin(valid_countries)]

shock_df = remove_high_missing_countries(
    shock_df,
    MISSING_THRESHOLD
)

# ============================================================
# COUNTRY-WISE INTERPOLATION
# ============================================================

validation_columns = [
    "GDP_Growth",
    "Inflation",
    "Unemployment",
    "Productivity"
]

shock_df = shock_df.sort_values(
    ["Country", "Year"]
)

for col in validation_columns:

    # Rolling interpolation
    shock_df[col] = (
        shock_df.groupby("Country")[col]
        .transform(
            lambda x: x.interpolate(
                method="linear",
                limit_direction="both"
            )
        )
    )

    # Remaining missing values -> country mean
    shock_df[col] = (
        shock_df.groupby("Country")[col]
        .transform(
            lambda x: x.fillna(x.mean())
        )
    )

# ============================================================
# SHOCK RESILIENCE METRICS
# ============================================================

def compute_shock_resilience(df):

    results = []

    countries = df["Country"].unique()

    for country in countries:

        cdf = df[df["Country"] == country]

        pre_shock = cdf[
            cdf["Year"] < SHOCK_START
        ]

        shock_period = cdf[
            (cdf["Year"] >= SHOCK_START)
            &
            (cdf["Year"] <= SHOCK_END)
        ]

        if len(pre_shock) == 0:
            continue

        if len(shock_period) == 0:
            continue

        # ----------------------------------------------------
        # GDP RESILIENCE
        # Higher = better
        # ----------------------------------------------------

        baseline_gdp = pre_shock[
            "GDP_Growth"
        ].mean()

        worst_gdp = shock_period[
            "GDP_Growth"
        ].min()

        gdp_resilience = (
            worst_gdp - baseline_gdp
        )

        # ----------------------------------------------------
        # UNEMPLOYMENT RESILIENCE
        # Lower unemployment increase = better
        # Variables already directionally harmonized
        # ----------------------------------------------------

        baseline_unemp = pre_shock[
            "Unemployment"
        ].mean()

        worst_unemp = shock_period[
            "Unemployment"
        ].max()

        unemployment_resilience = (
            baseline_unemp - worst_unemp
        )

        # ----------------------------------------------------
        # PRODUCTIVITY RESILIENCE
        # ----------------------------------------------------

        baseline_prod = pre_shock[
            "Productivity"
        ].mean()

        worst_prod = shock_period[
            "Productivity"
        ].min()

        productivity_resilience = (
            worst_prod - baseline_prod
        )

        # ----------------------------------------------------
        # INFLATION STABILITY
        # Lower volatility = better
        # ----------------------------------------------------

        inflation_stability = -(
            shock_period["Inflation"].std()
        )

        # ----------------------------------------------------
        # RECOVERY SPEED
        # Faster recovery = better
        # ----------------------------------------------------

        recovery_year = None

        for _, row in shock_period.iterrows():

            if row["GDP_Growth"] >= baseline_gdp:
                recovery_year = row["Year"]
                break

        if recovery_year is None:
            recovery_score = -(
                SHOCK_END - SHOCK_START + 1
            )
        else:
            recovery_score = -(
                recovery_year - SHOCK_START
            )

        # ----------------------------------------------------
        # STORE
        # ----------------------------------------------------

        results.append({

            "Country": country,

            "GDP_Resilience":
                gdp_resilience,

            "Unemployment_Resilience":
                unemployment_resilience,

            "Productivity_Resilience":
                productivity_resilience,

            "Inflation_Stability":
                inflation_stability,

            "Recovery_Speed":
                recovery_score
        })

    return pd.DataFrame(results)

resilience_df = compute_shock_resilience(
    shock_df
)

# ============================================================
# ROBUST NORMALIZATION
# ============================================================

metrics = [
    "GDP_Resilience",
    "Unemployment_Resilience",
    "Productivity_Resilience",
    "Inflation_Stability",
    "Recovery_Speed"
]

scaler = RobustScaler()

resilience_df[metrics] = scaler.fit_transform(
    resilience_df[metrics]
)

# ============================================================
# GLOBAL SHOCK RESILIENCE SCORE
# ============================================================

resilience_df["Shock_Resilience_Score"] = (
    resilience_df[metrics]
    .mean(axis=1)
)

# ============================================================
# MERGE WITH POSET RESULTS
# ============================================================

merged_df = pd.merge(
    poset_df,
    resilience_df,
    on="Country",
    how="inner"
)

# ============================================================
# VALIDATION BY POSET LEVEL
# ============================================================

level_results = (

    merged_df
    .groupby("Poset_Level")[
        "Shock_Resilience_Score"
    ]
    .agg([
        "mean",
        "median",
        "std",
        "count"
    ])
    .reset_index()
)

level_results.columns = [
    "Poset_Level",
    "Mean_Resilience",
    "Median_Resilience",
    "Std_Resilience",
    "N_Countries"
]

# ============================================================
# MONOTONIC VALIDATION
# ============================================================
# Higher POSet levels should exhibit
# lower resilience.
# ============================================================

spearman_corr, spearman_p = spearmanr(
    merged_df["Poset_Level"],
    merged_df["Shock_Resilience_Score"]
)

# ============================================================
# KRUSKAL-WALLIS TEST
# ============================================================
# Non-parametric comparison between levels
# ============================================================

groups = []

for level in sorted(
    merged_df["Poset_Level"].unique()
):

    group = merged_df[
        merged_df["Poset_Level"] == level
    ]["Shock_Resilience_Score"]

    groups.append(group)

kruskal_stat, kruskal_p = kruskal(*groups)

# ============================================================
# SAVE RESULTS
# ============================================================

resilience_df.to_csv(
    "country_resilience_scores.csv",
    index=False
)

level_results.to_csv(
    "level_validation_results.csv",
    index=False
)

stats_df = pd.DataFrame({

    "Metric": [

        "Spearman_Correlation",
        "Spearman_PValue",
        "Kruskal_Statistic",
        "Kruskal_PValue"
    ],

    "Value": [

        spearman_corr,
        spearman_p,
        kruskal_stat,
        kruskal_p
    ]
})

stats_df.to_csv(
    "statistical_validation.csv",
    index=False
)

# ============================================================
# TERMINAL OUTPUT
# ============================================================

print("=" * 60)
print("POSET SHOCK VALIDATION")
print("=" * 60)

print()
print("LEVEL-BASED RESILIENCE")
print(level_results)

print()
print("=" * 60)

print(
    f"Spearman Correlation: "
    f"{spearman_corr:.4f}"
)

print(
    f"Spearman P-Value: "
    f"{spearman_p:.4f}"
)

print()
print(
    f"Kruskal Statistic: "
    f"{kruskal_stat:.4f}"
)

print(
    f"Kruskal P-Value: "
    f"{kruskal_p:.4f}"
)

print()
print("=" * 60)

if spearman_corr < 0:
    print(
        "Validation successful:"
    )
    print(
        "higher POSet levels are associated "
        "with lower resilience."
    )
else:
    print(
        "No negative monotonic relationship detected."
    )

print("=" * 60)