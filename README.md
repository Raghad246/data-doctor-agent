# Data Doctor Agent

A multi-agent system for data quality analysis and automated data cleaning using CrewAI.

## Project Idea

The project takes raw CSV sales data, analyzes its quality, detects issues, and then performs safe and consistent cleaning operations.

Workflow:

Raw CSV Data  
↓  
Data Quality Analyst  
↓  
Quality Assessment  
↓  
Data Cleaning Specialist  
↓  
Cleaned CSV + Cleaning Report

## Agents

### Data Quality Analyst
Responsible for:
- Detecting missing values
- Detecting duplicate rows
- Detecting invalid ages and dates
- Detecting inconsistent city names
- Detecting outliers in `order_amount`

### Data Cleaning Specialist
Responsible for:
- Removing duplicate rows
- Filling missing numeric values
- Correcting invalid ages
- Standardizing city names
- Handling missing cities
- Converting invalid dates
- Preserving outliers
- Generating the final cleaned dataset and report

## Technologies

- CrewAI
- Python
- Pandas
- Ollama
- Llama

## Output Files

- `cleaned_sales_data.csv`
- `cleaning_report.md`

## Running

```bash
crewai run
