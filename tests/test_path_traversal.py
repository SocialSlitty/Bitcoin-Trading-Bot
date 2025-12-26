import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestPathTraversal(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        self.mock_df = MagicMock()
        # Mocking iloc and copy to return a mock object that can be indexed
        self.mock_df.iloc = MagicMock()
        self.mock_df.iloc.__getitem__.return_value.copy.return_value = {
            "Date": [], "Close": [], "EMA_7": [], "SMA_30": [], "SMA_200": []
        }
        self.mock_trades = []

    @patch('bitcoin_sim.plt')
    def test_path_traversal_attack(self, mock_plt):
        # Attempt to save to a parent directory
        unsafe_filename = "../attack.png"

        # This should raise a ValueError when the security fix is implemented
        with self.assertRaises(ValueError) as cm:
            plot_results(self.mock_df, self.mock_trades, filename=unsafe_filename)

        self.assertIn("Invalid filename", str(cm.exception))

    @patch('bitcoin_sim.plt')
    def test_absolute_path_attack(self, mock_plt):
        # Attempt to save to an absolute path (assuming unix-like for this environment)
        unsafe_filename = "/tmp/attack.png"

        with self.assertRaises(ValueError):
             plot_results(self.mock_df, self.mock_trades, filename=unsafe_filename)

    @patch('bitcoin_sim.plt')
    def test_valid_filename(self, mock_plt):
        # This should succeed
        safe_filename = "safe_plot.png"
        try:
            plot_results(self.mock_df, self.mock_trades, filename=safe_filename)
        except ValueError:
            self.fail("plot_results raised ValueError unexpectedly for valid filename")

        # Verify savefig was called with the correct filename
        mock_plt.savefig.assert_called_with(safe_filename)

if __name__ == "__main__":
    unittest.main()
