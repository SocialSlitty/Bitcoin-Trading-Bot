import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    @patch('bitcoin_sim.plt')
    def test_plot_results_path_traversal(self, mock_plt):
        """
        Test that plot_results raises ValueError if filename contains path components.
        This prevents writing to arbitrary locations (Path Traversal).
        """
        # Mock data
        mock_df = MagicMock()
        mock_df.iloc = MagicMock()
        mock_trades = []

        # Test with a filename containing a path separator
        unsafe_filenames = [
            "../outside.png",
            "subdir/inside.png",
            "/absolute/path.png",
            "C:\\windows\\test.png"  # Windows style (might not be detected on Linux env but good to test logic if possible)
        ]

        for filename in unsafe_filenames:
            # We only strictly enforce that os.path.dirname is empty
            # which works for / and whatever os.sep is.
            # Manually checking for both / and \ might be safer for cross-platform

            # Note: On Linux, 'subdir/inside.png' has a dirname.
            # '../outside.png' has a dirname.

            # Only test if the filename effectively has a directory component for the current OS
            if os.path.dirname(filename):
                with self.subTest(filename=filename):
                    with self.assertRaises(ValueError):
                        plot_results(mock_df, mock_trades, filename=filename)

    @patch('bitcoin_sim.plt')
    def test_plot_results_valid_filename(self, mock_plt):
        """Test that a valid filename is accepted."""
        mock_df = MagicMock()
        mock_df.iloc = MagicMock()
        mock_trades = []

        valid_filename = "safe_plot.png"

        try:
            plot_results(mock_df, mock_trades, filename=valid_filename)
        except ValueError:
            self.fail("plot_results raised ValueError for a valid filename")

        # Verify savefig was called
        mock_plt.savefig.assert_called_with(valid_filename)

if __name__ == "__main__":
    unittest.main()
