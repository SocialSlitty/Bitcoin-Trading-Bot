import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import run_simulation, SimConfig

class TestSimulation(unittest.TestCase):
    def test_run_simulation_date_format(self):
        # Create a small DataFrame
        N = 70 # Needs at least 60
        dates = np.arange('2024-01-01', '2024-03-12', dtype='datetime64[D]')
        # Ensure we have N dates
        dates = dates[:N]

        # Create dataframe
        df = pd.DataFrame({
            'Date': dates,
            'Close': np.linspace(100, 200, N),
            'Volume': np.ones(N) * 1000000000, # Large volume to pass filter
            'EMA_7': np.linspace(100, 200, N),
            'SMA_30': np.linspace(100, 200, N),
            'SMA_200': np.linspace(90, 190, N),
            'Vol_SMA_10': np.ones(N) * 1000000
        })

        # We need to ensure logic triggers.
        # Run runs on last 60 days. start_idx = 10.
        # We manipulate index 20 (relative to start 0) -> actual index 20.

        # Buy condition:
        # prev_ema_7 <= prev_sma_30 AND ema_7 > sma_30
        # price > sma_200 AND vol > threshold * vol_avg

        # Set index 19 (prev)
        df.loc[19, 'EMA_7'] = 100
        df.loc[19, 'SMA_30'] = 110 # EMA < SMA

        # Set index 20 (curr)
        df.loc[20, 'EMA_7'] = 120
        df.loc[20, 'SMA_30'] = 110 # EMA > SMA -> Cross

        df.loc[20, 'Close'] = 150
        df.loc[20, 'SMA_200'] = 100 # Price > SMA_200
        df.loc[20, 'Volume'] = 2000000000 # > 1.2 * 1000000

        # Run
        # Suppress logging during test
        import logging
        logging.disable(logging.CRITICAL)

        try:
            final_val, trades, ledger = run_simulation(df, SimConfig())
        finally:
            logging.disable(logging.NOTSET)

        # Check trades
        self.assertTrue(len(trades) > 0, "Expected at least one trade")
        first_trade = trades[0]

        # Check date format "YYYY-MM-DD"
        self.assertRegex(first_trade['Date'], r'^\d{4}-\d{2}-\d{2}$')

        # Check specific date correctness
        # Index 20 date is dates[20]
        expected_date = str(dates[20])
        self.assertEqual(first_trade['Date'], expected_date)

        # Check that we have exactly the number of ledger entries as simulation days (60)
        self.assertEqual(len(ledger), 60)

if __name__ == '__main__':
    unittest.main()
