import os
import boto3
from moto import mock_aws
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from src.read_file_data import read_file_data

@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"

@mock_aws
class TestReadFileData:
    def test_gets_file_and_reads_data(self):
        # ARRANGE
        s3 = boto3.client("s3")
        s3.create_bucket(
            Bucket="my_ingestion_bucket", CreateBucketConfiguration={"LocationConstraint":
                                                    "eu-west-2"}
            )
        sample_csv_data = """student_id,name,course,graduation_date,email_address
        1234,John Smith,Software,2024-03-31,j.smith@email.com
        """

        s3.put_object(Bucket="my_ingestion_bucket", Key="new_data/file1.csv", Body=sample_csv_data)
        
        file_path = "s3://my_ingestion_bucket/new_data/file1.csv"

        # ACT
        file_df = read_file_data(file_path)

        # ASSERT
        expected_df = pd.DataFrame([{
        "student_id": 1234,
        "name": "John Smith",
        "course": "Software",
        "graduation_date": "2024-03-31",
        "email_address": "j.smith@email.com"
        }])

        expected_df = expected_df[file_df.columns]

        assert_frame_equal(file_df.reset_index(drop=True), expected_df.reset_index(drop=True))
