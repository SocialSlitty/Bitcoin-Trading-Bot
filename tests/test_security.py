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
        # Mock dataframe and trades_log
        mock_df = MagicMock()
        # Mocking iloc to return a copy that is also a mock
        mock_df.iloc.__getitem__.return_value.copy.return_value = MagicMock()

        trades_log = []

        # Attempt path traversal
        filename = "../evil_plot.png"

        # This should raise ValueError in a secure implementation
        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
            plot_results(mock_df, trades_log, filename=filename)

    @patch('bitcoin_sim.plt')
    def test_plot_results_absolute_path(self, mock_plt):
        mock_df = MagicMock()
        mock_df.iloc.__getitem__.return_value.copy.return_value = MagicMock()
        trades_log = []

        # Attempt absolute path
        filename = "/tmp/evil_plot.png"

        with self.assertRaisesRegex(ValueError, "Filename must not contain path components"):
            plot_results(mock_df, trades_log, filename=filename)

    @patch('bitcoin_sim.plt')
    def test_plot_results_valid_filename(self, mock_plt):
        mock_df = MagicMock()
        mock_df.iloc.__getitem__.return_value.copy.return_value = MagicMock()
        trades_log = []

        filename = "safe_plot.png"
        try:
            plot_results(mock_df, trades_log, filename=filename)
        except ValueError:
            self.fail("plot_results raised ValueError unexpectedly for valid filename")

if __name__ == "__main__":
    unittest.main()
