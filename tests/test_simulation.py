
import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig, generate_synthetic_data, calculate_indicators, run_simulation

class TestSimulation(unittest.TestCase):
    def test_simulation_output_consistency(self):
        # Use default config which has fixed seed=42 and fixed dates
        config = SimConfig()

        # 1. Generate Data
        df = generate_synthetic_data(config)

        # 2. Calculate Indicators
        df = calculate_indicators(df)

        # 3. Drop NaN
        df = df.dropna().reset_index(drop=True)

        # 4. Run Simulation
        final_value, trades, ledger = run_simulation(df, config)

        # Assertions to ensure regression testing
        self.assertAlmostEqual(final_value, 981.8820640729841, places=5)
        self.assertEqual(len(trades), 5)

if __name__ == "__main__":
    unittest.main()
