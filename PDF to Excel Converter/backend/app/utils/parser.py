import re

# def parse_statement_text(text):
#     lines = text.split('\n')
#     data = []

#     for line in lines:
#         # Skip empty or short lines
#         if len(line.strip()) < 10:
#             continue

#         # Simple pattern: date followed by description and amounts
#         match = re.match(r'^(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,\.]*)\s+([\d,\.]*)\s+([\d,\.]*)$', line)
#         if match:
#             date, desc, debit, credit, balance = match.groups()
#             data.append({
#                 'Date': date,
#                 'Description': desc,
#                 'Debit': debit,
#                 'Credit': credit,
#                 'Balance': balance
#             })
    
#     return data


def parse_statement_text(text):
    data = []
    for line in text.splitlines():
        line = line.strip()
        if len(line) < 6:
            continue

        # Regex pattern:
        # Date: Jan 16 (3 letters + space + 1-2 digits)
        # Description: anything non-greedy until the amounts
        # Debit and Credit: numbers with commas and dots
        # Optional CR/DR indicator at end
        pattern = re.compile(
            r'^([A-Z][a-z]{2}\s+\d{1,2})\s+(.+?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s*(CR|DR)?$'
        )

        match = pattern.match(line)
        if match:
            date = match.group(1)
            description = match.group(2)
            debit = match.group(3)
            credit = match.group(4)
            indicator = match.group(5) if match.group(5) else ''

            data.append({
                'Date': date,
                'Description': description,
                'Debit': debit,
                'Credit': credit,
                'Balance': indicator  # Put CR/DR in balance or add a separate field
            })
        else:
            # Fallback: treat line as description only
            data.append({
                'Date': '',
                'Description': line,
                'Debit': '',
                'Credit': '',
                'Balance': ''
            })

    return data