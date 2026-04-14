# Interim Status Report
**Project:** Analyzing Resource Allocation for Special Education across U.S. States
**Team:** Beichen Hu (Lead Data Engineer) & Yizhou Fang (Lead Data Steward)

## 1. Project Overview & Current Status
This project investigates the equity of resource allocation for special education by integrating state-level disability statistics with federal funding and socioeconomic data. Specifically, we are examining the extent to which a state's Median Household Income (Census S1901) correlates with the per-pupil federal funding allocated for special education (Census ELSEC Table 1). 

**Current Status:** The project is progressing steadily and is currently on track. We have successfully transitioned from the project planning phase into the active data acquisition and data cleaning phases. We have built an automated, highly robust Python data pipeline that programmatically acquires, cleans, and integrates our primary financial and socioeconomic datasets. The initial relational merge has successfully output a clean, tidy dataset of 52 records (representing 50 states, Washington D.C., and national aggregates), which establishes the foundation for our upcoming statistical analysis.

## 2. Task Updates & Artifact References
We have made significant progress on our initial tasks. Below is a detailed update on each phase, including links to the specific artifacts generated in our GitHub repository:

* **Task 1: Project Plan and GitHub Setup (Completed)**
  * **Update:** We successfully initialized our Git repository and established a standardized directory structure to separate raw inputs from processed outputs. This ensures data provenance and prevents the accidental overwrite of source files. 
  * **Artifacts:** Our initial plan is documented in `[ProjectPlan.md](./ProjectPlan.md)`. The directory structure can be viewed here: `[/data/raw](./data/raw)`, `[/data/processed](./data/processed)`, and `[/scripts](./scripts)`.

* **Task 2: Data Acquisition (Completed)**
  * **Update:** We acquired the 2024 American Community Survey (ACS) 1-Year Estimates and the 2024 Public Elementary-Secondary School System Finances (ELSEC) data. These were downloaded directly from official U.S. Census Bureau endpoints.
  * **Artifacts:** Raw data files are securely stored in the raw data folder: `[ACSST1Y2024.csv](./data/raw/ACSST1Y2024.S1901-2026-03-09T222516.csv)` and `[elsec24_sumtables.xlsx](./data/raw/elsec24_sumtables.xlsx)`.

* **Task 3: Data Cleaning and Standardization (Completed)**
  * **Update:** Rather than manual cleaning, we engineered a programmatic Python pipeline. This script handles wide-to-long transformations and aggressive string sanitization using Regular Expressions (`re`) to ensure spatial keys (State Names) perfectly align.
  * **Artifacts:** The core cleaning and integration script is located at `[01_data_pipeline.py](./scripts/01_data_pipeline.py)`.

* **Task 4: Data Integration and Status Report (In Progress)**
  * **Update:** We successfully executed a Left Join on the "State" key for the ACS and ELSEC datasets. The output is a verified, structurally sound dataframe. The final step of integrating the IDEA Section 618 child count data is pending due to external server issues (detailed in Section 5).
  * **Artifacts:** The preliminary integrated dataset can be reviewed at `[integrated_special_ed_data.csv](./data/processed/integrated_special_ed_data.csv)`. This document serves as the Status Report artifact.

## 3. Updated Timeline
The following table outlines our adjusted timeline, indicating the current status of each task and projected completion dates.

| Task | Description | Status | Target Date | Assignee |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | Project Plan and GitHub Setup | ✅ Completed | Mar 10, 2026 | Beichen, Yizhou |
| **Task 2** | Data Acquisition (ACS, ELSEC, IDEA) | ✅ Completed* | Mar 20, 2026 | Beichen |
| **Task 3** | Data Cleaning and Standardization | ✅ Completed | Mar 27, 2026 | Yizhou |
| **Task 4** | Data Integration and Status Report | 🔄 In Progress | Mar 31, 2026 | Beichen, Yizhou |
| **Task 5** | Data Analysis and Pipeline Automation | ⏳ Not Started | Apr 20, 2026 | Yizhou |
| **Task 6** | Final Report and Code Review | ⏳ Not Started | May 3, 2026 | Beichen, Yizhou |
*(Note: Acquisition of the final IDEA dataset is pending external server restoration).*

## 4. Changes to Project Plan
While our core research questions remain identical, we have made strategic adjustments to our methodology and project plan based on the realities of the data we acquired:

1. **Pivot to Programmatic Regex Cleaning:** Initially, we anticipated utilizing manual or semi-automated tools for data standardization. However, acknowledging the emphasis on reproducibility and feedback regarding data integrity, we shifted to a 100% code-based approach. We developed a Python script leveraging `pandas` and the `re` (Regular Expressions) library. This change ensures that our cleaning process is fully transparent, repeatable, and eliminates human error during data manipulation.
2. **Modular Integration Strategy:** We originally planned to merge all three datasets simultaneously. Due to structural complexities, we altered our plan to a step-wise relational merge. We have successfully merged the Census and Finance data as a "base table" and will append the IDEA data in a subsequent pass.

## 5. Challenges Encountered and Resolutions
Data curation frequently involves unexpected formatting and access issues. We encountered three major challenges and implemented robust solutions for each:

* **Challenge 1: Census Wide-Format Duplication and Noise:** The ACS S1901 dataset utilizes a highly complex wide format, combining multiple demographic sub-categories under a single "Median income" header and embedding descriptive text strings within numeric estimate columns (e.g., "Alabama!!Households!!Estimate").
  * **Resolution:** We utilized the `pandas.melt()` function to pivot the data into a long, tidy format. Subsequently, we applied precise regular expressions (`str.extract(r'^([a-zA-Z\s]+)!!')`) to dynamically isolate the state names. We also applied `replace(r'[^\d.]', '')` to strip out currency symbols and commas, successfully coercing the targets into clean numeric floats without data loss.

* **Challenge 2: Messy Excel Headers and Padded Strings:** The ELSEC Table 1 finance data was provided as a legacy Excel table containing unreadable metadata header rows. Furthermore, the state names were padded with arbitrary periods (e.g., "Alabama......."), which would cause our relational joins to fail.
  * **Resolution:** We bypassed standard CSV reading and utilized the `openpyxl` engine within `pandas` to target the specific Excel sheet directly. We applied a regex pattern (`str.contains(r'\.{3,}')`) to programmatically locate valid state rows, followed by a secondary regex pass (`str.replace(r'[^a-zA-Z\s]', '')`) to sanitize the state names. This guaranteed a perfect 1-to-1 key match during integration.

* **Challenge 3: External Server Outage (IDEA Data):** During the final data acquisition phase for the IDEA child count dataset, the official U.S. Department of Education portal experienced an "Internal Server Error" (HTTP 500), preventing the download of the raw numeric data tables.
  * **Plan to Address:** To maintain continuous integration and avoid blocking the project timeline, we designed our Python pipeline with conditional logic. The pipeline currently bypasses the missing IDEA dataset and successfully integrates the Census and ELSEC data. We will monitor the government server and acquire the IDEA data once restored, seamlessly plugging it into our pipeline for Milestone 4.

## 6. Individual Contributions

### Beichen Hu (Lead Data Engineer)
For this milestone, I established the GitHub repository structure to reflect best practices in data engineering (`/raw`, `/processed`, `/scripts`). I served as the primary architect for the `01_data_pipeline.py` script. Recognizing the complexity of the Census and ELSEC data, I implemented advanced Regular Expressions (Regex) to parse the wide-to-long transformation and sanitize the messy categorical strings. I engineered the relational merge using `pandas` (Left Joins on the "State" identifier), verified the structural integrity of the output dataframe (`shape: 52, 4`), and drafted the technical methodology sections of this status report. 

### Yizhou Fang (Lead Data Steward)
For this milestone, I was responsible for data quality assurance and metadata documentation. I reviewed the structure and schema of all three acquired datasets to verify their suitability for our research questions. I examined the IDEA metadata file and confirmed which disability categories (including Hearing Impairment) and educational environments each state reports, documenting these findings for the team. I performed post-integration validation on the merged dataset by verifying that the state name matching between ACS and ELSEC sources was consistent, confirming that the expected 37-state coverage in the ELSEC data was preserved after the merge, and ensuring that no records were lost or duplicated during the join process. I also contributed to this status report by documenting the data quality constraints, the IDEA data gap, and the ethical considerations related to suppressed student counts in the OSEP data.
