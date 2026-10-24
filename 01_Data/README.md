# 01_Data — Data Layer

This folder contains all datasets used in the Customer Sales Intelligence Project.

## Folder Structure

01_Data/
├── raw/
├── cleaned/
└── README.md

## raw/

Contains the original datasets exactly as obtained from the source.

The raw data should not be manually modified.

Purpose:

- Preserve the original source data
- Maintain data integrity
- Allow reproducibility
- Provide a backup of the original dataset

## cleaned/

Contains datasets after data cleaning and preprocessing.

Typical cleaning activities may include:

- Removing duplicate records
- Handling missing values
- Correcting data types
- Standardizing column names
- Standardizing categorical values
- Handling invalid records
- Creating derived fields where appropriate

## Data Quality

Before using the data for SQL, Python, or Power BI, the following checks should be performed:

- Number of rows and columns
- Missing values
- Duplicate records
- Data types
- Unique values
- Invalid or inconsistent values
- Date ranges
- Numerical ranges
- Referential consistency

## Data Flow

Raw Data
   ↓
Data Quality Checks
   ↓
Data Cleaning
   ↓
Cleaned Data
   ↓
SQL / Python / Power BI

## Important Rule

The raw/ folder should contain the original source data without modification.

Any cleaning or transformation should be performed separately and documented.