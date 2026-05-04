import pandas as pd
import numpy as np
import os
import hashlib

# =======================================================
# 1. Environment Setup & Data Integrity Check
# =======================================================
def calculate_sha256(file_path):
    """Calculate SHA-256 hash of a file for project integrity checks."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

raw_dir = "data/raw/"
processed_dir = "data/processed/"
os.makedirs(processed_dir, exist_ok=True)

income_file = os.path.join(raw_dir, "ACSST1Y2024.S1901-2026-03-09T222516.csv")
finance_file = os.path.join(raw_dir, "elsec24_sumtables.xlsx")
idea_file = os.path.join(raw_dir, "idea_child_count_2024.csv")

# Compute and log SHA-256 checksums for raw datasets
for f in [income_file, finance_file, idea_file]:
    if os.path.exists(f):
        print(f"[Checksum] {os.path.basename(f)}: {calculate_sha256(f)}")

# =======================================================
# 2. Process Census Income Data
# =======================================================
df_income_raw = pd.read_csv(income_file)
melted = df_income_raw.melt(id_vars=['Label (Grouping)'], var_name='Col', value_name='Val')
median_rows = melted[melted['Label (Grouping)'].str.strip() == 'Median income (dollars)'].copy()
est_rows = median_rows[median_rows['Col'].str.contains('!!Households!!Estimate', na=False)].copy()

# Extract state names and clean numeric values
est_rows['State'] = est_rows['Col'].str.extract(r'^([a-zA-Z\s]+)!!', expand=False).str.strip()
est_rows['Median_Household_Income'] = pd.to_numeric(est_rows['Val'].replace(r'[^\d.]', '', regex=True), errors='coerce')
df_income = est_rows[['State', 'Median_Household_Income']].dropna().drop_duplicates(subset=['State'])

# =======================================================
# 3. Process ELSEC Finance Data
# =======================================================
df_fin_raw = pd.read_excel(finance_file, sheet_name='Table 1', header=None)

# Identify valid state rows using regex (looking for trailing periods)
state_rows = df_fin_raw[df_fin_raw[0].astype(str).str.contains(r'\.{3,}', na=False)].copy()
state_rows['State'] = state_rows[0].str.replace(r'[^a-zA-Z\s]', '', regex=True).str.strip()

# Extract total revenue and per-pupil spending
df_finance = state_rows[['State', 2, 10]].copy()
df_finance.columns = ['State', 'Total_Revenue_Thousands', 'Per_Pupil_Spending']
df_finance[['Total_Revenue_Thousands', 'Per_Pupil_Spending']] = df_finance[['Total_Revenue_Thousands', 'Per_Pupil_Spending']].apply(pd.to_numeric, errors='coerce')

# Filter out national aggregate rows
df_finance = df_finance[df_finance['State'] != 'Reporting Areas'].reset_index(drop=True)

# =======================================================
# 4. Process IDEA Special Ed Data
# =======================================================
# Skip top 5 metadata rows to read the actual data table
df_idea_raw = pd.read_csv(idea_file, skiprows=5)
df_idea_raw.columns = [str(col).strip() for col in df_idea_raw.columns]

# Filter specifically for the "Hearing Impairment" category
df_hi = df_idea_raw[df_idea_raw['SEA Disability Category'].astype(str).str.contains('Hearing Impairment', case=False, na=False)].copy()

# Identify all columns containing student age groups or totals
age_cols = [col for col in df_hi.columns if 'Age' in col or 'Total' in col]

# Clean privacy suppression symbols and convert columns to numeric
for col in age_cols:
    df_hi[col] = pd.to_numeric(df_hi[col].astype(str).replace(['x', 'S', '-'], np.nan), errors='coerce')

# Aggregate the total count of hearing impaired students by state
df_hi['HI_Student_Count'] = df_hi[age_cols].sum(axis=1)
df_idea_final = df_hi.groupby('State Name')['HI_Student_Count'].sum().reset_index()

df_idea_final.rename(columns={'State Name': 'State'}, inplace=True)
df_idea_final['State'] = df_idea_final['State'].str.strip()

# =======================================================
# 5. Master Integration (Inner Join) - 这里是刚才漏掉的！
# =======================================================
# Merge all three datasets sequentially on the "State" key
master_df = pd.merge(df_income, df_finance, on="State", how="inner")
master_df = pd.merge(master_df, df_idea_final, on="State", how="inner")

# Drop any rows without a valid state name to ensure data integrity
master_df = master_df.dropna(subset=['State'])

# Save the fully integrated master dataset
# 注意：这里的名字必须和 Snakefile 里的保持一致
output_path = os.path.join(processed_dir, "integrated_special_ed_data.csv")
master_df.to_csv(output_path, index=False)

print(f"Dataset shape: {master_df.shape}")
print(f"Saved integrated data to: {output_path}")