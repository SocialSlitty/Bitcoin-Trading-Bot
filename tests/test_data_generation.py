
import unittest
import numpy as np
import pandas as pd
from src.bitcoin_sim import SimConfig, generate_synthetic_data

class TestDataGeneration(unittest.TestCase):
    def test_output_structure(self):
        config = SimConfig(days=100)
        df = generate_synthetic_data(config)

        # Check columns
        expected_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        self.assertListEqual(list(df.columns), expected_columns)

        # Check length
        self.assertEqual(len(df), 100)

        # Check types
        self.assertTrue(np.issubdtype(df["Close"].dtype, np.number))
        self.assertTrue(np.issubdtype(df["Volume"].dtype, np.number))

        # Check logic: High >= Low, High >= Open, High >= Close, Low <= Open, Low <= Close
        # Allow small floating point errors?
        # Using numpy vectorized checks
        self.assertTrue(np.all(df["High"] >= df["Low"]))
        self.assertTrue(np.all(df["High"] >= df["Open"]))
        self.assertTrue(np.all(df["High"] >= df["Close"]))
        self.assertTrue(np.all(df["Low"] <= df["Open"]))
        self.assertTrue(np.all(df["Low"] <= df["Close"]))

    def test_reproducibility(self):
        config1 = SimConfig(days=50, seed=123)
        df1 = generate_synthetic_data(config1)

        config2 = SimConfig(days=50, seed=123)
        df2 = generate_synthetic_data(config2)

        pd.testing.assert_frame_equal(df1, df2)

if __name__ == "__main__":
    unittest.main()
