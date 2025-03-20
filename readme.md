# Product Recommendation Pipeline

## Installation
```bash
pip install -r requirements.txt 
```
## Usage
```bash
python src/main.py \
  --input <path/to/input_data.xlsx> \
  --output <path/to/output_recommendations.csv> \
  [--top-n NUM] [--top-ratio RATIO]
```

**Parameters**    
--input: Path to input Excel file (required)   
--output: Path to save recommendations CSV (required)   
--top-n: Exact number of clients to recommend (mutually exclusive with --top-ratio)   
--top-ratio: Fraction of qualified clients to recommend (default: 0.15)   

**Example Usage**
```bash
python src/main.py \
  --input data/DataScientist_CaseStudy_Dataset.xlsx \
  --output outputs/recommendation.csv \
  --top-ratio 0.1
```

## Repository Structure 
├── data/  # Raw datasets, DataScientist_CaseStudy_Dataset.xlsx   
├── outputs/  # list of clients with product to target,  product_recommendations.csv   
├── models/ # Saved model binaries   
├── encoders/ # Saved encoders   
├── scaler/ # Saved scaler   
├── Client_propensity_study.ipynb  # notebook for data analysis, and model building, models, encoders, and scalers are saved to respective directory in this notebook   
├── Report.md # report on approach and results analysis   
└── README.md # This document   

# Marketing Propensity Modeling & Revenue Optimization  

## Overview  
This project predicts client purchase propensity and revenue potential to optimize marketing outreach. It combines classification (purchase likelihood) and regression (revenue prediction) models, followed by a greedy algorithm to prioritize high-value targets.

---

## Project Flow & Approach Summary  

**Data Processing**
1. Data Cleaning 
2. Train-Test Split
3. Feature Engineering

**Modeling**
1. Propensity Models for each product (Bineary Classification)
2. Revenue Models for each product (Regression)  

**Recommendation Algorithm**   
Greedy algorithm on expected revenue for each product calculated from predicted propensity and revenue. 


<!-- ## 1. Data Processing  
- ​**Cleaning**:  
  - Removed duplicate records and merged multiple data sources into a unified dataset.  
- ​**Feature Engineering**:  
  - ​**Account Balances**: Replaced negative values with `0`, applied log transformation to reduce right-skew.  
  - ​**Count Features**: Standardized using z-score scaling.  
  - ​**Categorical Variables**: One-hot encoded the `Sex` column.  
- ​**Data Splitting**:  
  - Separated unlabeled test data (clients without purchase outcomes).  
  - Split remaining data into 80% training and 20% validation sets (stratified by class).  

---

## 2. Modeling  
### ​**Propensity Models (Classification)**  
- ​**Objective**: Predict purchase likelihood for 3 products (`Sale_CC`, `Sale_MF`, `Sale_CL`).  
- ​**Approach**:  
  - Tested ​**LightGBM** (grid search, AUC-optimized) vs. ​**logistic regression** (baseline).  
  - ​**Key Tradeoff**: LightGBM achieved higher AUC (0.78 vs. 0.76), but logistic regression offered better precision-recall balance.  
  - ​**Final Choice**: Logistic regression for operational simplicity and balanced performance.  

### ​**Revenue Models (Regression)**  
- ​**Objective**: Predict revenue for clients flagged as likely purchasers.  
- ​**Approach**:  
  - Compared ​**LightGBM Regressor** (grid search) with ​**linear regression** (baseline).  
  - ​**Key Insight**: LightGBM slightly outperformed linear regression (MAE: 12.8 vs. 13.1, R²: 0.72 vs. 0.71) but was less interpretable.  
  - ​**Final Choice**: Linear regression for stable, interpretable predictions.  

---

## 3. Recommendation Algorithm  
- ​**Expected Revenue**:  
  - Calculated as `P(Propensity) × Predicted Revenue` for each (client, product) pair.  
- ​**Targeting Workflow**:  
  1. ​**Thresholding**: Excluded clients with propensity < 0.5.  
  2. ​**Ranking**: Sorted remaining pairs by descending expected revenue.  
  3. ​**Selection**: Greedily picked top pairs, ensuring:  
     - Maximum 1 product recommendation per client.  
     - Batch execution within predefined client quotas.  

**Design Philosophy**: Prioritized model interpretability and operational simplicity, balancing performance with deployment practicality.   -->