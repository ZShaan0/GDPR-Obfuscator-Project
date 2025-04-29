import pandas as pd
from pandas.testing import assert_frame_equal
from src.obfuscate_data import obfuscate_data


class TestObfuscateData:
    def test_pii_data_is_obfuscated(self):
        # ARRANGE
        test_df = pd.DataFrame(
            [
                {
                    "student_id": 1234,
                    "name": "John Smith",
                    "course": "Software",
                    "graduation_date": "2024-03-31",
                    "email_address": "j.smith@email.com",
                }
            ]
        )

        pii_fields = ["name", "email_address"]

        # ACT
        obfuscated_df = obfuscate_data(test_df, pii_fields)

        # ASSERT
        expected_df = pd.DataFrame(
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

        expected_df = expected_df[obfuscated_df.columns]

        assert_frame_equal(
            obfuscated_df.reset_index(drop=True),
            expected_df.reset_index(drop=True)
        )
