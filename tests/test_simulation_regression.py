import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulationRegression(unittest.TestCase):
    def test_run_simulation_output_structure(self):
        # Setup data
        # Need enough days for 200 SMA warmup + 60 days simulation required by run_simulation
        config = SimConfig(days=300)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        # Drop NaN rows to ensure we have valid data for simulation
        df = df.dropna().reset_index(drop=True)

        # Run simulation
        final_value, trades_log, ledger_df = run_simulation(df, config)

        # Verify output types
        self.assertIsInstance(final_value, float)
        self.assertIsInstance(trades_log, list)
        self.assertIsInstance(ledger_df, pd.DataFrame)

        # Verify trades_log structure
        for trade in trades_log:
            self.assertIn("Date", trade)
            self.assertIsInstance(trade["Date"], str, "Date must be a string")

            # Verify format YYYY-MM-DD
            try:
                # pandas to_datetime is flexible, so we check length and format strictly
                # YYYY-MM-DD is 10 chars
                self.assertEqual(len(trade["Date"]), 10)
                pd.to_datetime(trade["Date"], format="%Y-%m-%d")
            except ValueError:
                self.fail(f"Date format incorrect: {trade['Date']}")

        if len(trades_log) == 0:
            print("\nWARNING: No trades generated in test, date format not fully verified.")

if __name__ == "__main__":
    unittest.main()
