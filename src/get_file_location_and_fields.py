"""This function takes a JSON string containing:
- the S3 location of the required CSV file for obfuscation,
- the names of the fields that are required to be obfuscated,
and converts them to python elements."""

import json

def get_file_location_and_fields(loc_and_fields_string):
    try:
        data = json.loads(loc_and_fields_string)
        file_path = data['file_to_obfuscate']
        pii_fields = data['pii_fields']
        return file_path, pii_fields
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ValueError("Invalid JSON input or missing 'file_to_obfuscate'/'pii_fields' keys") from e