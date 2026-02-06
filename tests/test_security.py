import unittest
import sys
import os
import pandas as pd
from unittest.mock import patch

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    """Security regression tests."""

    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        """
        Test that plot_results raises ValueError if filename contains path separators.
        This prevents path traversal vulnerabilities.
        """
        # Create minimal valid dataframe to satisfy function requirements
        # It needs at least 60 rows because the function slices [-60:]
        # but technically it handles any size, just slices the last 60.
        # But to be safe lets give it enough data.
        periods = 65
        data = {
            "Date": pd.date_range(start="2023-01-01", periods=periods),
            "Close": [100.0] * periods,
            "EMA_7": [100.0] * periods,
            "SMA_30": [100.0] * periods,
            "SMA_200": [100.0] * periods,
        }
        df = pd.DataFrame(data)
        trades_log = []

        # Test absolute path
        with self.assertRaises(ValueError):
            plot_results(df, trades_log, filename="/tmp/hacked.png")

        # Test relative path
        with self.assertRaises(ValueError):
            plot_results(df, trades_log, filename="../hacked.png")

        # Test valid filename (should not raise)
        try:
            plot_results(df, trades_log, filename="safe.png")
        except ValueError:
            self.fail("plot_results raised ValueError on valid filename")

if __name__ == "__main__":
    unittest.main()
