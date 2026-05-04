﻿# Project Plan: Analyzing Resource Allocation for Special Education across U.S. States

## Overview
This project investigates the equity of resource allocation for special education, specifically focusing on students with hearing impairments and other disabilities under the Individuals with Disabilities Education Act (IDEA). By integrating state-level disability statistics with federal funding and socioeconomic data, we aim to identify whether funding distribution aligns with the actual needs of special education communities. Our approach involves a comprehensive data curation pipeline, from automated acquisition to relational integration, providing a transparent look at how socioeconomic factors influence educational support for vulnerable groups.

Our plan has three main steps:
1. **Getting Data**: We will collect 2024 income and school funding data from the Census Bureau, along with 2024-25 student counts from the Department of Education (OSEP).
2. **Cleaning and Joining**: We will clean these different files and join them together using "State Name" as a common link to create one main table.
3. **Analysis**: We will look for patterns to see if states with more money actually provide more support for students with disabilities, such as those with hearing problems.

By following a clear data lifecycle, we make sure our work is easy to check, follows ethical rules, and is well-documented.

## Team
* **Beichen Hu**: **Role: Lead Data Engineer** Responsible for Overview, Research Questions and Datasets (Plan Part); Responsible for managing the GitHub repository, writing code to download data from APIs, joining the datasets using Python, and creating the final automated workflow. (Project)
* **Yizhou Fang**: **Role:Lead Data Steward** Responsible for Project Subject, Timeline and Constraints and Gaps (Plan Part). Responsible for checking data quality, making sure the data labels (metadata) are clear, and handling privacy and legal rules. (Project)

## Research Questions
1. **Fiscal Correlation**: To what extent does a state’s Median Household Income (Census S1901) correlate with the per-pupil federal funding allocated for special education (Census ELSEC Table 1)?
2. **Disparity Identification**: Which U.S. states demonstrate the most significant gap between the prevalence of students with hearing impairments and the growth of state-level educational appropriations in the 2024-25 cycle?

## Datasets
We will use three distinct, primary datasets that are entirely independent of Kaggle, ensuring clear provenance and providing real-world data wrangling opportunities:

1. **American Community Survey (ACS) 1-Year Estimates (2024):**
   - *Source:* U.S. Census Bureau. Link: https://data.census.gov/table?q=S1901&g=010XX00US$0400000
   - *Description:* Contains household economic characteristics and income estimates.
2. **Public Elementary-Secondary School System Finances (ELSEC 2024):**
   - *Source:* Annual Survey of School System Finances (Census/NCES). Link: https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html
   - *Description:* Contains state-level revenue, expenditures, and per-pupil spending metrics.
3. **IDEA Section 618 Part B Child Count Metadata (2024-25):**
   - *Source:* U.S. Department of Education (EDPass). Link:https://data.ed.gov/dataset/docs/idea-section-618-state-part-b-child-count-and-educational-environments
   - *Description:* Contains state-level administrative policies indicating which disability categories (e.g., Hearing Impairment, Autism) and environments are utilized.
   - *Status:* We have acquired the official 2024-25 metadata schemas (Files 5002/5003).

We selected these three specific datasets because they represent the three pillars of our research question: **Need**, **Resource**, and **Context**. 

* **The "Need" (IDEA Dataset)**: This dataset provides the numerator for our analysis—the actual count of students requiring specialized support. Without this, we cannot normalize the financial data to a "per-pupil" basis.
* **The "Resource" (ELSEC Dataset)**: This serves as our primary dependent variable. It reveals the actual federal and state dollars flowing into school systems. By combining this with the IDEA count, we can calculate the "Relative Funding Intensity" for each state.
* **The "Context" (ACS S1901 Dataset)**: This acts as our independent variable or grouping factor. It allows us to categorize states into economic tiers (e.g., High-Income vs. Low-Income states) to see if a state's general wealth dictates the level of support for its special education community.

### Data Integration Strategy
The datasets will be integrated using a relational model with **"State Name"** and **"Reporting Year"** as primary join keys. We will transform the Census "wide" format into a "tidy" long format to facilitate seamless merging with the IDEA student counts.】

Integration will be achieved through a **One-to-One Relational Join**. 
1. **Key Standardization**: We will first create a crosswalk table that maps OSEP's state names to the Census Bureau's FIPS codes to prevent "mismatch errors" caused by naming variations (e.g., "Wash. D.C." vs "District of Columbia").
2. **Merging**: Using Python’s `pandas` library, we will perform a `left join` on the **State identifier** and **Fiscal Year (2024)**. 
3. **Data Validation**: Post-integration, we will verify the row count (expecting 50 states + DC) to ensure no data was lost during the merge process. This integrated table will allow us to run a linear regression to answer whether `Median_Income` significantly predicts `Special_Ed_Spending_Per_Pupil`.

## Requirements and Curation Plan

### Data Lifecycle
We relate our project to the **DCC Curation Lifecycle Model**, documenting the transition from raw acquisition to analyzed findings.

### Files, Storage, and Organization
* **Structure**: Raw data in `/data/raw`, metadata in `/data/metadata`, and cleaned files in `/data/processed`.
* **Model**: We will use a tabular data model for the final integrated product.

### Ethical Data Handling
* **Privacy**: We will address issues related to confidentiality, specifically the suppression of small student counts ('S' values) in OSEP data to protect student identities.
* **Licensing**: Both datasets are public domain; we will cite the Census Bureau and the Dept. of Education accordingly.

### Data Quality and Cleaning
* **Assessment**: We will perform systematic profiling to detect outliers or inconsistencies in state-level reporting.
* **Cleaning**: We will apply semantic cleaning to normalize state identifiers and handle non-numeric suppression codes.

## Timeline
| Task | Description | Deadline | People |
| :--- | :--- | :--- | :--- |
| **Task 1: Project Plan and GitHub Setup** | We will write the milestone 2 document and create our code repository. We will set up folders for raw data, processed data, and metadata. We will submit the project plan link. | March 10, 2026 | Beichen Hu, Yizhou Fang |
| **Task 2: Data Acquisition** | We will download the 3 primary datasets. These include the census household income data, the school system finances data, and the special education child count metadata. We will write scripts to load these files safely into our workspace. | March 20, 2026 | Beichen Hu |
| **Task 3: Data Cleaning and Standardization** | The census data is currently in a wide shape. We need to change it to a long shape. We will also fix the state names in all 3 datasets so they match exactly. We will locate and handle the missing data for the states in the finance table. | March 27, 2026 | Yizhou Fang |
| **Task 4: Data Integration and Status Report** | We will join the 3 datasets into 1 large table. We will use the state name and the reporting year as the main keys to link them. After merging, we will write a status report of about 1500 words for milestone 3 to explain our progress. | March 31, 2026 | Beichen Hu, Yizhou Fang |
| **Task 5: Data Analysis and Pipeline Automation** | We will set up a tool called Snakemake to make our whole process run automatically from start to finish. Then, we will calculate the math to see the relationship between household income and special education spending per pupil. We will make graphs to show the results. | April 20, 2026 | Yizhou Fang |
| **Task 6: Final Report and Code Review** | We will write the final project paper for milestone 4. We will review our code to make sure it is clean and easy to read. We will add notes about data privacy and data ethics. We will turn in the final project. | May 3, 2026 | Beichen Hu, Yizhou Fang |
## Constraints and Gaps
1. Data Completeness and Spatial Coverage: The school finance data for 2024 only includes 37 states, which limits our spatial coverage. We will try to find the missing states using the census application programming interface.
2. Temporal Alignment: We are combining financial data from 2024, census estimates from 2024, and special education data from the 2024 to 2025 school year. The slight time difference between these periods could affect our results.
3. Technical Difficulties: The census dataset is very wide with complex column names. Changing this into a long shape so it matches the other files will take a lot of work.
4. Ethical Restrictions: The special education data hides small numbers to protect student privacy. This creates missing data that we cannot legally fill in, which might change our math results.

## Gaps
1. Data Integration: Anticipating the week 7 course topics, we need to learn more about global as view and local as view methods to define how our datasets will merge.
2. Missing Data Handling: Anticipating the week 9 and 10 topics, we do not know how to handle the hidden privacy numbers in the special education data without breaking our statistics.
3. Workflow Automation: Anticipating week 12, we need to research how to build a reproducible pipeline using Snakemake to connect all our steps automatically.

## Data Curation Plan
* **Cleaning (Module 10-12)**: We will fix state names (like changing "IL" to "Illinois") and turn text numbers into real numbers so we can do math.
* **Organization (Module 2)**: We will keep original files in a `raw` folder and cleaned files in a `processed` folder.
