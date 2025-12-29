import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import generate_synthetic_data, SimConfig

class TestDataGeneration(unittest.TestCase):
    def test_output_structure(self):
        config = SimConfig(days=100)
        df = generate_synthetic_data(config)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), config.days)

        expected_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        for col in expected_columns:
            self.assertIn(col, df.columns)

    def test_output_values_sanity(self):
        config = SimConfig(days=100)
        df = generate_synthetic_data(config)

        # High should be >= Open and Close
        self.assertTrue((df["High"] >= df["Open"]).all())
        self.assertTrue((df["High"] >= df["Close"]).all())

        # Low should be <= Open and Close
        self.assertTrue((df["Low"] <= df["Open"]).all())
        self.assertTrue((df["Low"] <= df["Close"]).all())

        # Volume should be positive
        self.assertTrue((df["Volume"] >= 0).all())

        # Prices should be positive (unless extreme volatility drives them to 0, but unlikely with these params)
        self.assertTrue((df["Close"] > 0).all())

if __name__ == "__main__":
    unittest.main()
