import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        # Setup mock df and trades - minimal data to avoid errors before the savefig call
        import pandas as pd
        df = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=60),
            'Close': [100]*60,
            'EMA_7': [100]*60,
            'SMA_30': [100]*60,
            'SMA_200': [100]*60
        })
        trades = []

        # Attempt path traversal
        unsafe_filename = "../evil.png"

        # Expectation: Should raise ValueError because of path traversal
        with self.assertRaises(ValueError):
            plot_results(df, trades, filename=unsafe_filename)

        # Also check absolute paths if we want to restrict to CWD (or just basename)
        # Using a dummy absolute path that should be rejected
        unsafe_filename_2 = "/tmp/evil.png"
        with self.assertRaises(ValueError):
             plot_results(df, trades, filename=unsafe_filename_2)

    @patch('bitcoin_sim.plt')
    def test_plot_results_valid_filename(self, mock_plt):
         # Setup mock df and trades
        import pandas as pd
        df = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=60),
            'Close': [100]*60,
            'EMA_7': [100]*60,
            'SMA_30': [100]*60,
            'SMA_200': [100]*60
        })
        trades = []

        valid_filename = "safe_plot.png"
        try:
            plot_results(df, trades, filename=valid_filename)
        except ValueError:
            self.fail("plot_results raised ValueError on valid filename")

        # Verify savefig was called
        mock_plt.savefig.assert_called_with(valid_filename)

if __name__ == "__main__":
    unittest.main()
