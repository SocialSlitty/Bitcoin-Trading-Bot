
import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_simulation_results(self):
        # Use default config (seed=42)
        config = SimConfig()

        # 1. Generate Data
        df = generate_synthetic_data(config)

        # 2. Calculate Indicators
        df = calculate_indicators(df)

        # 3. Drop NaN rows (replicating main block logic)
        df = df.dropna().reset_index(drop=True)

        # 4. Run Simulation
        final_value, trades, ledger = run_simulation(df, config)

        # Assertions to ensure regression safety
        self.assertAlmostEqual(final_value, 981.88, places=2)
        self.assertEqual(len(trades), 5)

        # Check first trade details
        first_trade = trades[0]
        self.assertEqual(first_trade['Date'], "2024-11-01")
        self.assertEqual(first_trade['Type'], "BUY")

        # Check last trade details
        last_trade = trades[-1]
        self.assertEqual(last_trade['Date'], "2024-12-14")
        self.assertEqual(last_trade['Type'], "BUY")

        # Verify ledger dates are datetime64[D] (or similar numpy/pandas types)
        # In the simulation, daily_ledger stores 'today_date_val' which is dates[i] (numpy datetime64)
        self.assertTrue(isinstance(ledger.iloc[0]['Date'], (np.datetime64, pd.Timestamp)))

if __name__ == "__main__":
    unittest.main()
