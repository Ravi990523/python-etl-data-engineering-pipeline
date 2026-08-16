@'
# 🚀 End-to-End ETL Data Engineering Pipeline

An end-to-end Data Engineering project built with Python, Pandas, SQLAlchemy, PyMySQL, REST APIs, and MySQL.

The pipeline extracts data from external sources, validates and transforms the data, applies schema mapping and incremental processing, and loads new records into MySQL.

---

## 📌 Project Overview

This project demonstrates a modular ETL pipeline designed to process product data from a REST API.

### Source

- REST API
- CSV files

### Target

- MySQL Database

### Main ETL Flow

REST API / CSV  
↓  
Extract  
↓  
Schema Mapping  
↓  
Data Validation  
↓  
Transformation  
↓  
Watermark Filtering  
↓  
Incremental Loading  
↓  
MySQL  
↓  
Logging & Monitoring

---

## 🏗️ Architecture

```text
              REST API / CSV
                    |
                    v
             +-------------+
             |   Extract   |
             +-------------+
                    |
                    v
             +-------------+
             |   Schema    |
             |   Mapping   |
             +-------------+
                    |
                    v
             +-------------+
             | Validation  |
             +-------------+
                    |
                    v
             +-------------+
             | Transform   |
             +-------------+
                    |
                    v
             +-------------+
             |  Watermark  |
             |  Filtering  |
             +-------------+
                    |
                    v
             +-------------+
             | Incremental |
             |    Load     |
             +-------------+
                    |
                    v
             +-------------+
             |    MySQL    |
             +-------------+
                    |
                    v
             +-------------+
             |   Logging   |
             +-------------+