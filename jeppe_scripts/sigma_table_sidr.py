#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# ----------------------------
# 1️⃣ Load only selected rows from .h_info
# ----------------------------
rows_to_keep = [0,3,5,6,7]  # line numbers you want
param_names_to_keep = [
    "100~\\omega{}_{b}", "\\omega{}_{cdm}", "100*\theta{}_{s}", "n_{s}", "r", "m_{ncdm_interacting}", "log10G_{eff_ncdm_interacting}",
    "deg_{ncdm_interacting}", "H0"
]

rows = {}
with open("/home/jeppethybo/connect_public/Grendel_files/SIDR_iter_2/SIDR_iter_2.h_info") as f:
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

# ----------------------------
# 4️⃣ Add article values for comparison
# ----------------------------
NI_mean = {
    '100~\\omega{}_{b}': 2.2380,
    '\\omega{}_{cdm}': 0.1185,
    'n_{s}': 0.9650,
    'r': None,  # < 0.037
    'm_{ncdm_interacting}': None,  # < 0.119
    'log10G_{eff_ncdm_interacting}': None,  # unconstrained
    'deg_{ncdm_interacting}': 2.99,
    'H0': 67.40
}

NI_1_sigma_plus = {
    '100~\\omega{}_{b}': 0.00017,
    '\\omega{}_{cdm}': 0.0027,
    'n_{s}': 0.006,
    'r': None,
    'm_{ncdm_interacting}': None,
    'log10G_{eff_ncdm_interacting}': None,
    'deg_{ncdm_interacting}': 0.16,
    'H0': 1.00
}

NI_1_sigma_minus = {
    '100~\\omega{}_{b}': 0.00017,
    '\\omega{}_{cdm}': 0.0027,
    'n_{s}': 0.006,
    'r': None,
    'm_{ncdm_interacting}': None,
    'log10G_{eff_ncdm_interacting}': None,
    'deg_{ncdm_interacting}': 0.16,
    'H0': 1.00
}

MI_mean = {
    '100~\\omega{}_{b}': 2.2330,
    '\\omega{}_{cdm}': 0.1184,
    'n_{s}': 0.9650,
    'r': None,  # < 0.034
    'm_{ncdm_interacting}': None,  # < 0.121
    'log10G_{eff_ncdm_interacting}': None,  # only upper limit
    'deg_{ncdm_interacting}': 2.97,
    'H0': 67.20
}

MI_1_sigma_plus = {
    '100~\\omega{}_{b}': 0.00019,
    '\\omega{}_{cdm}': 0.0028,
    'n_{s}': 0.008,
    'r': None,
    'm_{ncdm_interacting}': None,
    'log10G_{eff_ncdm_interacting}': None,
    'deg_{ncdm_interacting}': 0.17,
    'H0': 1.10
}

MI_1_sigma_minus = {
    '100~\\omega{}_{b}': 0.00019,
    '\\omega{}_{cdm}': 0.0030,
    'n_{s}': 0.007,
    'r': None,
    'm_{ncdm_interacting}': None,
    'log10G_{eff_ncdm_interacting}': None,
    'deg_{ncdm_interacting}': 0.19,
    'H0': 1.10
}

SI_mean = {
    '100~\\omega{}_{b}': 2.2360,
    '\\omega{}_{cdm}': 0.1160,
    'n_{s}': 0.9300,
    'r': None,  # < 0.037
    'm_{ncdm_interacting}': None,  # < 0.161
    'log10G_{eff_ncdm_interacting}': -1.70,
    'deg_{ncdm_interacting}': 2.76,
    'H0': 66.90
}

SI_1_sigma_plus = {
    '100~\\omega{}_{b}': 0.00018,
    '\\omega{}_{cdm}': 0.0027,
    'n_{s}': 0.006,
    'r': None,
    'm_{ncdm_interacting}': None,
    'log10G_{eff_ncdm_interacting}': 0.17,
    'deg_{ncdm_interacting}': 0.15,
    'H0': 1.0
}

SI_1_sigma_minus = {
    '100~\\omega{}_{b}': 0.00018,
    '\\omega{}_{cdm}': 0.0027,
    'n_{s}': 0.006,
    'r': None,
    'm_{ncdm_interacting}': None,
    'log10G_{eff_ncdm_interacting}': 0.10,
    'deg_{ncdm_interacting}': 0.17,
    'H0': 1.1
}




# Map article means into DataFrame
df['NI_mean'] = df.index.map(NI_mean)
df['NI_1_sigma_plus'] = df.index.map(NI_1_sigma_plus)
df['NI_1_sigma_minus'] = df.index.map(NI_1_sigma_minus)

df['MI_mean'] = df.index.map(MI_mean)
df['MI_1_sigma_plus'] = df.index.map(MI_1_sigma_plus)
df['MI_1_sigma_minus'] = df.index.map(MI_1_sigma_minus)

df['SI_mean'] = df.index.map(SI_mean)
df['SI_1_sigma_plus'] = df.index.map(SI_1_sigma_plus)
df['SI_1_sigma_minus'] = df.index.map(SI_1_sigma_minus)


# Format article 1σ strings
def article_sigma_notation(row, model):
    mean = row.get(f"{model}_mean")
    plus = row.get(f"{model}_1_sigma_plus")
    minus = row.get(f"{model}_1_sigma_minus")
    
    # Handle missing values
    if pd.isna(mean) or mean is None:
        return ""
    if plus is None or minus is None or pd.isna(plus) or pd.isna(minus):
        return "unconstrained"
    
    return rf"${mean:.4f}^{{+{plus:.4f}}}_{{-{minus:.4f}}}$"


df['NI_1sigma'] = df.apply(article_sigma_notation, axis=1, model='NI')
df['MI_1sigma'] = df.apply(article_sigma_notation, axis=1, model='MI')
df['SI_1sigma'] = df.apply(article_sigma_notation, axis=1, model='SI')

# ----------------------------
# 5️⃣ Generate LaTeX table
# ----------------------------
table = df[['NI_1sigma', 'MI_1sigma', 'SI_1sigma', 'my_1sigma']].to_latex(
    escape=False, 
    index=True,
    column_format="lcccc",
    caption="Filtered DRMD parameters and comparison to article values.",
    label="tab:drmd_compare"
)

with open("drmd_params_filtered.tex", "w") as f:
    f.write(table)

print(table)
