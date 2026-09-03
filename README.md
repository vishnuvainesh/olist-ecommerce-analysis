# 🛒 Olist E-Commerce Marketplace Analysis

## 📌 Project Overview

This project is an end-to-end **E-Commerce Data Analytics and Business Intelligence project** based on the **Olist Brazilian E-Commerce Public Dataset**.

The objective is to analyze marketplace performance across **sales, customers, sellers, products, delivery operations, payments, and customer reviews**, and convert the analysis into meaningful business insights and actionable recommendations.

The project combines:

- Python
- Pandas
- SQL
- MySQL
- Plotly
- Statistical Analysis
- Streamlit
- Git/GitHub

The final outcome is an interactive **Streamlit Business Intelligence Dashboard** that presents KPIs, visualizations, analytical findings, and business recommendations.

---

# 🎯 Business Objective

The main objective of this project is to understand the performance of the Olist marketplace and answer important business questions such as:

- How much revenue does the marketplace generate?
- How many orders and customers does the marketplace have?
- How does revenue change over time?
- Which product categories generate the most revenue?
- Which sellers perform the best?
- Which products have the highest sales volume?
- Where are customers geographically concentrated?
- What is the average order value?
- How many customers make repeat purchases?
- What is the average delivery time?
- How many orders are delayed?
- Which locations experience longer delivery times?
- Does delivery performance affect customer satisfaction?
- Which product categories receive the highest ratings?
- What business actions can improve marketplace performance?

---

# 📊 Dataset

The project uses the **Olist Brazilian E-Commerce Public Dataset**.

The dataset contains **9 related tables** representing different aspects of the e-commerce marketplace.

## Dataset Tables

| Table | Description |
|---|---|
| Customers | Customer information and location |
| Geolocation | Brazilian ZIP-code geographic information |
| Orders | Order status and order timestamps |
| Order Items | Products purchased in each order |
| Order Payments | Payment and installment information |
| Order Reviews | Customer ratings and review information |
| Products | Product attributes |
| Sellers | Seller information |
| Category Translation | Portuguese-to-English product category translation |

---

# 🔄 Project Workflow

The project follows a structured end-to-end data analytics workflow.

## Step 1 — Understand the Business Problem

- Understand the marketplace business context
- Define business objectives
- Identify important business questions
- Determine the KPIs required for analysis

---

## Step 2 — Understand the Dataset & ER Diagram

- Understand all 9 tables
- Examine table structures
- Understand columns and data types
- Identify primary keys
- Identify foreign keys
- Understand relationships between tables
- Study the Entity Relationship Diagram
- Prepare a data dictionary

---

## Step 3 — Load Raw Data

The original Olist CSV files were loaded using **Pandas**.

The raw datasets are kept separately from the cleaned datasets to preserve the original source data.

---

## Step 4 — Data Quality Analysis

Data quality checks were performed before cleaning the datasets.

The analysis includes:

- Missing value analysis
- Duplicate record analysis
- Data type validation
- Invalid and inconsistent value checks
- Potential outlier identification
- Primary-key uniqueness checks
- Referential integrity considerations

---

## Step 5 — Data Cleaning & Preprocessing

The datasets were cleaned and prepared for analysis.

Major activities include:

- Handling missing values
- Correcting data types
- Removing unnecessary duplicates where applicable
- Standardizing values
- Preparing clean datasets
- Validating cleaned data
- Creating analysis-ready datasets

---

## Step 6 — Store Cleaned Data in MySQL

The cleaned datasets were integrated into a **MySQL database**.

Database used:

```text
olist_ecommerce
```

Python was used to establish the connection between the application and MySQL.

---

## Step 7 — SQL Business Analysis

SQL queries were developed to calculate important business KPIs and analytical metrics.

Examples include:

- Total Revenue
- Total Orders
- Total Customers
- Total Sellers
- Average Order Value
- Average Review Score
- Monthly Revenue
- Revenue by Category
- Sales by Location
- Repeat vs New Customers
- Top Customers
- Top Sellers
- Top Products
- Average Delivery Time
- On-Time vs Delayed Orders
- Delivery Performance by Location
- Delivery Delay vs Review Score
- Review Distribution
- Reviews by Category

---

## Step 8 — Exploratory Data Analysis

Exploratory Data Analysis was performed to understand marketplace patterns.

The analysis covers:

- Revenue trends
- Sales performance
- Product categories
- Customer distribution
- Customer spending
- Seller performance
- Product performance
- Geographic sales
- Delivery performance
- Customer reviews

---

## Step 9 — Statistical Analysis

Statistical analysis was performed to investigate relationships and patterns within the marketplace data.

The analysis helps understand relationships between operational and customer-related variables, particularly:

- Delivery performance
- Customer reviews
- Sales behavior
- Customer purchasing patterns

---

## Step 10 — Streamlit Dashboard

An interactive Streamlit dashboard was developed to present the analytical results.

The dashboard contains:

1. Overview
2. Sales
3. Customers
4. Sellers & Products
5. Delivery
6. Reviews
7. Executive Insights

---

## Step 11 — Final Business Insights & Recommendations

The final analytical results are converted into actionable business recommendations.

The recommendations focus on:

- Revenue growth
- Customer retention
- Delivery optimization
- Seller quality
- Customer satisfaction

---

# 📁 Project Structure

```text
project1_GUVI/
│
├── README.md
├── .gitignore
├── python.sql
│
├── data/
│   │
│   ├── raw/
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── product_category_name_translation.csv
│   │
│   └── cleaned/
│       ├── category_translation.csv
│       ├── customers.csv
│       ├── geolocation.gz
│       ├── orders.csv
│       ├── order_items.csv
│       ├── order_payments.csv
│       ├── order_reviews.csv
│       ├── products.csv
│       └── sellers.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_analysis.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_sql_analysis.ipynb
│   ├── 06_eda.ipynb
│   ├── 07_statistical_analysis.ipynb
│   ├── load_data.py
│   └── test_mysql.py
│
└── streamlit/
    ├── app.py
    ├── database.py
    ├── queries.py
    └── utils.py
```

> **Note:** The cleaned geolocation dataset is stored as `geolocation.gz` because the uncompressed geolocation CSV is very large.

---

# 🛠️ Technologies Used

## Programming & Data Analysis

- Python
- Pandas
- NumPy

## Database

- MySQL
- SQL
- MySQL Connector for Python

## Visualization

- Plotly
- Streamlit

## Statistical Analysis

- Descriptive statistics
- Relationship analysis
- Business-oriented statistical analysis

## Development

- Jupyter Notebook
- VS Code
- Git
- GitHub

---

# 🗄️ Database Integration

The project uses MySQL for storing cleaned datasets and performing business analysis.

Database:

```text
olist_ecommerce
```

Python connects to MySQL using environment variables instead of hardcoding credentials.

Example:

```python
import os
import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "olist_ecommerce")
    )
```

Database credentials should be stored locally in a `.env` file.

Example:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=olist_ecommerce
```

The `.env` file must **not** be uploaded to GitHub.

---

# 📈 SQL Analysis

SQL was used to perform business-level analysis directly from the MySQL database.

Important analytical queries include:

### Business Overview

- Total Revenue
- Total Orders
- Total Customers
- Total Sellers
- Average Order Value
- Average Review Score

### Sales Analysis

- Monthly Revenue
- Revenue by Category
- Category Performance
- Sales by Location

### Customer Analysis

- Customer Distribution
- Repeat vs New Customers
- Customer Spending
- Top Customers

### Seller & Product Analysis

- Top Sellers
- Top Selling Products
- Category Performance

### Delivery Analysis

- Average Delivery Time
- On-Time vs Delayed Orders
- Delivery by Location
- Delivery Delay vs Review Score

### Review Analysis

- Review Score Distribution
- Reviews by Category
- Rating vs Delivery

---

# 📊 Streamlit Dashboard

The Streamlit application provides an interactive business intelligence dashboard.

---

## 1. Overview

The Overview page provides a high-level summary of marketplace performance.

### KPIs

- Total Revenue
- Total Orders
- Total Customers
- Active Sellers
- Average Order Value
- Average Review Score

### Visualizations

- Monthly Revenue
- Top Categories
- Review Distribution

---

## 2. Sales

The Sales page focuses on marketplace revenue performance.

### Analysis

- Revenue Trend
- Category Economics
- Revenue by Category
- Geographic Sales

This page helps identify where revenue is concentrated.

---

## 3. Customers

The Customer Intelligence page focuses on customer behavior.

### Analysis

- Total Customers
- Repeat Customers
- Repeat Customer Rate
- Customer Distribution
- New vs Repeat Customers
- Customer Spending
- Highest-Value Customers

This helps understand customer retention and customer value.

---

## 4. Sellers & Products

This page evaluates seller and product performance.

### Analysis

- Total Sellers
- Leading Sellers
- Top Sellers
- Top-Selling Products
- Category Performance

This helps identify high-performing sellers and products.

---

## 5. Delivery

The Delivery page evaluates marketplace logistics.

### KPIs

- Average Delivery Time
- Delayed Orders

### Analysis

- On-Time vs Delayed Orders
- Delivery Time by Location
- Delivery Delay vs Review Score

This helps identify potential operational improvement areas.

---

## 6. Reviews

The Reviews page evaluates customer satisfaction.

### KPIs

- Average Review Score
- Five-Star Reviews

### Analysis

- Review Score Distribution
- Category Satisfaction
- Rating vs Delivery Performance

---

## 7. Executive Insights

The Executive Insights page provides a decision-focused summary.

It includes:

- Executive Scorecard
- Marketplace Scale
- Revenue Insights
- Customer Experience Insights
- Operational Insights
- Top Customers
- Top Sellers
- Top Products
- Recommended Focus Areas

---

# 💡 Business Insights

The analysis focuses on several major business areas.

## Revenue Insights

Revenue analysis identifies:

- Overall marketplace revenue
- Revenue trends over time
- High-performing categories
- Revenue concentration
- High-value sellers and products

These insights can help the business prioritize high-performing areas.

---

## Customer Insights

Customer analysis identifies:

- Customer distribution
- Repeat purchasing behavior
- Customer spending
- High-value customers
- Geographic concentration

This can help improve customer retention strategies.

---

## Seller Insights

Seller analysis identifies:

- High-volume sellers
- Revenue-generating sellers
- Seller performance differences
- Potential high-quality sellers

Seller performance should be evaluated using multiple metrics rather than sales volume alone.

---

## Product Insights

Product analysis identifies:

- Top-selling products
- High-volume products
- High-performing categories
- Product contribution to marketplace activity

---

## Delivery Insights

Delivery analysis evaluates:

- Average delivery duration
- Delayed orders
- Geographic delivery differences
- Relationship between delivery performance and customer ratings

Delivery performance is an important operational factor that can influence customer experience.

---

## Review Insights

Review analysis evaluates:

- Overall customer satisfaction
- Rating distribution
- Five-star reviews
- Category-level satisfaction
- Relationship between delivery and ratings

---

# 🚀 Business Recommendations

## 1. Focus on High-Performing Categories

Identify categories that consistently generate strong revenue and order volume.

Recommended actions:

- Prioritize high-performing categories
- Increase marketing activity
- Improve inventory planning
- Encourage seller participation in successful categories
- Develop category-specific promotions

---

## 2. Improve Customer Retention

Repeat customers are important for long-term marketplace value.

Recommended actions:

- Monitor repeat purchasing behavior
- Identify high-value customers
- Create loyalty campaigns
- Provide personalized offers
- Encourage repeat purchases
- Develop targeted promotional campaigns

---

## 3. Optimize Delivery Performance

Delivery delays should be monitored at both marketplace and geographic levels.

Recommended actions:

- Identify locations with longer delivery times
- Monitor delayed orders
- Improve logistics planning
- Improve seller fulfillment processes
- Track delivery performance regularly

---

## 4. Monitor Seller Quality

Seller performance should not be measured using sales volume alone.

Recommended actions:

- Compare seller revenue
- Compare order volume
- Monitor customer ratings
- Monitor delivery performance
- Identify consistently high-performing sellers
- Investigate sellers with high volume but poor customer satisfaction

---

## 5. Improve Customer Experience

Customer reviews should be analyzed together with operational performance.

Recommended actions:

- Investigate low-rated categories
- Identify sellers associated with poor ratings
- Analyze delivery delays
- Monitor customer feedback
- Improve problem areas affecting customer satisfaction

---

# 📦 Large Dataset Handling

The geolocation dataset is significantly larger than the other datasets.

Therefore, the cleaned geolocation dataset is compressed as:

```text
geolocation.gz
```

instead of uploading the large uncompressed CSV file.

This reduces repository size and makes the project easier to manage.

---

The application will connect to MySQL and display the interactive dashboard.

---

# 🧪 Testing & Validation

The project was tested across the major workflow stages.

Validation includes:

- Data quality checks
- Duplicate checks
- Primary-key uniqueness checks
- Data type validation
- SQL query testing
- MySQL connectivity testing
- Dashboard query validation
- Streamlit application testing
- Visualization validation
- Final business insight validation

---

# 📋 Project Deliverables

## 1. Source Code

Python notebooks and scripts for:

- Data understanding
- Data quality analysis
- Data cleaning
- EDA
- Statistical analysis
- SQL integration

---

## 2. SQL Integration

Includes:

- MySQL database
- Python-MySQL connection
- SQL business queries
- KPI calculations
- Business analysis queries

---

## 3. Streamlit Application

Interactive dashboard containing:

- KPIs
- Charts
- Tables
- Business insights
- Recommendations

---

## 4. Project Documentation

This README contains:

- Project objective
- Dataset description
- Project workflow
- Technologies
- Database integration
- Dashboard details
- Business insights
- Recommendations
- Setup instructions

---

## 5. Business Insights & Recommendations

The final analysis provides recommendations related to:

- Revenue growth
- Customer retention
- Delivery optimization
- Seller quality
- Customer satisfaction

---

## 6. Final Presentation

The project can be presented using the following structure:

1. Business Problem
2. Business Objectives
3. Dataset
4. ER Diagram
5. Data Understanding
6. Data Quality Analysis
7. Data Cleaning
8. MySQL Integration
9. SQL Analysis
10. Exploratory Data Analysis
11. Statistical Analysis
12. Streamlit Dashboard
13. Key Business Insights
14. Business Recommendations
15. Conclusion

---

# 🧠 Key Learning Outcomes

This project demonstrates practical experience in:

- Understanding business requirements
- Working with relational datasets
- Data quality analysis
- Data cleaning and preprocessing
- Feature engineering
- SQL analytics
- MySQL database integration
- Exploratory Data Analysis
- Statistical analysis
- Data visualization
- Streamlit dashboard development
- Business intelligence
- Insight generation
- Git/GitHub project organization

---

# 🏁 Conclusion

This project demonstrates a complete **end-to-end E-Commerce Data Analytics workflow**.

Raw Olist marketplace data was transformed through:

```text
Raw Data
    ↓
Data Understanding
    ↓
Data Quality Analysis
    ↓
Data Cleaning
    ↓
MySQL Integration
    ↓
SQL Business Analysis
    ↓
EDA
    ↓
Statistical Analysis
    ↓
Streamlit Dashboard
    ↓
Business Insights
    ↓
Recommendations
```

The final solution provides an interactive business intelligence dashboard that allows users to understand marketplace performance across:

- Sales
- Customers
- Sellers
- Products
- Delivery
- Reviews

The project demonstrates how data can be transformed into **actionable business intelligence and decision support**.

---

# 👨‍💻 Project

**Olist E-Commerce Marketplace Analysis**

**Technologies:** Python | Pandas | SQL | MySQL | Plotly | Streamlit | Git | GitHub

**Project Type:** E-Commerce Data Analytics & Business Intelligence
