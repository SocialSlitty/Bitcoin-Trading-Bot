
import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_simulation_reproducibility(self):
        """
        Verifies that the simulation produces deterministic results for a fixed seed.
        This serves as a regression test for performance optimizations.
        """
        config = SimConfig(seed=42)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)
        final_value, trades, ledger = run_simulation(df, config)

        # Expected values from baseline run
        expected_final_value = 981.8820640729841
        expected_trades_count = 5

        self.assertAlmostEqual(final_value, expected_final_value, places=6)
        self.assertEqual(len(trades), expected_trades_count)

        # Verify first trade details
        first_trade = trades[0]
        self.assertEqual(first_trade['Date'], '2024-11-01')
        self.assertEqual(first_trade['Type'], 'BUY')
        self.assertAlmostEqual(first_trade['Price'], 54603.68639901874, places=4)

if __name__ == "__main__":
    unittest.main()
