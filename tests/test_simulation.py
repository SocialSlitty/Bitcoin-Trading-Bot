import unittest
import sys
import os
import pandas as pd
import numpy as np
import matplotlib
# Use Agg backend to prevent display errors
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_simulation_runs(self):
        # Use a fixed seed and enough days
        config = SimConfig(seed=42, days=300)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)

        # Verify df has enough rows
        self.assertGreaterEqual(len(df), 60)

        final_val, trades, ledger = run_simulation(df, config)

        # Check output types
        self.assertIsInstance(final_val, float)
        self.assertIsInstance(trades, list)
        self.assertIsInstance(ledger, pd.DataFrame)

        # Check trades format if any
        # With seed=42 and days=300, we expect trades
        self.assertTrue(len(trades) > 0, "Simulation with seed=42 should produce trades")

        trade = trades[0]
        self.assertIn("Date", trade)
        # Verify date format YYYY-MM-DD
        self.assertRegex(trade["Date"], r"^\d{4}-\d{2}-\d{2}$")

        # Check ledger format
        self.assertIn("Date", ledger.columns)
        # Ledger date is numpy datetime64
        self.assertTrue(np.issubdtype(ledger["Date"].dtype, np.datetime64))

        # Verify ledger length matches simulation window (60 days)
        # run_simulation hardcodes 60 days
        self.assertEqual(len(ledger), 60)

if __name__ == "__main__":
    unittest.main()
