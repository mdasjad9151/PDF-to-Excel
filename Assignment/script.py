import os
import re
import fitz  # PyMuPDF
import pandas as pd
from google import genai
from dotenv import load_dotenv


load_dotenv()
# META Data for this project
API_KEY = os.getenv("GEMINI_API_KEY")
print(API_KEY)

PDF_PATH = "input/sample PDF.pdf"
print(PDF_PATH)
OUTPUT_DIR = "reports/"
MODEL_NAME = "models/gemini-1.5-flash"  

# initialize gemini setup
client = genai.Client(api_key=API_KEY)



def extract_pdf_sections(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Split based on report heading
    reports = full_text.split("THE LONDON CLINIC PATHOLOGY REPORT")
    # print(reports)
    return [r.strip() for r in reports if r.strip()]

def extract_patient_name(text):
    surname = re.search(r"Surname\s+([A-Z\s]+?)(?:\n|$)", text)
    forename = re.search(r"Forename\s+([A-Z\s]+?)(?:\n|$)", text)

    if surname and forename:
        fn = ' '.join(forename.group(1).strip().split())  # Remove extra spaces/newlines
        ln = ' '.join(surname.group(1).strip().split())
        return f"{fn.title().replace(' ', '_')}_{ln.title().replace(' ', '_')}"
    
    return "Unknown_Patient"
def ask_gemini_for_table(text):
    prompt = f"""
You are a medical assistant. Below is a pathology report text from a PDF. Extract a table with the following columns:
[Test Name, Value, Units, Reference Range]. Only include medical test results. Don't include any headers or extra info.

Report:
{text}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

def parse_table_and_save(response_text, filename):
    lines = response_text.strip().split("\n")
    rows = []

    for line in lines:
        # remove header and separator lines
        if re.match(r"^\|?\s*-+\s*\|", line) or "Test Name" in line:
            continue
        # Parse only valid table rows
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 3:
            while len(parts) < 4:  # pad missing columns
                parts.append("")
            rows.append(parts[:4])

    # Write to Excel only if valid rows exist
    if rows:
        df = pd.DataFrame(rows, columns=["Test", "Value", "Units", "Reference Range"])
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, f"{filename}.xlsx")
        df.to_excel(file_path, index=False)
        print(f"Saved: {file_path}")
    else:
        print(f"No valid table rows found for {filename}")


# --- MAIN ---
def process_pdf(pdf_path):
    reports = extract_pdf_sections(pdf_path)
    for report in reports:
        patient_name = extract_patient_name(report)
        response_text = ask_gemini_for_table(report)
        print(response_text)
        parse_table_and_save(response_text, patient_name)
        print(patient_name)

# --- RUN ---
if __name__ == "__main__":
    process_pdf(PDF_PATH)
