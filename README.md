# Bitcoin Trading Bot 📈

A comprehensive backtesting framework for evaluating Bitcoin trading strategies using synthetic data and technical analysis.

## Overview

This project simulates Bitcoin price movements using **Geometric Brownian Motion (GBM)**, a mathematical model that captures realistic price volatility and trends. The framework implements a **Golden Cross trading strategy**, a popular technical analysis approach that identifies optimal entry and exit points based on moving average crossovers.

## Features

✨ **Synthetic Data Generation with GBM**
- Realistic Bitcoin price simulation with configurable drift and volatility
- Generated OHLCV (Open, High, Low, Close, Volume) data
- Reproducible results with fixed random seeds

📊 **Technical Indicators**
- EMA(7): 7-day Exponential Moving Average
- SMA(30): 30-day Simple Moving Average
- SMA(200): 200-day Simple Moving Average (trend filter)
- Volume SMA(10): 10-day Volume Moving Average

🎯 **Golden Cross Strategy**
- Entry signals with volume and trend confirmation
- Death Cross exit signals
- Configurable volume threshold filters

💰 **Fee-Aware Backtesting**
- 0.1% trading fees on all transactions
- Realistic profit/loss calculations
- Complete trade history logging

📈 **Performance Metrics**
- ROI (Return on Investment)
- Maximum Drawdown
- Win Rate percentage
- Total trades executed

🎨 **Automated Visualization**
- Price charts with indicator overlays
- Buy/Sell signal markers
- Saved as PNG for analysis

## Installation

```bash
git clone https://github.com/SocialSlitty/bitcoin-trading-bot.git
cd bitcoin-trading-bot
pip install -r requirements.txt
```

## Quick Start

Run the simulation with default parameters:

```bash
python src/bitcoin_sim.py
```

**What happens when you run it:**
1. Generates 260 days of synthetic Bitcoin price data using GBM
2. Calculates technical indicators (EMA, SMA, Volume averages)
3. Backtests the Golden Cross strategy on the last 60 days
4. Outputs detailed trade logs and performance metrics to console
5. Saves a visualization chart as `trading_simulation.png`

## Configuration

The simulation is controlled through the `SimConfig` dataclass with the following parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `days` | 260 | Total days of price data to generate |
| `start_price` | 60000.0 | Initial Bitcoin price in USD |
| `seed` | 42 | Random seed for reproducibility |
| `mu` | 0.0005 | Daily drift (expected return) |
| `sigma` | 0.035 | Daily volatility (3.5%) |
| `fee_rate` | 0.001 | Trading fee percentage (0.1%) |
| `volume_threshold` | 1.2 | Volume filter multiplier |
| `initial_capital` | 1000.0 | Starting capital in USD |
| `base_volume` | 100000000 | Base daily volume ($100M) |
| `simulation_end_date` | "2024-12-21" | Fixed end date for reproducibility |

**Example configuration:**
```python
from src.bitcoin_sim import SimConfig

config = SimConfig(
    days=365,
    start_price=50000.0,
    sigma=0.05,  # Higher volatility
    initial_capital=5000.0
)
```

## Strategy Logic

### Golden Cross Entry (BUY)
A **BUY** signal is triggered when all conditions are met:
- EMA(7) crosses **above** SMA(30) (Golden Cross)
- Current price is **above** SMA(200) (uptrend confirmation)
- Volume is **above** 1.2x the 10-day average (volume confirmation)

### Death Cross Exit (SELL)
A **SELL** signal is triggered when:
- EMA(7) crosses **below** SMA(30) (Death Cross)

## Performance Metrics

**ROI (Return on Investment)**
- Percentage gain/loss relative to initial capital
- Formula: `(Final Value - Initial Capital) / Initial Capital × 100`

**Maximum Drawdown**
- Largest peak-to-trough decline in portfolio value
- Measures downside risk
- Lower is better (less risk)

**Win Rate**
- Percentage of profitable trades
- Formula: `Winning Trades / Total Closed Trades × 100`

**Total Trades**
- Number of buy/sell transactions executed
- Includes both entries and exits

## Example Output

```
FINAL PERFORMANCE RESULTS
==============================
Initial Capital: $1000.00
Final Value:     $1150.25
Net Profit:      $150.25 (15.03%)
Max Drawdown:    -8.45%
Total Trades:    8
Win Rate:        62.50%
==============================
```

## Project Structure

```
bitcoin-trading-bot/
├── src/
│   └── bitcoin_sim.py      # Main simulation and strategy logic
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Disclaimer

⚠️ **For Educational Purposes Only**

This is a backtesting framework for learning about algorithmic trading strategies. It uses synthetic data and simplified market assumptions. **Do not use this for actual trading decisions.** Real cryptocurrency markets involve additional complexities including:
- Market liquidity and slippage
- Order book dynamics
- Black swan events
- Regulatory risks
- Exchange-specific factors

Past performance (even on real data) does not guarantee future results. Always conduct thorough research and consult financial professionals before trading.
