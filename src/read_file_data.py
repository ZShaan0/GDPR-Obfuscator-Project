"""This function takes the S3 location of the CSV file to be obfuscated,
and reads the file data into a pandas dataframe."""

import boto3
import pandas as pd
from io import StringIO


def read_file_data(file_path):
    # Parse S3 file_path
    s3_bucket_and_key = file_path.replace("s3://", "")
    s3_parts = s3_bucket_and_key.split("/", 1)
    bucket = s3_parts[0]
    key = s3_parts[1]

    # Init boto3 client
    s3 = boto3.client("s3")

    # Read data from S3 into memory
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")

    # Load into pandas DataFrame from memory
    df = pd.read_csv(StringIO(content))
    return df
