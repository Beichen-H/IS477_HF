# Data Dictionary

## Integrated Dataset: `data/processed/integrated_special_ed_data.csv`

This file is the primary analytical dataset produced by our pipeline. It merges three federal data sources using an inner join on the `State` key, retaining only states with complete data across all sources.

| Column | Type | Description | Source | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `State` | string | U.S. state name (e.g., "Alabama") | All three datasets | Primary join key; 37 states after inner join |
| `Median_Household_Income` | float | Estimated median household income in USD (2024) | ACS S1901 | Extracted from "Households!!Estimate" column group |
| `Total_Revenue_Thousands` | float | Total state education revenue in thousands of USD (FY 2024) | ELSEC Table 1, Column 2 | Only 37 states covered in 2024 release |
| `Per_Pupil_Spending` | float | Per-pupil current spending in USD (FY 2024) | ELSEC Table 1, Column 10 | Only 37 states covered in 2024 release |
| `HI_Student_Count` | float | Total count of students with Hearing Impairment served under IDEA Part B | IDEA 618 Child Count | Aggregated across all age groups; suppressed cells excluded |

## Clustered Dataset: `data/processed/clustered_integrated_dataset.csv`

This file extends the integrated dataset with K-Means clustering results.

| Column | Type | Description |
| :--- | :--- | :--- |
| All columns from integrated dataset | — | Same as above |
| `Cluster` | int | K-Means cluster assignment (0, 1, or 2) |
| `Cluster_Label` | string | Descriptive label: "Tier 1: Higher Income / Higher Spending", "Tier 2: Mid Income / Moderate Spending", or "Tier 3: Lower Income / Lower Spending" |

## Raw Data Files

### 1. `data/raw/ACSST1Y2024.S1901-2026-03-09T222516.csv`
- **Source:** U.S. Census Bureau, American Community Survey 1-Year Estimates (2024)
- **URL:** https://data.census.gov/table?q=S1901&g=010XX00US$0400000
- **Format:** CSV, wide format (17 rows × 417 columns)
- **Description:** Income distribution estimates for households across all U.S. states. Each state has 8 columns (4 categories × Estimate/Margin of Error).
- **Key field used:** "Median income (dollars)" row, "Households!!Estimate" columns
- **License:** Public domain (U.S. federal government work)

### 2. `data/raw/elsec24_sumtables.xlsx`
- **Source:** U.S. Census Bureau / NCES, Annual Survey of School System Finances (2024)
- **URL:** https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html
- **Format:** XLSX with 3 sheets; 62 rows × 12 columns in Table 1
- **Description:** State-level revenue, expenditures, and per-pupil spending for public school systems.
- **Coverage:** 37 of 52 reporting areas
- **Key fields used:** Column 0 (State name), Column 2 (Total Revenue), Column 10 (Per-Pupil Spending)
- **License:** Public domain (U.S. federal government work)

### 3. `data/raw/idea_child_count_2024.csv`
- **Source:** U.S. Department of Education, OSEP (EDPass)
- **URL:** https://data.ed.gov/dataset/docs/idea-section-618-state-part-b-child-count-and-educational-environments
- **Format:** CSV with 5 metadata header rows followed by data table
- **Description:** State-level counts of students with disabilities by disability category and age group. Contains privacy suppression symbols (`x`, `S`, `-`) for small cell counts.
- **Key fields used:** `State Name`, `SEA Disability Category` (filtered for "Hearing Impairment"), age-group columns
- **License:** Public domain (U.S. federal government work)

## Missing Data

The following 15 states/territories lack ELSEC finance data in the 2024 release and are excluded from the final integrated dataset (due to inner join): Alaska, Connecticut, District of Columbia, Illinois, Kansas, Louisiana, Massachusetts, Mississippi, Nevada, New Jersey, New York, Oregon, Tennessee, West Virginia, Puerto Rico.
