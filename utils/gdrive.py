import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def create_sheet_and_share(data_dict, email_to_share):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = os.getenv("GOOGLE_CREDS_JSON", "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet = client.create("F1 Standings")
    sheet.share(email_to_share, perm_type="user", role="writer")
    worksheet = sheet.get_worksheet(0)

    print("Received data_dict:", data_dict)
    print("Sharing with:", email_to_share)
    
    parsed_rows = []
    for row in data_dict:
        if isinstance(row, str):
            parsed_rows.append(json.loads(row))
        else:
            parsed_rows.append(row)

    print("After Parsed_rows:", parsed_rows)

    if not parsed_rows:
        raise ValueError("No data provided to populate the sheet.")

    headers = list(parsed_rows[0].keys())
    worksheet.append_row(headers)

    for row in parsed_rows:
        worksheet.append_row(list(row.values()))
    
    print("successfully Processed", sheet.url)

    return sheet.url
