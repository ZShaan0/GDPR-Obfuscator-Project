import os
import boto3
from moto import mock_aws
import pytest
import pandas as pd
from src.output_data_body import output_data_body


@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
class TestOutPutDataBody:
    def test_output_is_a_byte_stream_representation_of_a_file(self):
        # ARRANGE
        test_df = pd.DataFrame(
            [
                {
                    "student_id": 1234,
                    "name": "***",
                    "course": "Software",
                    "graduation_date": "2024-03-31",
                    "email_address": "***",
                }
            ]
        )

        expected_data_body = (
            "student_id,name,course,graduation_date,email_address\n"
            "1234,***,Software,2024-03-31,***\n"
        ).encode("utf-8")

        # ACT
        obfuscated_data_body = output_data_body(test_df)

        # ASSERT
        assert obfuscated_data_body == expected_data_body

    def test_output_data_body_is_compatible_with_boto3_putobject(self):
        # ARRANGE
        test_df = pd.DataFrame(
            [
                {
                    "student_id": 1234,
                    "name": "***",
                    "course": "Software",
                    "graduation_date": "2024-03-31",
                    "email_address": "***",
                }
            ]
        )

        obfuscated_data_body = output_data_body(test_df)

        expected_fetched_data_body = (
            "student_id,name,course,graduation_date,email_address\n"
            "1234,***,Software,2024-03-31,***\n"
        ).encode("utf-8")

        s3 = boto3.client("s3")
        s3.create_bucket(
            Bucket="my_ingestion_bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        # ACT
        s3.put_object(
            Bucket="my_ingestion_bucket",
            Key="obfuscated_data/file1.csv",
            Body=obfuscated_data_body,
        )

        uploaded_object = s3.get_object(
            Bucket="my_ingestion_bucket", Key="obfuscated_data/file1.csv"
        )
        uploaded_content = uploaded_object["Body"].read()

        # ASSERT
        assert uploaded_content == expected_fetched_data_body
