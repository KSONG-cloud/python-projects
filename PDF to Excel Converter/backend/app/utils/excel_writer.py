from openpyxl import Workbook
import pandas as pd
import re





def save_to_excel(text_data, excel_path):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Extracted Data"

        # Write header
        headers = ['Date', 'Description', 'Debit', 'Credit', 'Balance']
        ws.append(headers)

        # # Clean and split lines
        # lines = [line.strip() for line in text_data.splitlines() if line.strip()]


        # # Split by lines and write each line in a row
        # for line in lines:
        #     # Naive example: match lines starting with a date like "Jul 14"
        #     if re.match(r'^[A-Z][a-z]{2}\s+\d{1,2}', line):
        #         # Split the line into parts
        #         parts = re.split(r'\s{2,}', line)  # Split on 2+ spaces
        #         if len(parts) >= 5:
        #             date = parts[0]
        #             description = parts[1]
        #             debit = parts[2] if parts[2] else ''
        #             credit = parts[3] if parts[3] else ''
        #             balance = parts[4]
        #             ws.append([date, description, debit, credit, balance])
        #         else:
        #             # fallback: put everything in one row
        #             ws.append([line])
        #     else:
        #         # Probably a continuation of description or irrelevant
        #         ws.append([line])

        for entry in text_data:
            ws.append([
                entry.get('Date', ''),
                entry.get('Description', ''),
                entry.get('Debit', ''),
                entry.get('Credit', ''),
                entry.get('Balance', '')
            ])


        wb.save(excel_path)
        return excel_path
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return None