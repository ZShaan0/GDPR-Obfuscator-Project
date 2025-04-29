"""This tool will be invoked by sending a JSON string containing:
- the S3 location of the required CSV file for obfuscation
- the names of the fields that are required to be obfuscated.
It fetches the data, obfuscates the required fields and
outputs a byte-stream body of the obfuscated data,
ready to be uploaded to s3 storage via boto3."""

from src.get_file_location_and_fields import get_file_location_and_fields
from src.read_file_data import read_file_data
from src.obfuscate_data import obfuscate_data
from src.output_data_body import output_data_body


def gdpr_obfuscator(loc_and_fields_string):
    # Parse the json string to get the required filepath and pii fields
    file_path, pii_fields = get_file_location_and_fields(loc_and_fields_string)

    # Read the data from s3 storage into a pandas dataframe
    raw_data_df = read_file_data(file_path)

    # Obfuscate the PII data
    obfuscated_data_df = obfuscate_data(raw_data_df, pii_fields)

    # Output the obfuscated data into a byte-stream body
    obfuscated_data_body = output_data_body(obfuscated_data_df)

    # Return the byte-stream body so that it can be uploaded to s3 storage
    return obfuscated_data_body
