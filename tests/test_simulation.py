import unittest
import sys
import os
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import generate_synthetic_data, calculate_indicators, run_simulation, SimConfig

class TestSimulation(unittest.TestCase):
    def test_generate_synthetic_data_shape(self):
        days = 100
        config = SimConfig(days=days)
        df = generate_synthetic_data(config)

        self.assertEqual(len(df), days)
        expected_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_generate_synthetic_data_determinism(self):
        days = 50
        config = SimConfig(days=days, seed=123)
        df1 = generate_synthetic_data(config)
        df2 = generate_synthetic_data(config)

        pd.testing.assert_frame_equal(df1, df2)

    def test_simulation_flow(self):
        # Run the full pipeline
        config = SimConfig(days=300) # Enough for warm up
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)

        final_value, trades, ledger = run_simulation(df, config)

        self.assertIsInstance(final_value, float)
        self.assertIsInstance(trades, list)
        self.assertIsInstance(ledger, pd.DataFrame)

    def test_indicator_calculation(self):
        config = SimConfig(days=50)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)

        self.assertIn("EMA_7", df.columns)
        self.assertIn("SMA_30", df.columns)
        self.assertIn("SMA_200", df.columns)
        self.assertIn("Vol_SMA_10", df.columns)

if __name__ == "__main__":
    unittest.main()
