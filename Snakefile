# Snakemake Workflow for Special Education Resource Allocation Project
import sys

PYTHON = sys.executable

rule all:
    input:
        "data/processed/fig01_income_vs_spending.png",
        "data/processed/fig02_cluster_evaluation.png",
        "data/processed/fig03_kmeans_clustering.png",
        "data/processed/clustered_integrated_dataset.csv"

rule analyze_data:
    input:
        "data/processed/integrated_special_ed_data.csv",
        "scripts/02_data_analysis.py"
    output:
        "data/processed/fig01_income_vs_spending.png",
        "data/processed/fig02_cluster_evaluation.png",
        "data/processed/fig03_kmeans_clustering.png",
        "data/processed/clustered_integrated_dataset.csv"
    shell:
        "{PYTHON} scripts/02_data_analysis.py"

rule clean_and_integrate:
    input:
        "data/raw/ACSST1Y2024.S1901-2026-03-09T222516.csv",
        "data/raw/elsec24_sumtables.xlsx",
        "data/raw/idea_child_count_2024.csv",
        "scripts/01_data_pipeline.py"
    output:
        "data/processed/integrated_special_ed_data.csv"
    shell:
        "{PYTHON} scripts/01_data_pipeline.py"