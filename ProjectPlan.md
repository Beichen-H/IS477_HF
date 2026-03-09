# Project Plan: Analyzing Resource Allocation for Special Education across U.S. States

## Overview
This project investigates the equity of resource allocation for special education, specifically focusing on students with hearing impairments and other disabilities under the Individuals with Disabilities Education Act (IDEA). By integrating state-level disability statistics with federal funding and socioeconomic data, we aim to identify whether funding distribution aligns with the actual needs of special education communities. Our approach involves a comprehensive data curation pipeline, from automated acquisition to relational integration, providing a transparent look at how socioeconomic factors influence educational support for vulnerable groups.

## Team
* **Beichen Hu**: **Role:** Responsible for
* **Yizhou Fang**: **Role:** Responsible for 

## Research Questions
1. **Fiscal Correlation**: To what extent does a state’s Median Household Income (Census S1901) correlate with the per-pupil federal funding allocated for special education (Census ELSEC Table 1)?
2. **Disparity Identification**: Which U.S. states demonstrate the most significant gap between the prevalence of students with hearing impairments and the growth of state-level educational appropriations in the 2024-25 cycle?

## Datasets
We will use three distinct, primary datasets that are entirely independent of Kaggle, ensuring clear provenance and providing real-world data wrangling opportunities:

1. **American Community Survey (ACS) 1-Year Estimates (2024):** - *Source:* U.S. Census Bureau.
   - *Description:* Contains household economic characteristics and income estimates.
2. **Public Elementary-Secondary School System Finances (ELSEC 2024):** - *Source:* Annual Survey of School System Finances (Census/NCES).
   - *Description:* Contains state-level revenue, expenditures, and per-pupil spending metrics.
3. **IDEA Section 618 Part B Child Count Metadata (2024-25):** - *Source:* U.S. Department of Education (EDPass).
   - *Description:* Contains state-level administrative policies indicating which disability categories (e.g., Hearing Impairment, Autism) and environments are utilized.
   - *Status:* We have acquired the official 2024-25 metadata schemas (Files 5002/5003).


### Data Integration Strategy
The datasets will be integrated using a relational model with **"State Name"** and **"Reporting Year"** as primary join keys. We will transform the Census "wide" format into a "tidy" long format to facilitate seamless merging with the IDEA student counts.

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
| Milestone | Task | Lead | Due Date |
| :--- | :--- | :--- | :--- |
| **Milestone 2** | Project Plan and GitHub Release (`project-plan` tag) | Team | March 10 |
| **Acquisition** | Scripting data intake and integrity verification | [Name] | March 20 |
| **Milestone 3** | Submit Interim Status Report (~1500 words) | Team | March 31 |
| **Integration** | Merging Census and IDEA datasets | Team | April 10 |
| **Automation** | Finalizing the end-to-end Snakemake workflow | [Name] | April 20 |
| **Milestone 4** | Final Project Submission | Team | May 03 |

## Constraints and Gaps
* **Missing Data (ELSEC 2024)**: We identified that the ELSEC 2024 summary tables contain missing data for certain states. We will address this by:
    1. Cross-referencing missing states with the ACS S1901 table to ensure demographic coverage.
    2. Using the Census Bureau's master API to retrieve specific state data that might be absent from the Excel summary tables.
    3. Documenting any states that must be excluded from final correlation analysis due to insufficient fiscal reporting.
* **Gaps**: Further research into Workflow Automation is required to ensure a robust, reproducible pipeline.
