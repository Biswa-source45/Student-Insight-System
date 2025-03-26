# Project Documentation: Student-Insight System

## Introduction

The **Student-Insight System** is a Tkinter-based Python application designed to analyze student performance based on class test scores and internal marks. Users can upload CSV files containing student data, search for specific students using their registration number, academic year, and department, and visualize performance trends.

## Features

- Upload Class Test and Internal Marks data (CSV format).
- Analyze individual student performance.
- Display scores in a user-friendly interface.
- Generate performance comparison graphs.
- Download analysis as a PDF report.
- Reset and clear input fields.
- Exit application securely.

## System Requirements

- Python 3.x
- Required Libraries:
  - `tkinter`
  - `matplotlib`
  - `fpdf`
  - `csv`
  - `os`

### Install All Required Libraries

Run the following command to install all necessary dependencies:

```bash
pip install fpdf matplotlib
```

## Installation & Setup

1. Ensure Python 3.x is installed.
2. Install dependencies using:
   ```bash
   pip install fpdf matplotlib
   ```
3. Run the application:
   ```bash
   python mainIndex.py
   ```

## How to Use

### Upload CSV Files

- Click on "Upload File" for **Class Test** and **Internal Marks**.
- Select the respective CSV file.
- A confirmation message will be displayed.

### Analyze Student Data

- Enter **Registration Number**, **Academic Year**, and **Department**.
- Click on the "Analyze" button.
- The system will fetch records and display results.
- A performance graph will be shown if data is available.

### Download Report

- Click the "Download PDF" button to save the student’s analysis as a **PDF file**.

### Reset & Exit

- Click "Reset" to clear all inputs.
- Click "Exit" to close the application.

## CSV File Format

The application processes two CSV files:

1. **Class Test Scores (Example CSV Format):**

   | Regno | AccYear | Dept | Subject1 | Subject2 | ... |
   | ----- | ------- | ---- | -------- | -------- | --- |
   | 12345 | 2024    | CSE  | 78       | 85       | ... |

2. **Internal Marks (Example CSV Format):**

   | Regno | AccYear | Dept | Subject1 | Subject2 | ... |
   | ----- | ------- | ---- | -------- | -------- | --- |
   | 12345 | 2024    | CSE  | 80       | 90       | ... |

## Future Enhancements

- Add database support for long-term storage.
- Implement student login for personalized reports.
- Include predictive analysis using AI.

## User Manual

### Getting Started

1. Open the application by running `python mainIndex.py`.
2. Ensure the required CSV files are available.
3. Follow on-screen instructions for uploading and analysis.

### Common Issues & Solutions

1. **File Upload Issue:** Ensure the file format is CSV.
2. **Data Not Found:** Double-check registration number, academic year, and department.
3. **Graph Not Displayed:** Ensure valid numeric data is present in the CSV.

## Contact & Support

For issues or suggestions, reach out via GitHub issues or email.
[biswapvt506@gmail.com](biswapvt506@gmail.com)

---

### 📌 Design & Developed By: [Biswabhusan Sahoo](https://www.linkedin.com/in/biswabhusan-sahoo-22b704292/?trk=opento_sprofile_topcard)
