import unittest
import os
import shutil
import tempfile
import sys
import pandas as pd
import matplotlib
# Use Agg backend for headless testing
matplotlib.use('Agg')

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from bitcoin_sim import plot_results

class TestSecurityIssue(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.outside_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.outside_dir)

    def test_path_traversal_prevention(self):
        # Create dummy data
        df = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=100),
            'Close': [100] * 100,
            'EMA_7': [100] * 100,
            'SMA_30': [100] * 100,
            'SMA_200': [100] * 100
        })
        trades_log = []

        # Target file that should NOT be created
        target_file = os.path.join(self.outside_dir, "hacked.png")

        cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)

            # Calculate relative path to outside_dir
            rel_path = os.path.relpath(self.outside_dir, self.test_dir)
            malicious_filename = os.path.join(rel_path, "hacked.png")

            print(f"Attempting to write to: {malicious_filename}")

            # Expect ValueError now
            with self.assertRaises(ValueError) as cm:
                plot_results(df, trades_log, filename=malicious_filename)

            print(f"Caught expected error: {cm.exception}")
            self.assertIn("contains path components", str(cm.exception))

            # Verify target file still doesn't exist
            if os.path.exists(target_file):
                self.fail("File was written despite the error!")
            else:
                print("Secure: File was not written.")

        finally:
            os.chdir(cwd)

if __name__ == '__main__':
    unittest.main()
