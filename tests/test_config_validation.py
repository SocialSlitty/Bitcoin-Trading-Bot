import unittest
import sys
import os

# Add src to path to allow importing bitcoin_sim
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bitcoin_sim import SimConfig

class TestSimConfigValidation(unittest.TestCase):
    def test_valid_config(self):
        try:
            config = SimConfig()
        except ValueError as e:
            self.fail(f"Valid config raised ValueError: {e}")

    def test_invalid_days(self):
        with self.assertRaisesRegex(ValueError, "days must be positive"):
            SimConfig(days=0)

        with self.assertRaisesRegex(ValueError, "days must be positive"):
            SimConfig(days=-10)

    def test_invalid_start_price(self):
        with self.assertRaisesRegex(ValueError, "start_price must be positive"):
            SimConfig(start_price=0)

        with self.assertRaisesRegex(ValueError, "start_price must be positive"):
            SimConfig(start_price=-100)

    def test_invalid_sigma(self):
        with self.assertRaisesRegex(ValueError, "sigma must be non-negative"):
            SimConfig(sigma=-0.1)

    def test_invalid_initial_capital(self):
        with self.assertRaisesRegex(ValueError, "initial_capital must be non-negative"):
            SimConfig(initial_capital=-100)

    def test_invalid_base_volume(self):
        with self.assertRaisesRegex(ValueError, "base_volume must be non-negative"):
            SimConfig(base_volume=-1)

    def test_invalid_fee_rate(self):
        with self.assertRaisesRegex(ValueError, "fee_rate must be non-negative"):
            SimConfig(fee_rate=-0.01)

    def test_invalid_volume_threshold(self):
        with self.assertRaisesRegex(ValueError, "volume_threshold must be non-negative"):
            SimConfig(volume_threshold=-0.5)

if __name__ == "__main__":
    unittest.main()
