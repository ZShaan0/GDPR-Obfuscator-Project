"""This function takes a dataframe 
and converts it to byte-stream representation of a file
which can be uploaded as a CSV file to s3 storage
using boto3 putObject."""

import pandas as pd
from io import StringIO

def output_data_body(obfuscated_df):
    buffer = StringIO()
    obfuscated_df.to_csv(buffer, index=False)
    data_body = buffer.getvalue().encode('utf-8')
    return data_body