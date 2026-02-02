import unittest
import numpy as np
import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_run_simulation_consistency(self):
        config = SimConfig(seed=42, days=300) # Ensure enough days for warm-up + 60 days
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)

        final_value, trades, ledger = run_simulation(df, config)

        # Check basic structure
        self.assertIsInstance(final_value, float)
        self.assertIsInstance(trades, list)
        self.assertIsInstance(ledger, pd.DataFrame)

        # Check date format in trades
        if trades:
            self.assertRegex(trades[0]['Date'], r'^\d{4}-\d{2}-\d{2}$')

        # Check correctness of dates
        # The first date in simulation (last 60 days)
        start_idx = len(df) - 60
        expected_date = df['Date'].iloc[start_idx]

        # ledger contains the simulation steps
        self.assertEqual(len(ledger), 60)
        self.assertEqual(ledger['Date'].iloc[0], expected_date)

if __name__ == '__main__':
    unittest.main()
