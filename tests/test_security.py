import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.getcwd(), 'src'))

# Set backend before importing module that imports pyplot
import matplotlib
matplotlib.use('Agg')

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        """
        Test that plot_results raises ValueError when a filename with path components is provided.
        """
        mock_df = MagicMock()
        mock_df.iloc.__getitem__.return_value.copy.return_value = mock_df
        trades_log = []

        evil_filename = "../evil_chart.png"

        # Expect ValueError (Secure behavior)
        with self.assertRaises(ValueError):
            plot_results(mock_df, trades_log, filename=evil_filename)

    @patch('bitcoin_sim.plt')
    def test_plot_results_valid_filename(self, mock_plt):
        mock_df = MagicMock()
        mock_df.iloc.__getitem__.return_value.copy.return_value = mock_df
        trades_log = []
        valid_filename = "safe_chart.png"

        plot_results(mock_df, trades_log, filename=valid_filename)
        # Verify savefig was called on the mock_plt object
        mock_plt.savefig.assert_called_with(valid_filename)

if __name__ == "__main__":
    unittest.main()
