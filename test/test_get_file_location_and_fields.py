from src.get_file_location_and_fields import get_file_location_and_fields
import pytest


class TestGetFileAndLocationData:
    def test_get_file_location_and_fields_data(self):
        # ARRANGE
        test_file_loc_json = """{
            "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
            "pii_fields": ["name", "email_address"]
        }
        """

        # ACT
        file_path, pii_fields = get_file_location_and_fields(
            test_file_loc_json
            )

        # ASSERT
        assert file_path == "s3://my_ingestion_bucket/new_data/file1.csv"
        assert pii_fields == ["name", "email_address"]

    def test_handle_erroneous_json_input(self):
        # ARRANGE
        test_file_loc_json = """{
            "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv"
        }
        """

        # ACT & ASSERT
        with pytest.raises(ValueError):
            file_path, pii_fields = get_file_location_and_fields(
                test_file_loc_json
                )
