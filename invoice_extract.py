import os
import PyPDF2
import re
import csv

def extract_line_items(pdf_path):
    line_items = []

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            print(f"Page {page_num + 1} text:\n{text}")
            # define regex pattern based on invoice format
            # ... multiline flag to match from start of line: (?m)^ 
            # ... end of line flag in multiline or string: $
            # ... tab separated look-ahead: (?<=\t)(.*,.*?)(?=\t)
            # ... currency amount: d{1,3}(?:,
            pattern = r'Item.*$'

            matches = re.findall(pattern, text)

            for match in matches:
                line_items.append(match)

    return line_items

def save_to_csv(line_items, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # write header if needed: csv_writer.writerow(['Column1', 'Column2', ...])

        for item in line_items:
            # extracted line items might need further processing based on invoice
            # possibly split, format, or clean data before writing to CSV
            csv_writer.writerow([item])

def process_pdfs_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)

            items = extract_line_items(pdf_path)

            output_csv = os.path.splitext(pdf_path)[0] + '_output.csv'
            save_to_csv(items, output_csv)

# run
pdf_directory = 'A-invoices'
process_pdfs_in_directory(pdf_directory)
