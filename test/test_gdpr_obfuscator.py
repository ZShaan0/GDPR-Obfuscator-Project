import os
import boto3
from moto import mock_aws
import pytest
from src.gdpr_obfuscator import gdpr_obfuscator


@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
class TestGDPRObfuscator:
    def test_GDPR_obfuscator_successfully_combines_util_functions(self):
        # ARRANGE
        s3 = boto3.client("s3")
        s3.create_bucket(
            Bucket="my_ingestion_bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        sample_csv_data = """id,name,course,grad_date,email
        1234,John Smith,Software,2024-03-31,j.smith@email.com
        """

        s3.put_object(
            Bucket="my_ingestion_bucket",
            Key="new_data/file1.csv",
            Body=sample_csv_data
        )

        location_and_fields_json_string = """{
            "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
            "pii_fields": ["name", "email"]
        }
        """

        expected_data_body = (
            "id,name,course,grad_date,email\n"
            "1234,***,Software,2024-03-31,***\n"
        ).encode("utf-8")

        # ACT
        obfuscated_data_body = gdpr_obfuscator(location_and_fields_json_string)

        # ASSERT
        assert obfuscated_data_body == expected_data_body
