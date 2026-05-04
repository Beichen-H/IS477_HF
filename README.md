# Interstate Special Education Resource Allocation Analysis
**Course: IS477  Data Management, Curation, and Reproducibility** | **Milestone 4: Full Pipeline & Analysis**

## Contributors
- **Beichen Hu** — Lead Data Engineer
- **Yizhou Fang** — Lead Data Steward

## Summary
This project investigates the relationship between state-level economic wealth (Median Household Income) and resources allocated to special education—specifically focusing on students with hearing impairments under the Individuals with Disabilities Education Act (IDEA).

IDEA mandates that all students with disabilities receive a Free Appropriate Public Education (FAPE). However, the actual funding mechanisms that support this mandate vary significantly across states. Some states allocate substantially more per pupil than others, raising critical questions about whether students with disabilities in lower-income states receive equitable support. By integrating socioeconomic data from the U.S. Census Bureau with school finance records and IDEA disability student counts, we aim to quantify whether wealthier states systematically invest more per student—and whether this creates structural inequities for special education communities in lower-income states.

We curated and integrated three federal datasets: the 2024 American Community Survey (ACS) S1901 table providing state-level median household income, the 2024 Public Elementary-Secondary School System Finances (ELSEC) providing per-pupil spending figures, and the IDEA Section 618 Part B Child Count data documenting students with hearing impairments by state. These three datasets represent the three pillars of our research: socioeconomic context (ACS), resource allocation (ELSEC), and student need (IDEA). Together, they enable a comprehensive assessment of whether funding aligns with the actual needs of special education communities.

Our data pipeline involved significant data engineering challenges. The Census Bureau's ACS data was stored in an extremely wide format with 417 columns, requiring a programmatic wide-to-long transformation using pandas. The ELSEC school finance data used a legacy Excel layout with dot-leader padded state names that prevented standard parsing. The IDEA child count data contained privacy suppression symbols for small student populations, consistent with FERPA regulations, which required careful handling to avoid violating student confidentiality. We resolved all of these issues through a fully automated Python pipeline that applies regular expressions for state name standardization and performs relational inner joins across all three sources using the cleaned state identifiers as join keys.

Our analysis of 37 states with complete data reveals a statistically significant positive correlation between median household income and per-pupil education spending. To move beyond simple correlation, we applied K-Means clustering (k=3, validated through the Elbow Method and Silhouette Score analysis) to segment states into three distinct socioeconomic-educational tiers. The results show that high-income states spend on average over $5,000 more per pupil than low-income states, confirming a meaningful disparity in educational investment. However, income explains only a portion of the variance in spending, suggesting that state-level tax policies, political priorities, and cost-of-living differences also play important roles.

For our second research question, we examined the relationship between hearing impairment student counts and total state education revenue. While we found a strong positive correlation, this relationship is largely confounded by state population size—larger states naturally have both more students with disabilities and larger education budgets. Future work normalizing by total student population would provide a more meaningful per-capita comparison. Overall, our findings highlight that significant funding disparities exist across U.S. states, and targeted federal interventions may be needed to ensure equitable support for special education students regardless of where they live.

## Data Profile

### Dataset 1: American Community Survey (ACS) 1-Year Estimates S1901 (2024)
- **Source:** U.S. Census Bureau
- **URL:** https://data.census.gov/table?q=S1901&g=010XX00US$0400000
- **File:** [`data/raw/ACSST1Y2024.S1901-2026-03-09T222516.csv`](data/raw/ACSST1Y2024.S1901-2026-03-09T222516.csv)
- **Structure:** CSV, wide format (17 rows × 417 columns). Each state has 8 columns (4 household categories × Estimate/Margin of Error). The rows represent income brackets (e.g., "Less than $10,000", "$10,000 to $14,999") plus summary statistics including "Median income (dollars)" and "Mean income (dollars)." The column headers follow a hierarchical naming convention such as "Alabama!!Households!!Estimate" that encodes both the geographic unit and the statistic type within the column name itself.
- **Content:** 2024 estimated median household income for 52 areas (50 states + DC + Puerto Rico). Range: $62,106 (Arkansas) to $102,905 (Maryland). The dataset also includes estimates for families, married-couple families, and nonfamily households, though we only extracted the "Households" median for our analysis.
- **Ethical/Legal:** Public domain (17 U.S.C. § 105). All values aggregated at the state level; no individual data. The Census Bureau applies statistical disclosure protections including sampling error margins to prevent identification of small populations.
- **Role:** Independent variable—classifies states by income level to test whether wealthier states allocate more funding per student.

### Dataset 2: Public Elementary-Secondary School System Finances (ELSEC 2024)
- **Source:** U.S. Census Bureau / NCES
- **URL:** https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html
- **File:** [`data/raw/elsec24_sumtables.xlsx`](data/raw/elsec24_sumtables.xlsx)
- **Structure:** XLSX with 3 sheets: "Table 1" (state-level summary, 62 rows × 12 columns), "Table 2" (additional breakdowns), and "Definitions" (column descriptions). Table 1 uses a legacy formatting style with dot-leader padding in state names (e.g., "Alabama…......") and multi-row descriptive headers that prevent standard pandas loading.
- **Content:** FY 2024 state-level revenue, expenditures, and per-pupil spending. Covers **37 of 52** reporting areas. The 15 missing states/territories are: Alaska, Connecticut, DC, Illinois, Kansas, Louisiana, Massachusetts, Mississippi, Nevada, New Jersey, New York, Oregon, Tennessee, West Virginia, and Puerto Rico. Key columns used: Column 2 (Total Revenue in thousands of dollars) and Column 10 (Per-Pupil Current Spending in dollars).
- **Ethical/Legal:** Public domain. No individual-level data. The 15-state coverage gap is a known limitation of the 2024 preliminary release and does not reflect data suppression.
- **Role:** Primary dependent variable—per-pupil spending is the direct measure of resource allocation we are analyzing in relation to state income levels.

### Dataset 3: IDEA Section 618 Part B Child Count (2024-25)
- **Source:** U.S. Department of Education, OSEP
- **URL:** https://data.ed.gov/dataset/docs/idea-section-618-state-part-b-child-count-and-educational-environments
- **File:** [`data/raw/idea_child_count_2024.csv`](data/raw/idea_child_count_2024.csv)
- **Structure:** CSV with 5 metadata header rows (skipped during processing), followed by a structured data table. Columns include `State Name`, `SEA Disability Category`, and multiple age-group columns (e.g., "Age 3-5", "Age 6-11", "Age 12-17", "Age 18-21") containing student counts. Some cells contain privacy suppression symbols (`x`, `S`, `-`) instead of numeric values, indicating that the true count falls below a minimum reporting threshold.
- **Content:** State-level counts of students with disabilities served under IDEA Part B, broken down by disability category and age group. We specifically filtered for the "Hearing Impairment" category and aggregated counts across all age groups to produce a single `HI_Student_Count` per state. Privacy-suppressed cells were converted to NaN to comply with FERPA regulations, meaning some state totals may be slightly underestimated.
- **Ethical/Legal:** Public domain. Small cell counts (fewer than 10 students) are suppressed with placeholder symbols (`S`, `x`, `-`) to protect student privacy under FERPA. We preserved these suppressions by converting them to NaN rather than imputing values, which would risk exposing protected student information.
- **Role:** Provides the student-level need data for Research Question 2, enabling us to assess whether states with more hearing-impaired students receive proportionally more funding.

## Data Quality
We performed a systematic quality assessment of all three datasets before and after integration, addressing four dimensions: completeness, consistency, accuracy, and structural integrity.

**Completeness:** The ACS income dataset is fully complete with median household income values for all 52 reporting areas (50 states, DC, and Puerto Rico), with no missing values in the fields we extracted. The ELSEC finance dataset has a significant completeness gap: only 37 of 52 states are represented in the 2024 preliminary release. This means that 15 states, including several large ones like New York, Illinois, New Jersey, and Massachusetts, are entirely absent from our finance data. This gap is not due to data suppression but rather the phased release schedule of the Census Bureau's fiscal survey. The IDEA child count data is structurally complete across all reporting jurisdictions, but contains privacy-suppressed values (`S`, `x`, `-`) for specific age-group cells where student counts fall below the minimum reporting threshold. These suppressed values were converted to NaN and excluded from aggregation, which means that the total hearing impairment count for some states may be slightly underestimated. We estimated that fewer than 5% of age-group cells were affected by suppression.

**Consistency:** State name standardization was the most significant consistency challenge in this project. Each of the three datasets used a different convention for representing state names. The ACS data embedded state names within multi-level column headers using a delimiter format (e.g., "Alabama!!Households!!Estimate"), requiring regex extraction to isolate the geographic component. The ELSEC data used dot-leader padding within a legacy Excel table (e.g., "Alabama…......"), requiring regex-based stripping of all non-alphabetic characters. The IDEA data used a plain "State Name" column that required only whitespace trimming. After applying our standardization pipeline, we verified that all state names matched exactly across sources by comparing the sorted unique values from each dataset. No mismatches or orphan records were found after cleaning.

**Accuracy:** We validated our extracted values against known benchmarks and published reports. Maryland appears as the highest-income state ($102,905) and Arkansas as the lowest ($62,106), which is consistent with Census Bureau press releases and other published analyses of the 2024 ACS data. For per-pupil spending, Vermont ranks highest ($28,818) and Idaho ranks lowest ($11,056), both of which align with NCES published tables. We also spot-checked several mid-range states (e.g., Ohio, Texas, Florida) and confirmed that their values matched the source tables. No implausible outliers or data entry errors were detected in any of the three datasets after cleaning.

**Structural Integrity:** The final integrated dataset was produced using an inner join strategy, which retains only the 37 states that appear in all three datasets. This conservative approach ensures that every row in the analytical dataset has complete values for income, spending, and hearing impairment counts, avoiding the complications of missing data during statistical analysis. We verified that the merged dataset contains no duplicate state entries and that all numeric columns have appropriate data types (float64). SHA-256 checksums are computed and printed during each pipeline execution for all three raw input files, enabling verification that the source data has not been corrupted or modified between runs.

## Data Cleaning
All cleaning operations were performed programmatically in Python using pandas, NumPy, and the `re` (regular expressions) module. No manual data manipulation was performed at any stage, ensuring that our entire pipeline is fully reproducible from raw inputs to final outputs.

**Wide-to-Long Transformation (ACS Data):** The Census S1901 file presented the most complex structural challenge. With 417 columns arranged in a hierarchical wide format, the data could not be used directly for analysis or merging. We applied `pandas.melt()` to unpivot the entire table, converting it from a 17-row by 417-column matrix into a long-format table with three columns: the row label, the original column name, and the cell value. From this melted table, we filtered for rows where the label matched "Median income (dollars)" and further filtered for columns containing the substring "!!Households!!Estimate" to isolate only the median household income estimates. This two-step filtering process reduced the dataset from over 7,000 melted rows to exactly 52 clean records—one per state/territory.

**State Name Extraction and Standardization:** Extracting clean state names from the ACS column headers required the regex pattern `r'^([a-zA-Z\s]+)!!'`, which captures all alphabetic characters and spaces before the first `!!` delimiter. For the ELSEC data, we first identified valid state rows using the pattern `r'\.{3,}'` (three or more consecutive periods), then stripped all non-alphabetic characters using `r'[^a-zA-Z\s]'` to remove the dot-leader padding. For the IDEA data, the `State Name` column was already in a usable format and required only `str.strip()` to remove leading and trailing whitespace. After standardization, we confirmed that all 37 states present in the ELSEC data had exact string matches in both the ACS and IDEA datasets.

**Numeric Coercion and Formatting (ACS and ELSEC Data):** The ACS income values contained embedded formatting characters including commas and dollar signs (e.g., "$66,659"). We applied `replace(r'[^\d.]', '', regex=True)` to strip all non-numeric characters except decimal points, then converted the cleaned strings to float using `pd.to_numeric(errors='coerce')`. For the ELSEC data, we read the Excel file with `header=None` to bypass the irregular multi-row header structure, then manually extracted the relevant columns by positional index (column 2 for Total Revenue, column 10 for Per-Pupil Spending). Both columns were coerced to numeric with the same `errors='coerce'` approach, which safely converts any remaining non-numeric artifacts to NaN rather than raising errors. The national aggregate row labeled "Reporting Areas" was explicitly filtered out to prevent it from being treated as a state.

**Privacy Suppression Handling (IDEA Data):** The IDEA child count CSV uses the symbols `x`, `S`, and `-` to suppress small cell counts in compliance with FERPA student privacy regulations. Our cleaning script replaces all three symbols with `np.nan` before converting the age-group columns to numeric types. When computing the total hearing-impaired student count per state, we used the pandas `sum()` function, which by default excludes NaN values from the summation. This means that if a state has one or two age groups suppressed, the remaining age groups are still summed correctly, and the total reflects the available data without any illegal imputation of the suppressed cells. We chose this approach deliberately to maintain compliance with federal privacy regulations while retaining as much analytical value as possible.

## Findings
Our analysis of 37 states with complete data across all three sources reveals meaningful and statistically significant relationships between state wealth, education spending, and special education needs.

**Research Question 1—Income vs. Spending Correlation:** The Pearson correlation analysis demonstrates a statistically significant positive relationship (**r = 0.422**) between median household income and per-pupil education spending. States with higher median incomes tend to allocate more dollars per student, confirming our initial hypothesis that economic wealth plays a role in education funding. However, income alone does not fully determine spending levels. The regression analysis shows that while the upward trend is clear and statistically significant, there is considerable scatter around the regression line, indicating that other factors—such as state tax structure, legislative priorities, unionization rates, and regional cost of living—also exert substantial influence on per-pupil spending. Some states like Wyoming spend well above what their income levels would predict, while states like Utah and Idaho spend below the trendline despite moderate income levels.

**K-Means Clustering Analysis (k=3):** To move beyond a simple linear relationship, we applied K-Means clustering to identify natural groupings among states based on both income and spending simultaneously. We evaluated cluster counts from k=2 through k=9 using both the Elbow Method (Within-Cluster Sum of Squares) and the Silhouette Score. The evaluation metrics indicated that k=3 provided the optimal balance between model complexity and cluster separation. The three resulting tiers are:
- **Tier 1 (Higher Income / Higher Spending):** This cluster includes states like Maryland, New Hampshire, and Virginia, which combine above-average household incomes with high per-pupil spending. These states generally have strong tax bases and a history of prioritizing education funding.
- **Tier 2 (Mid Income / High Spending Outliers):** This cluster captures states that fall near the national average for income but exhibit disproportionately high educational investment. A prime example is **Vermont**, which completely detaches from the linear trend to spend the highest amount per pupil in the nation (~$28,000) despite a moderate median income. Other states in this tier include Pennsylvania and Delaware.
- **Tier 3 (Lower Income / Lower Spending):** This cluster includes states like Arkansas, Idaho, South Carolina, and Oklahoma, which have both lower household incomes and lower per-pupil spending. Students with disabilities in these states may face resource constraints compared to their peers in Tier 1 states.

The clustering analysis reveals structural groupings that a simple correlation coefficient cannot capture, showing that states tend to cluster into distinct socioeconomic-educational profiles rather than falling along a smooth continuum.

**Research Question 2—Hearing Impairment and Revenue:** The Pearson correlation between hearing-impaired student counts (`HI_Student_Count`) and total state education revenue (`Total_Revenue_Thousands`) is exceptionally strong (**r = 0.974**). However, we interpret this result with caution. Both variables are heavily influenced by state population size: larger states like California, Texas, and Florida naturally have both more students with hearing impairments and larger education budgets. This means the observed correlation largely reflects a population size effect rather than a meaningful policy relationship. A more informative analysis would normalize hearing impairment counts by total student enrollment to produce a prevalence rate, then compare that rate against per-pupil spending rather than total revenue. This normalization is identified as a priority for future work.

![Regression: Income vs. Spending](data/processed/fig01_income_vs_spending.png)
![Cluster Evaluation](data/processed/fig02_cluster_evaluation.png)
![K-Means Clustering](data/processed/fig03_kmeans_clustering.png)

## Future Work
Several directions could extend and strengthen this analysis in meaningful ways.

First, the most impactful improvement would be **per-capita normalization** of the hearing impairment data. Currently, our analysis correlates raw student counts with total revenue, which conflates population size with funding adequacy. Dividing hearing-impaired student counts by total state enrollment would produce a prevalence rate that can be meaningfully compared across states of different sizes. This normalized metric could then be regressed against per-pupil spending (rather than total revenue) to test whether states with higher hearing impairment prevalence actually allocate more resources per affected student. This would directly address the equity question at the heart of our research.

Second, the **15-state gap** in the ELSEC finance data represents a significant limitation. Several of the missing states—including New York, Illinois, Massachusetts, New Jersey, and Connecticut—are among the largest and highest-spending states in the country. Their absence almost certainly affects our clustering results and may bias our correlation estimates. Future work could address this gap by incorporating ELSEC data from prior fiscal years (2022 or 2023) as a proxy, querying the Census Bureau API for supplementary finance tables, or using state-level education budget documents published by individual state agencies. Even partial recovery of these 15 states would substantially improve the generalizability of our findings.

Third, a **longitudinal analysis** tracking the income-spending relationship across multiple years (e.g., 2019–2024) would reveal whether funding disparities are widening or narrowing over time. This temporal dimension would also enable examination of how COVID-19 disruptions and subsequent federal relief funding (such as ESSER grants) affected state education budgets, and whether those effects were distributed equitably across income tiers.

Fourth, our current K-Means model uses only two variables (income and per-pupil spending). Incorporating **additional covariates** such as state tax revenue as a percentage of GDP, cost-of-living indices, student-teacher ratios, special education enrollment rates, and political party control of state legislatures could produce more nuanced and policy-relevant clusters. A principal component analysis (PCA) could also help identify which underlying factors most strongly differentiate the state tiers we identified.

Fifth, exploring **alternative clustering and classification methods** could yield additional insights. While K-Means provided interpretable results with three tiers, other approaches such as hierarchical clustering, DBSCAN, or Gaussian Mixture Models might reveal more nuanced groupings or identify outlier states that do not fit neatly into any tier. Additionally, a supervised classification approach could be used to predict which tier a state belongs to based on a broader set of socioeconomic and policy features, potentially identifying the most influential predictors of education funding levels.

Finally, this project provided several **lessons learned** about working with federal government data. Building programmatic regex-based pipelines from the outset proved essential, as the idiosyncratic formatting of both Census Bureau datasets would have made manual cleaning extremely error-prone and non-reproducible. The privacy suppression in the IDEA data reinforced the importance of treating suppressed values as genuinely missing (NaN) rather than as zeros or candidates for imputation, both for statistical accuracy and for ethical compliance with FERPA. We also learned the value of computing SHA-256 checksums for raw data files, which provides a simple but effective mechanism for verifying data integrity across pipeline executions.

## Challenges
We encountered several significant challenges during the course of this project, spanning data access, data formatting, and analytical methodology.

**Federal Data Portal Instability:** During our initial data acquisition phase for Milestone 3, the EDPass data portal (data.ed.gov) experienced persistent Internal Server Errors that prevented us from downloading the IDEA Section 618 child count data. This was an external factor entirely outside our control and caused a significant delay in our timeline. We eventually obtained the data through an alternative download path, but this experience underscored the importance of building resilient acquisition strategies when working with government data sources. Researchers should always plan for the possibility that a data portal may be temporarily unavailable and identify backup sources or cached versions in advance.

**Complex and Non-Standard Data Formatting:** Both Census Bureau datasets presented substantial formatting challenges that prevented standard loading methods. The ACS S1901 file uses an extremely wide format with 417 columns, where state names are embedded within multi-level column headers using `!!` delimiters. This format is optimized for human readability in Census Bureau table viewers but is poorly suited for programmatic analysis. The ELSEC finance data presented a different challenge: state names were padded with arbitrary sequences of dots and special characters within a legacy Excel layout that included multi-row descriptive headers. Both issues required custom regex-based parsing solutions rather than simple `pd.read_csv()` or `pd.read_excel()` calls. The time investment in building these regex parsers was significant but paid dividends in producing a fully automated and reproducible pipeline.

**Privacy Suppression in IDEA Data:** The IDEA child count data suppresses cells containing fewer than 10 students using the symbols `S`, `x`, and `-`. While this suppression is essential for protecting student privacy under FERPA, it creates analytical challenges. We cannot legally impute these values, and simply treating them as zero would undercount affected populations. Our solution—converting suppressed cells to NaN and excluding them from summation—is statistically conservative and ethically appropriate, but it means that our hearing impairment totals for some states may be slightly lower than the true values. This is a fundamental tension in working with education data: the need for individual privacy necessarily limits the precision of aggregate analyses.

**Spatial Coverage Gap:** The 2024 ELSEC release covers only 37 of 52 reporting areas. This is not a data quality issue per se—the Census Bureau simply has not yet collected fiscal year 2024 data from all states—but it significantly constrains our analysis. Our inner join strategy further limits the analytical dataset to only those states present in all three sources. The 15 missing states include several of the largest and wealthiest in the country (New York, Illinois, Massachusetts, New Jersey), which means our sample may underrepresent the high-spending end of the distribution and bias our correlation estimates and cluster assignments.

**Temporal Alignment:** Our three datasets span slightly different time periods: the ACS covers calendar year 2024, ELSEC covers fiscal year 2024 (which varies by state but typically runs July–June), and the IDEA data covers school year 2024–25. While these periods substantially overlap, the slight misalignment means we are not measuring all three variables at exactly the same point in time. For a cross-sectional analysis like ours, this is a minor limitation, but it would become more problematic in a longitudinal study where year-over-year changes are the focus.

## Reproducing
### Prerequisites
- Python 3.9+
- pip

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/Beichen-H/IS477_HF.git
cd IS477_HF

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline
snakemake -c1
```

This executes two rules:
1. `clean_and_integrate` → `scripts/01_data_pipeline.py` → produces `data/processed/integrated_special_ed_data.csv`
2. `analyze_data` → `scripts/02_data_analysis.py` → produces visualizations and `data/processed/clustered_integrated_dataset.csv`

### Output Files
| File | Description |
| :--- | :--- |
| `data/processed/integrated_special_ed_data.csv` | Merged dataset (37 states × 5 columns) |
| `data/processed/clustered_integrated_dataset.csv` | Dataset with K-Means cluster labels |
| `data/processed/fig01_income_vs_spending.png` | Regression scatter plot |
| `data/processed/fig02_cluster_evaluation.png` | Elbow method + silhouette score |
| `data/processed/fig03_kmeans_clustering.png` | State clustering visualization |

### Raw Data
All raw data files are included in the repository under `data/raw/`. SHA-256 checksums are computed and displayed during pipeline execution for integrity verification.

## References

### Datasets
1. U.S. Census Bureau. (2024). *American Community Survey 1-Year Estimates, Table S1901: Income in the Past 12 Months (in 2024 Inflation-Adjusted Dollars)*. https://data.census.gov/table?q=S1901&g=010XX00US$0400000
2. U.S. Census Bureau & NCES. (2024). *Annual Survey of School System Finances (ELSEC), Table 1: Summary of Public Elementary-Secondary School System Finances*. https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html
3. U.S. Department of Education, OSEP. (2025). *IDEA Section 618 State Part B Child Count and Educational Environments, SY 2024-25*. https://data.ed.gov/dataset/docs/idea-section-618-state-part-b-child-count-and-educational-environments

### Software
4. McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61.
5. Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362. https://doi.org/10.1038/s41586-020-2649-2
6. Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90–95. https://doi.org/10.1109/MCSE.2007.55
7. Waskom, M. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021. https://doi.org/10.21105/joss.03021
8. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
9. Mölder, F., et al. (2021). Sustainable data analysis with Snakemake. *F1000Research*, 10, 33. https://doi.org/10.12688/f1000research.29032.2

## Contributions

### Beichen Hu (Lead Data Engineer)
Beichen was responsible for the technical implementation of the project. He established the GitHub repository structure, authored the data pipeline script (`01_data_pipeline.py`) implementing regex-based parsing and cleaning for all three datasets, and developed the analysis script (`02_data_analysis.py`) with regression analysis and K-Means clustering. He configured the Snakemake workflow for end-to-end automation and managed all data acquisition, including finding an alternative source for the IDEA child count data when the original portal experienced server errors.

### Yizhou Fang (Lead Data Steward)
Yizhou was responsible for data quality assurance, metadata documentation, and project reporting. She reviewed and validated the structure of all three datasets, confirming their suitability for the research questions. She performed post-integration quality checks including verifying state name consistency across sources, validating that merged records were complete and free of duplicates, and confirming that privacy-suppressed values in the IDEA data were handled correctly. She authored the data dictionary, machine-readable metadata (Schema.org JSON-LD), and the documentation components of the final report including the Data Profile, Data Quality, Data Cleaning, and Challenges sections. She also ensured compliance with licensing requirements for all federal data sources.

## License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
All datasets are in the **public domain** as U.S. federal government works.
