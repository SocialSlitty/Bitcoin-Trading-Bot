import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_run_simulation_smoke(self):
        """Smoke test to ensure run_simulation completes without error and returns valid results."""
        config = SimConfig(days=400) # Ensure enough days for >60 day simulation + 200 day warmup
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)

        final_value, trades, ledger = run_simulation(df, config)

        self.assertIsInstance(final_value, float)
        self.assertIsInstance(trades, list)
        self.assertIsInstance(ledger, pd.DataFrame)

        # Verify ledger columns
        expected_cols = ["Date", "Price", "EMA_7", "SMA_30", "SMA_200", "Portfolio Value", "Holdings"]
        for col in expected_cols:
            self.assertIn(col, ledger.columns)

        # Verify date format in trades if any trades occurred
        if trades:
            self.assertIsInstance(trades[0]["Date"], str)
            # Basic regex check for YYYY-MM-DD
            self.assertRegex(trades[0]["Date"], r"^\d{4}-\d{2}-\d{2}$")

if __name__ == "__main__":
    unittest.main()
