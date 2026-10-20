import unittest

import polars as pl

from src.clean_data import filter_offensive_plays


class TestFilterOffensivePlays(unittest.TestCase):

    def test_excludes_non_offensive_plays(self):
        # Arrange: Create a small, controlled dataset.
        plays = pl.DataFrame({
            "record_id": ["A", "B", "C", "D", "E", "F"],
            "play_type": [
                "run", "pass", "run", "pass", "run", "kickoff"
            ],
            "qb_kneel": [0, 0, 1, 0, 0, 0],
            "qb_spike": [0, 0, 0, 1, 0, 0],
            "two_point_attempt": [0, 0, 0, 0, 1, 0],
        })

        # Act: Apply our filtering function.
        result = filter_offensive_plays(plays)

        # Assert: Only the expected records remain.
        self.assertEqual(
            result["record_id"].to_list(),
            ["A", "B"]
        )

    def test_missing_indicator_values(self):
        plays = pl.DataFrame({
            "record_id": ["A", "B"],
            "play_type": ["run", "pass"],
            "qb_kneel": [None, 0],
            "qb_spike": [0, None],
            "two_point_attempt": [0, 0],
        })

        result = filter_offensive_plays(plays)

        print("Records surviving null filtering:",
            result["record_id"].to_list())

        self.assertEqual(
        result["record_id"].to_list(),
        ["A", "B"]
)