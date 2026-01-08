import unittest
import sys
import os
import shutil
import tempfile
import pandas as pd
import matplotlib

# Use Agg backend to avoid GUI errors
matplotlib.use('Agg')

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import plot_results

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Setup dummy data for plotting
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=10),
            'Close': [100.0] * 10,
            'EMA_7': [100.0] * 10,
            'SMA_30': [100.0] * 10,
            'SMA_200': [100.0] * 10
        })
        self.trades = []

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_path_traversal_prevention(self):
        """Test that plot_results rejects filenames with path components."""
        # Attempt to write to parent directory
        # Since we are in a temp dir, ".." refers to the parent of the temp dir.
        # Ideally, we want to prevent ANY directory traversal.

        unsafe_filenames = [
            "../evil.png",
            "subdir/evil.png",
            "/tmp/evil.png",
            "..\\evil.png"
        ]

        for filename in unsafe_filenames:
            with self.subTest(filename=filename):
                try:
                    plot_results(self.df, self.trades, filename=filename)
                    self.fail(f"VULNERABILITY: Successfully wrote to {filename}")
                except ValueError as e:
                    # This is what we want
                    self.assertIn("filename must not contain path components", str(e))
                except FileNotFoundError:
                     # If the directory doesn't exist, we might get this, but our code should ideally catch it BEFORE trying to write.
                     # However, since we check for separators, it should raise ValueError.
                     # If it raised FileNotFoundError, it means it bypassed our check.
                     self.fail(f"VULNERABILITY: Bypassed check and attempted to write to {filename} (got FileNotFoundError)")
                except Exception as e:
                    self.fail(f"VULNERABILITY: Bypassed check and got {type(e).__name__} for {filename}")
