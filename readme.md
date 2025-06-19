# 🧬 Gemini-Powered Pathology Report Extractor

This project uses the **Google Gemini API (via `google.genai.Client`)** to intelligently extract structured lab test data from a multi-patient PDF pathology report. Each patient's report is saved as a clean, individual Excel file using the patient’s name.

---

## Features

- **PDF to Structured Excel** — Converts unstructured lab reports into clean tables.
- **Automatic Patient Detection** — Extracts patient names from each section of the PDF.
- **One Report Per File** — Saves each patient’s test results in a separate `.xlsx` file.
- **Gemini-Powered Intelligence** — Uses Google Gemini 1.5 Flash to extract and clean data.
- **Preprocessing for Accuracy** — Handles tricky values like percentages and units.

---

##  Project Structure

```
pdf-to-excel/
    ├── readme.md
    ├── requirements.txt
    └── Assignment/
        ├── script.py
        ├── input/
        └── reports/
            ├── Lynne_Christine_Evans.xlsx
            └── Test_Patient.xlsx
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt

```
### 2.  Set Up API Key
Create a .env file with your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Add Your PDF
Place your PDF report (with multiple patient entries) into the input/ folder, for example:

```
input/sample PDF.pdf

```

### Run script.py

```bash
python main.py

```