import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulationRegression(unittest.TestCase):
    def setUp(self):
        # Use a fixed seed config for reproducibility
        self.config = SimConfig(seed=42, days=260)
        self.df = generate_synthetic_data(self.config)
        self.df = calculate_indicators(self.df)
        self.df = self.df.dropna().reset_index(drop=True)

    def test_run_simulation_output_structure(self):
        final_value, trades_log, daily_ledger = run_simulation(self.df, self.config)

        # Check return types
        self.assertIsInstance(final_value, float)
        self.assertIsInstance(trades_log, list)
        self.assertIsInstance(daily_ledger, pd.DataFrame)

        # Check date formats in trades_log
        if len(trades_log) > 0:
            trade = trades_log[0]
            self.assertIn("Date", trade)
            # Date should be a string YYYY-MM-DD
            self.assertIsInstance(trade["Date"], str)
            self.assertRegex(trade["Date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_run_simulation_values(self):
        # Run simulation
        final_value, trades_log, daily_ledger = run_simulation(self.df, self.config)

        # Check specific values for regression
        # These values depend on seed=42
        # Just check they are not None and reasonable
        self.assertGreater(final_value, 0)
        self.assertEqual(len(daily_ledger), 60) # Should be 60 days

        # Check that we have some trades (depends on logic, but with seed 42 likely yes)
        # If no trades, that's fine too, but we want to verify structure.

if __name__ == "__main__":
    unittest.main()
