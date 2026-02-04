import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def test_path_traversal_in_plot_results(self):
        # Mock dataframe and trades_log
        df = MagicMock()
        # Mocking iloc[-60:].copy() return value
        # We need to make sure the mocked object behaves enough like a DF to not crash before the savefig
        mock_df_slice = MagicMock()
        # The code does: plot_data["Date"], plot_data["Close"], etc.
        mock_df_slice.__getitem__.return_value = [1, 2, 3]

        df.iloc.__getitem__.return_value.copy.return_value = mock_df_slice

        trades_log = []

        # Try to pass a malicious filename
        malicious_filename = "../malicious_plot.png"

        with patch('bitcoin_sim.plt') as mock_plt:
            with self.assertRaises(ValueError) as cm:
                plot_results(df, trades_log, filename=malicious_filename)

            self.assertIn("Filename must not contain path components", str(cm.exception))

    def test_path_traversal_absolute_path(self):
        df = MagicMock()
        mock_df_slice = MagicMock()
        mock_df_slice.__getitem__.return_value = [1, 2, 3]
        df.iloc.__getitem__.return_value.copy.return_value = mock_df_slice

        trades_log = []

        malicious_filename = "/tmp/malicious_plot.png"

        with patch('bitcoin_sim.plt') as mock_plt:
            with self.assertRaises(ValueError) as cm:
                plot_results(df, trades_log, filename=malicious_filename)

            self.assertIn("Filename must not contain path components", str(cm.exception))
