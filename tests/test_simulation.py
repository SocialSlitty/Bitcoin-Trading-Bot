import unittest
import sys
import os
import numpy as np
import pandas as pd

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_run_simulation_deterministic(self):
        """
        Verifies that run_simulation produces deterministic results given a fixed seed.
        This serves as a regression test for refactoring.
        """
        config = SimConfig(seed=42, days=300)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)

        final_value, trades, ledger = run_simulation(df, config)

        # Assertions based on pre-refactoring run
        self.assertAlmostEqual(final_value, 830.9395404529857, places=5)
        self.assertEqual(len(trades), 4)

        first_trade = trades[0]
        self.assertEqual(first_trade['Date'], '2024-11-04')
        self.assertEqual(first_trade['Type'], 'BUY')
        self.assertAlmostEqual(first_trade['Price'], 60761.19516531508, places=5)

    def test_simulation_runs_full_length(self):
        """
        Test that simulation can run on full generated data if passed appropriately.
        We'll use a config that generates enough data and verify it doesn't crash.
        """
        config = SimConfig(seed=123, days=100)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)
        # Should result in less than 60 rows potentially if days=100 and warmup=200?
        # SimConfig default days=260. warmup is implied by indicators.
        # SMA_200 requires 200 data points.
        # If days=100, generate_synthetic_data returns 100 rows.
        # calculate_indicators will have SMA_200 as NaN for all rows.
        # dropna() will result in empty dataframe.

        # So we need days > 200 + 60
        config = SimConfig(seed=123, days=300)
        df = generate_synthetic_data(config)
        df = calculate_indicators(df)
        df = df.dropna().reset_index(drop=True)

        # This checks if run_simulation works without error
        run_simulation(df, config)

if __name__ == '__main__':
    unittest.main()
