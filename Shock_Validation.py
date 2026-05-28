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
#   - country_resilience_scores_{shock_id}.csv  (one per shock)
#   - level_validation_results_{shock_id}.csv   (one per shock)
#   - statistical_validation_{shock_id}.csv     (one per shock)
#   - combined_resilience_scores.csv            (averaged across shocks)
#   - combined_level_validation.csv             (averaged across shocks)
#   - combined_statistical_validation.csv       (both shocks)
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

# Each shock is defined by:
#   id          : short label used in filenames and reports
#   pre_start   : first year of the pre-shock baseline window
#   pre_end     : last  year of the pre-shock baseline window
#   shock_start : first year of the shock window
#   shock_end   : last  year of the shock window

SHOCKS = [
    {
        "id":          "GFC_2008",
        "label":       "Global Financial Crisis (2008)",
        "pre_start":   2005,
        "pre_end":     2007,
        "shock_start": 2008,
        "shock_end":   2010,
    },
    {
        "id":          "COVID_2020",
        "label":       "COVID-19 Pandemic (2020)",
        "pre_start":   2017,
        "pre_end":     2019,
        "shock_start": 2020,
        "shock_end":   2022,
    },
]

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

VALIDATION_COLUMNS = [
    "GDP_Growth",
    "Inflation",
    "Unemployment",
    "Productivity"
]

shock_df = shock_df.sort_values(
    ["Country", "Year"]
)

for col in VALIDATION_COLUMNS:

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

def compute_shock_resilience(df, shock_cfg):
    """
    Compute per-country resilience metrics for a single
    shock episode defined by shock_cfg.
    """

    pre_start   = shock_cfg["pre_start"]
    pre_end     = shock_cfg["pre_end"]
    shock_start = shock_cfg["shock_start"]
    shock_end   = shock_cfg["shock_end"]

    results = []

    for country in df["Country"].unique():

        cdf = df[df["Country"] == country]

        pre_shock = cdf[
            (cdf["Year"] >= pre_start)
            &
            (cdf["Year"] <= pre_end)
        ]

        shock_period = cdf[
            (cdf["Year"] >= shock_start)
            &
            (cdf["Year"] <= shock_end)
        ]

        if len(pre_shock) == 0:
            continue

        if len(shock_period) == 0:
            continue

        # ------------------------------------------------
        # GDP RESILIENCE
        # Higher = better
        # ------------------------------------------------

        baseline_gdp = pre_shock["GDP_Growth"].mean()
        worst_gdp    = shock_period["GDP_Growth"].min()

        gdp_resilience = worst_gdp - baseline_gdp

        # ------------------------------------------------
        # UNEMPLOYMENT RESILIENCE
        # Lower unemployment increase = better
        # ------------------------------------------------

        baseline_unemp = pre_shock["Unemployment"].mean()
        worst_unemp    = shock_period["Unemployment"].max()

        unemployment_resilience = baseline_unemp - worst_unemp

        # ------------------------------------------------
        # PRODUCTIVITY RESILIENCE
        # ------------------------------------------------

        baseline_prod = pre_shock["Productivity"].mean()
        worst_prod    = shock_period["Productivity"].min()

        productivity_resilience = worst_prod - baseline_prod

        # ------------------------------------------------
        # INFLATION STABILITY
        # Lower volatility = better
        # ------------------------------------------------

        inflation_stability = -(shock_period["Inflation"].std())

        # ------------------------------------------------
        # RECOVERY SPEED
        # Faster return to pre-shock GDP = better
        # ------------------------------------------------

        recovery_year = None

        for _, row in shock_period.iterrows():
            if row["GDP_Growth"] >= baseline_gdp:
                recovery_year = row["Year"]
                break

        if recovery_year is None:
            recovery_score = -(shock_end - shock_start + 1)
        else:
            recovery_score = -(recovery_year - shock_start)

        # ------------------------------------------------
        # STORE
        # ------------------------------------------------

        results.append({
            "Country":                   country,
            "Shock_ID":                  shock_cfg["id"],
            "GDP_Resilience":            gdp_resilience,
            "Unemployment_Resilience":   unemployment_resilience,
            "Productivity_Resilience":   productivity_resilience,
            "Inflation_Stability":       inflation_stability,
            "Recovery_Speed":            recovery_score,
        })

    return pd.DataFrame(results)

# ============================================================
# ROBUST NORMALISATION  +  GLOBAL SCORE
# ============================================================

METRICS = [
    "GDP_Resilience",
    "Unemployment_Resilience",
    "Productivity_Resilience",
    "Inflation_Stability",
    "Recovery_Speed",
]

def normalise_and_score(resilience_df):
    """
    Apply RobustScaler to the five raw metrics and compute
    the composite Shock_Resilience_Score.
    """
    scaler = RobustScaler()
    resilience_df[METRICS] = scaler.fit_transform(
        resilience_df[METRICS]
    )
    resilience_df["Shock_Resilience_Score"] = (
        resilience_df[METRICS].mean(axis=1)
    )
    return resilience_df

# ============================================================
# VALIDATION HELPERS
# ============================================================

def level_summary(merged_df):
    """Descriptive statistics per POSet level."""
    out = (
        merged_df
        .groupby("Poset_Level")["Shock_Resilience_Score"]
        .agg(["mean", "median", "std", "count"])
        .reset_index()
    )
    out.columns = [
        "Poset_Level",
        "Mean_Resilience",
        "Median_Resilience",
        "Std_Resilience",
        "N_Countries",
    ]
    return out


def statistical_tests(merged_df):
    """Spearman correlation + Kruskal-Wallis across POSet levels."""

    spearman_corr, spearman_p = spearmanr(
        merged_df["Poset_Level"],
        merged_df["Shock_Resilience_Score"]
    )

    groups = [
        merged_df[merged_df["Poset_Level"] == lvl]["Shock_Resilience_Score"]
        for lvl in sorted(merged_df["Poset_Level"].unique())
    ]

    kruskal_stat, kruskal_p = kruskal(*groups)

    return pd.DataFrame({
        "Metric": [
            "Spearman_Correlation",
            "Spearman_PValue",
            "Kruskal_Statistic",
            "Kruskal_PValue",
        ],
        "Value": [
            spearman_corr,
            spearman_p,
            kruskal_stat,
            kruskal_p,
        ],
    })

# ============================================================
# MAIN LOOP — one run per shock episode
# ============================================================

all_resilience   = []   # raw (pre-normalisation) frames
all_level        = []
all_stats        = []

for shock_cfg in SHOCKS:

    shock_id = shock_cfg["id"]

    print("=" * 60)
    print(f"PROCESSING SHOCK: {shock_cfg['label']}")
    print("=" * 60)

    # ----------------------------------------------------------
    # Compute raw resilience metrics
    # ----------------------------------------------------------

    res_df = compute_shock_resilience(shock_df, shock_cfg)

    # ----------------------------------------------------------
    # Normalise within this shock episode
    # ----------------------------------------------------------

    res_df = normalise_and_score(res_df)

    # ----------------------------------------------------------
    # Merge with POSet levels
    # ----------------------------------------------------------

    merged = pd.merge(
        poset_df[["Country", "Poset_Level"]],
        res_df,
        on="Country",
        how="inner"
    )

    # ----------------------------------------------------------
    # Level summary + statistical tests
    # ----------------------------------------------------------

    lv = level_summary(merged)
    lv["Shock_ID"] = shock_id

    st = statistical_tests(merged)
    st["Shock_ID"] = shock_id

    # ----------------------------------------------------------
    # Print
    # ----------------------------------------------------------

    print()
    print("LEVEL-BASED RESILIENCE")
    print(lv.drop(columns="Shock_ID").to_string(index=False))
    print()
    print(f"Spearman Correlation : {st.loc[st['Metric']=='Spearman_Correlation','Value'].values[0]:.4f}")
    print(f"Spearman P-Value     : {st.loc[st['Metric']=='Spearman_PValue','Value'].values[0]:.4f}")
    print(f"Kruskal Statistic    : {st.loc[st['Metric']=='Kruskal_Statistic','Value'].values[0]:.4f}")
    print(f"Kruskal P-Value      : {st.loc[st['Metric']=='Kruskal_PValue','Value'].values[0]:.4f}")
    print()

    spearman_corr = st.loc[st["Metric"] == "Spearman_Correlation", "Value"].values[0]

    if spearman_corr < 0:
        print("Validation: higher POSet levels → lower resilience  ✓")
    else:
        print("No negative monotonic relationship detected.")

    print()

    # ----------------------------------------------------------
    # Per-shock CSVs
    # ----------------------------------------------------------

    res_df.to_csv(
        f"country_resilience_scores_{shock_id}.csv",
        index=False
    )

    lv.to_csv(
        f"level_validation_results_{shock_id}.csv",
        index=False
    )

    st.to_csv(
        f"statistical_validation_{shock_id}.csv",
        index=False
    )

    # ----------------------------------------------------------
    # Accumulate for combined outputs
    # ----------------------------------------------------------

    merged["Shock_ID"] = shock_id
    all_resilience.append(merged)
    all_level.append(lv)
    all_stats.append(st)

# ============================================================
# COMBINED OUTPUT
# ============================================================

combined_resilience = pd.concat(all_resilience, ignore_index=True)
combined_level      = pd.concat(all_level,      ignore_index=True)
combined_stats      = pd.concat(all_stats,      ignore_index=True)

# ----------------------------------------------------------
# Average resilience score per country across both shocks
# ----------------------------------------------------------

avg_resilience = (
    combined_resilience
    .groupby("Country")
    .agg(
        Poset_Level=("Poset_Level", "first"),
        Mean_Shock_Resilience_Score=("Shock_Resilience_Score", "mean"),
        N_Shocks=("Shock_Resilience_Score", "count"),
    )
    .reset_index()
)

# ----------------------------------------------------------
# Average level statistics across both shocks
# ----------------------------------------------------------

avg_level = (
    combined_level
    .groupby("Poset_Level")
    .agg(
        Mean_Resilience=("Mean_Resilience", "mean"),
        Median_Resilience=("Median_Resilience", "mean"),
        Std_Resilience=("Std_Resilience", "mean"),
        N_Countries=("N_Countries", "mean"),
    )
    .reset_index()
)

# ----------------------------------------------------------
# Save combined CSVs
# ----------------------------------------------------------

avg_resilience.to_csv("combined_resilience_scores.csv",     index=False)
avg_level.to_csv("combined_level_validation.csv",      index=False)
combined_stats.to_csv("combined_statistical_validation.csv", index=False)

# ============================================================
# COMBINED TERMINAL SUMMARY
# ============================================================

print("=" * 60)
print("COMBINED VALIDATION SUMMARY (both shocks)")
print("=" * 60)
print()
print(avg_level.to_string(index=False))
print()

for shock_cfg in SHOCKS:
    shock_id = shock_cfg["id"]
    sub = combined_stats[combined_stats["Shock_ID"] == shock_id]

    def val(metric):
        return sub.loc[sub["Metric"] == metric, "Value"].values[0]

    print(f"--- {shock_cfg['label']} ---")
    print(f"  Spearman r = {val('Spearman_Correlation'):.4f}  "
          f"(p = {val('Spearman_PValue'):.4f})")
    print(f"  Kruskal H  = {val('Kruskal_Statistic'):.4f}  "
          f"(p = {val('Kruskal_PValue'):.4f})")
    print()

print("=" * 60)