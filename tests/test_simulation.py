
import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import generate_synthetic_data, calculate_indicators, run_simulation, SimConfig

class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.config = SimConfig(days=300, seed=42)
        self.df = generate_synthetic_data(self.config)
        self.df = calculate_indicators(self.df)
        self.df = self.df.dropna().reset_index(drop=True)

    def test_run_simulation_returns_valid_structure(self):
        final_value, trades_log, daily_ledger = run_simulation(self.df, self.config)

        self.assertIsInstance(final_value, float)
        self.assertIsInstance(trades_log, list)
        self.assertIsInstance(daily_ledger, pd.DataFrame)

        # Check trades_log structure
        if len(trades_log) > 0:
            trade = trades_log[0]
            self.assertIn("Date", trade)
            self.assertIn("Type", trade)
            self.assertIn("Price", trade)

            # Check Date format is YYYY-MM-DD
            date_str = trade["Date"]
            self.assertIsInstance(date_str, str)
            self.assertRegex(date_str, r"^\d{4}-\d{2}-\d{2}$")

    def test_simulation_consistency(self):
        # Run twice with same input, should get same result
        res1 = run_simulation(self.df, self.config)
        res2 = run_simulation(self.df, self.config)

        self.assertEqual(res1[0], res2[0]) # Final Value
        self.assertEqual(len(res1[1]), len(res2[1])) # Number of trades

        # Check first trade date string equality
        if len(res1[1]) > 0:
            self.assertEqual(res1[1][0]["Date"], res2[1][0]["Date"])

if __name__ == "__main__":
    unittest.main()
