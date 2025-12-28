import unittest
import sys
import os
import shutil
import pathlib
import pandas as pd
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create dummy data for plot_results
        dates = pd.date_range(end="2024-01-01", periods=60)
        self.df = pd.DataFrame({
            "Date": dates,
            "Close": [100.0] * 60,
            "EMA_7": [100.0] * 60,
            "SMA_30": [100.0] * 60,
            "SMA_200": [100.0] * 60,
            "Volume": [1000] * 60
        })
        self.trades_log = []

    def test_path_traversal_prevention(self):
        """Test that plot_results raises ValueError for paths outside CWD."""

        # We need to mock plt.savefig to avoid actual file operations and display errors
        # BUT we want the validation logic before savefig to run.

        with patch('matplotlib.pyplot.figure'), \
             patch('matplotlib.pyplot.plot'), \
             patch('matplotlib.pyplot.scatter'), \
             patch('matplotlib.pyplot.title'), \
             patch('matplotlib.pyplot.xlabel'), \
             patch('matplotlib.pyplot.ylabel'), \
             patch('matplotlib.pyplot.legend'), \
             patch('matplotlib.pyplot.grid'), \
             patch('matplotlib.pyplot.tight_layout'), \
             patch('matplotlib.pyplot.savefig') as mock_savefig:

            # Attempt to write to parent directory
            malicious_filename = "../malicious_plot.png"

            with self.assertRaisesRegex(ValueError, "Path traversal detected"):
                plot_results(self.df, self.trades_log, filename=malicious_filename)

            # Ensure savefig was NOT called
            mock_savefig.assert_not_called()

            # Attempt to write to absolute path outside CWD (e.g., /tmp)
            # Note: /tmp might be allowed depending on logic, but current logic enforces CWD.
            # Let's use a path that is definitely outside, like '/'
            if os.name == 'posix':
                malicious_filename = "/tmp/malicious_plot.png"
                # If CWD is not /tmp, this should fail.
                cwd = pathlib.Path.cwd()
                if not pathlib.Path(malicious_filename).resolve().is_relative_to(cwd):
                     with self.assertRaisesRegex(ValueError, "Path traversal detected"):
                        plot_results(self.df, self.trades_log, filename=malicious_filename)

    def test_valid_filename(self):
        """Test that a valid filename within CWD is accepted."""
        with patch('matplotlib.pyplot.figure'), \
             patch('matplotlib.pyplot.plot'), \
             patch('matplotlib.pyplot.scatter'), \
             patch('matplotlib.pyplot.title'), \
             patch('matplotlib.pyplot.xlabel'), \
             patch('matplotlib.pyplot.ylabel'), \
             patch('matplotlib.pyplot.legend'), \
             patch('matplotlib.pyplot.grid'), \
             patch('matplotlib.pyplot.tight_layout'), \
             patch('matplotlib.pyplot.savefig') as mock_savefig:

            valid_filename = "safe_plot.png"
            plot_results(self.df, self.trades_log, filename=valid_filename)

            # Ensure savefig WAS called with resolved path
            self.assertTrue(mock_savefig.called)
            args, _ = mock_savefig.call_args
            self.assertTrue(str(args[0]).endswith("safe_plot.png"))

if __name__ == "__main__":
    unittest.main()
