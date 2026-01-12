#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# ----------------------------
# 1️⃣ Load only selected rows from .h_info
# ----------------------------
rows_to_keep = [0,2,3,5,6,7,8,9]  # line numbers you want
param_names_to_keep = [
    "100~\\omega{}_{b}", "\\omega{}_{cdm}", "h", "ln10^{10}A_{s}", "n_{s}",
    "\\tau{}_{reio}", "\\delta{}_{Neff_drmd}", "log10z_{stop}", "f_{idm_drmd}",
    "log10_{G_over_aH_drmd}", "H0", "\\Omega{}_{m}", "sigma8", "rs_{d}", "z_{dec_drmd}"
]

rows = {}
with open("/home/jeppethybo/Grendel_files/DRMD_desi_iter/DRMD_desi_iter.h_info") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if i not in rows_to_keep:
            continue
        if ":" not in line:
            continue
        key, values = line.split(":", 1)
        key = key.strip()
        values = values.split()
        rows[key] = values

# ----------------------------
# 2️⃣ Build DataFrame with filtered params
# ----------------------------
params = [p for p in rows.get("param names", []) if p in param_names_to_keep]
df = pd.DataFrame(index=params)

for key, values in rows.items():
    if key == "param names":
        continue
    # Keep only filtered params
    filtered_values = [float(values[i]) for i, p in enumerate(rows["param names"]) if p in param_names_to_keep]
    df[key] = filtered_values

# ----------------------------
# 3️⃣ Format your 1σ and 2σ
# ----------------------------
def sigma_notation(row, sigma=1):
    return (
        rf"${row['mean']:.4f}"
        rf"^{{+{abs(row[f'{sigma}-sigma +']):.4f}}}"
        rf"_{{-{abs(row[f'{sigma}-sigma -']):.4f}}}$" 
    )

df['my_1sigma'] = df.apply(sigma_notation, axis=1, sigma=1)
df['my_2sigma'] = df.apply(sigma_notation, axis=1, sigma=2)

print(df.columns.tolist())


df['best_fit_connect'] = df['Best Fit'].apply(lambda x: f"${x:.4f}$")

# ----------------------------
# 4️⃣ Add article values for comparison
# ----------------------------
article_mean = {
    '100~\\omega{}_{b}': 2.310,
    '\\omega{}_{cdm}': 0.1344,
    'h': 0.7276,
    'ln10^{10}A_{s}': 3.050,
    'n_{s}': 0.9770,
    '\\tau{}_{reio}': 0.0618,
    '\\delta{}_{Neff_drmd}': 0.80,
    'log10z_{stop}': 3.64,
    'f_{idm_drmd}': 0.0442,
    'log10_{G_over_aH_drmd}': 13.057,
    'H0': 72.8,
    '\\Omega{}_{m}': 0.2987,
    'sigma8': 0.8120,
    'rs_{d}': 139.142,
    'z_{dec_drmd}': 1778.28
}

article_best_fit = {
    '100~\\omega{}_{b}': 2.313,
    '\\omega{}_{cdm}': 0.1353,
    'h': 0.7289,
    'ln10^{10}A_{s}': 3.050,
    'n_{s}': 0.9783,
    '\\tau{}_{reio}': 0.0609,
    '\\delta{}_{Neff_drmd}': 0.83,
    'log10z_{stop}':  4.83,
    'f_{idm_drmd}': 0.0285,
    'log10_{G_over_aH_drmd}': 13.057,
    'H0': 72.9,
    '\\Omega{}_{m}': 0.2995,
    'sigma8': 0.8115,
    'rs_{d}': 138.743,
    'z_{dec_drmd}': 2238.72
}

article_1_sigma_plus = {
    '100~\\omega{}_{b}': 0.018,
    '\\omega{}_{cdm}': 0.0037,
    'h': 0.0082,
    'ln10^{10}A_{s}': 0.015,
    'n_{s}': 0.0048,
    '\\tau{}_{reio}': 0.0068,
    '\\delta{}_{Neff_drmd}': 0.16,
    'log10z_{stop}': None,
    'f_{idm_drmd}': None,
    'log10_{G_over_aH_drmd}': None,
    'H0': 0.8,
    '\\Omega{}_{m}': 0.0039,
    'sigma8': 0.0089,
    'rs_{d}': 0.52,
    'z_{dec_drmd}': 1172.9
}

article_1_sigma_minus = {
    '100~\\omega{}_{b}': 0.018,
    '\\omega{}_{cdm}': 0.0037,
    'h': 0.0082,
    'ln10^{10}A_{s}': 0.017,
    'n_{s}': 0.0048,
    '\\tau{}_{reio}': 0.0084,
    '\\delta{}_{Neff_drmd}': 0.16,
    'log10z_{stop}': None,
    'f_{idm_drmd}': None,
    'log10_{G_over_aH_drmd}': None,
    'H0': 0.8,
    '\\Omega{}_{m}': 0.0039,
    'sigma8': 0.0089,
    'rs_{d}': 0.52,
    'z_{dec_drmd}': 48.4636
}




# Map article means into DataFrame
df['article_mean'] = df.index.map(article_mean)
df['article_1_sigma_plus'] = df.index.map(article_1_sigma_plus)
df['article_1_sigma_minus'] = df.index.map(article_1_sigma_minus)
df['best_fit_article'] = df.index.map(article_best_fit)

# Format article 1σ strings
def article_sigma_notation(row):
    if pd.isna(row['article_mean']):
        return ""
    plus = row['article_1_sigma_plus']
    minus = row['article_1_sigma_minus']
    return rf"${row['article_mean']:.4f}^{{+{plus:.4f}}}_{{-{minus:.4f}}}$"

df['article_1sigma'] = df.apply(article_sigma_notation, axis=1)

# ----------------------------
# 5️⃣ Generate LaTeX table
# ----------------------------
table = df[['best_fit_article','best_fit_connect', 'article_1sigma', 'my_1sigma', 'my_2sigma']].to_latex(
    escape=False, 
    index=True,
    column_format="lcccc",
    caption="Filtered DRMD parameters and comparison to article values.",
    label="tab:drmd_compare"
)

with open("drmd_params_filtered.tex", "w") as f:
    f.write(table)

print(table)
