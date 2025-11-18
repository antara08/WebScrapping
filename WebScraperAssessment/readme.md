# 🧩 Web Scraping Technical Assessment (Selenium)

## Overview

This assessment evaluates your ability to design and implement a **Selenium-based web scraping workflow**. You will build a Python script that scrapes product data from the **LCBO website**, focusing on **wine listings** and **store availability**.

You will demonstrate:

- Selenium navigation and element selection
- Structured data extraction
- Data export (Excel/CSV)
- Clear and maintainable code structure

---

## 🕸️ Scraping Target

**Base URL:**  
`https://www.lcbo.com/en/products/wine/red-wine#t=clp-products-wine-red_wine&sort=relevancy&layout=card`

Your script must:

1. Navigate to the LCBO **Red Wine collection** page.
2. **Locate all wine listing cards** on the page.
3. **Extract the link (URL)** to each individual wine’s **detail page**.
4. Store all detail-page URLs in a list or collection for later iteration.

---

## 🍷 Wine Detail Extraction

For each wine’s **detail page**:

- Capture all key details (name, type, brand, price, sweetness, etc.) as described in the assessment.
- Store each record in a structured format (e.g., dictionary or dataframe).

Then, for each wine:

1. **Navigate to the “Availability” tab** or **store availability section**.
2. Extract all **store-level availability details**, including:
   - **Store name**
   - **City**
   - **Address**
   - **Quantity available**

---

## 📊 Data Output

### Option 1 — Excel Workbook

Create an Excel file (`wine_data.xlsx`) with **two sheets**:

1. `Wines` — wine-level details
2. `Availability` — store-level stock data

### Option 2 — CSV Files

If Excel libraries (e.g., `openpyxl`) are unavailable:

- Output two CSV files:
  - `wines.csv`
  - `availability.csv`

---

## ⚙️ Technical Requirements

| Requirement        | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| **Language**       | Python 3.x                                                           |
| **Libraries**      | Selenium (ChromeDriver preferred), Pandas, OpenPyXL (optional)       |
| **Execution**      | Script should be runnable via command line (`python scrape_lcbo.py`) |
| **Output**         | Saved data in local directory as `.xlsx` or `.csv`                   |
| **Code Quality**   | Organized, commented, and modular structure                          |
| **Error Handling** | Graceful handling of missing elements, navigation errors, etc.       |

---

## 🧠 Evaluation Criteria

| Category            | Description                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| **Correctness**     | Does the scraper extract and store all required details?               |
| **Code Structure**  | Are functions, loops, and variable names clear and maintainable?       |
| **Use of Selenium** | Are elements located reliably (e.g., `find_element`, `WebDriverWait`)? |
| **Data Output**     | Are both sheets (or CSVs) correctly formatted and complete?            |
| **Stability**       | Does the script handle pagination, delays, or missing data robustly?   |

---

## 🚀 Suggested Enhancements (Optional)

- Handle **pagination** to scrape multiple result pages.
- Include a **progress log** (via `print` or logging module).
- Implement **timeouts and retries** for reliability.
- Add **CLI arguments** (e.g., wine type filter or output file path).

---
