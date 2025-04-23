"""This function takes a dataframe and pii fields,

pd.DataFrame([{
        "student_id": 1234,
        "name": "John Smith",
        "course": "Software",
        "graduation_date": "2024-03-31",
        "email_address": "j.smith@email.com"
        }])
"pii_fields": ["name", "email_address"]

and obfuscates the pii data in the dataframe"""

import pandas as pd

def obfuscate_data(file_df, pii_fields):
    # itertate through pii columns
    for field in pii_fields:
        if field in file_df.columns:
            # Mask each value to obfuscate
            file_df[field] = file_df[field].apply(lambda x: "***")
    return file_df