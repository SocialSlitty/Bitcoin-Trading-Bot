import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class SimConfig:
    """Configuration for the trading simulation."""

    days: int = 260
    start_price: float = 60000.0
    seed: int = 42
    mu: float = 0.0005  # Daily drift
    sigma: float = 0.035  # Daily volatility (3.5%)
    fee_rate: float = 0.001  # Trading fee (0.1%)
    volume_threshold: float = 1.2  # Volume filter multiplier
    initial_capital: float = 1000.0
    base_volume: float = 100_000_000  # Base daily volume ($100M)
    simulation_end_date: str = "2024-12-21"  # Fixed for reproducibility

    def __post_init__(self):
        if self.days <= 0:
            raise ValueError("days must be positive")
        if self.start_price <= 0:
            raise ValueError("start_price must be positive")
        if self.sigma < 0:
            raise ValueError("sigma must be non-negative")
        if self.initial_capital < 0:
            raise ValueError("initial_capital must be non-negative")
        if self.base_volume < 0:
            raise ValueError("base_volume must be non-negative")
        if self.fee_rate < 0:
            raise ValueError("fee_rate must be non-negative")
        if self.volume_threshold < 0:
            raise ValueError("volume_threshold must be non-negative")


def generate_synthetic_data(config: SimConfig = None):
    """
    Generates synthetic daily OHLCV data for Bitcoin using Geometric Brownian Motion.

    Args:
        config (SimConfig): Configuration object with simulation parameters.

    Returns:
        pd.DataFrame: DataFrame containing Date, Open, High, Low, Close, Volume.
    """
    if config is None:
        config = SimConfig()

    np.random.seed(config.seed)

    # Parameters from config
    mu = config.mu
    sigma = config.sigma
    dt = 1  # Time step

    # Vectorized Geometric Brownian Motion
    # 1. Generate all random shocks at once
    shocks = np.random.normal(size=config.days)

    # 2. Calculate daily drifts and diffusion terms
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * shocks

    # 3. Compute log returns and cumulative sum
    log_returns = drift + diffusion
    cum_log_returns = np.cumsum(log_returns)

    # 4. Compute prices path
    # prices[0] is start_price, prices[1] is start_price * exp(r1), etc.
    prices = np.zeros(config.days + 1)
    prices[0] = config.start_price
    prices[1:] = config.start_price * np.exp(cum_log_returns)

    # Vectorized Volume Simulation
    vol_factors = np.random.lognormal(mean=0, sigma=0.5, size=config.days)

    # Calculate price move impact vectorially
    # abs(curr - prev) / prev
    price_changes = np.abs(np.diff(prices)) / prices[:-1]
    price_move_impacts = price_changes * 20

    volumes = config.base_volume * vol_factors * (1 + price_move_impacts)

    closes = prices[1:]
    opens = prices[:-1]

    # Generate High/Low relative to Open/Close (Vectorized)
    n = len(opens)
    # Generate random wick percentages for all days at once
    wick_ups_pct = np.random.uniform(0, 0.02, size=n)
    wick_downs_pct = np.random.uniform(0, 0.02, size=n)

    wick_ups = wick_ups_pct * opens
    wick_downs = wick_downs_pct * opens

    # Calculate Highs and Lows
    highs = np.maximum(opens, closes) + wick_ups
    lows = np.minimum(opens, closes) - wick_downs

    # Use fixed date for reproducibility
    # OPTIMIZATION: Use numpy arithmetic instead of pd.date_range for performance and robustness
    # This prevents OutOfBoundsDatetime errors for very large datasets (>200k days) and is ~3x faster.
    end_date = np.datetime64(config.simulation_end_date)
    start_date = end_date - np.timedelta64(config.days - 1, "D")
    dates = np.arange(
        start_date, end_date + np.timedelta64(1, "D"), dtype="datetime64[D]"
    )

    df = pd.DataFrame(
        {
            "Date": dates,
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes,
            "Volume": volumes,
        }
    )

    return df


def calculate_indicators(df):
    """
    Calculates technical indicators required for the strategy.

    Args:
        df (pd.DataFrame): DataFrame with OHLCV data.

    Returns:
        pd.DataFrame: DataFrame with added indicator columns.
    """
    # 7-day EMA
    df["EMA_7"] = df["Close"].ewm(span=7, adjust=False).mean()

    # 30-day SMA
    df["SMA_30"] = df["Close"].rolling(window=30).mean()

    # 200-day SMA
    df["SMA_200"] = df["Close"].rolling(window=200).mean()

    # 10-day Volume SMA
    df["Vol_SMA_10"] = df["Volume"].rolling(window=10).mean()

    return df


def run_simulation(df, config: SimConfig = None):
    """
    Runs the trading simulation on the last 60 days of data.

    Args:
        df (pd.DataFrame): DataFrame with OHLCV data and indicators.
        config (SimConfig): Configuration object with simulation parameters.

    Returns:
        tuple: (final_portfolio_value, trades_log, daily_ledger)
    """
    if config is None:
        config = SimConfig()

    cash = config.initial_capital
    btc_holdings = 0.0

    # Ensure we have enough data after NaN removal
    if len(df) < 60:
        raise ValueError(
            "Dataframe must have at least 60 days of data after indicator warm-up."
        )

    start_idx = len(df) - 60

    trades_log = []
    daily_ledger = []

    logger.info(
        f"{'Date':<12} | {'Price':<10} | {'7 EMA':<10} | {'30 SMA':<10} | {'Action':<6} | {'Portfolio':<10}"
    )
    logger.info("-" * 75)

    # Pre-extract numpy arrays for performance (avoiding iloc in loop)
    dates_series = df["Date"]
    dates = dates_series.values
    prices = df["Close"].values
    ema_7s = df["EMA_7"].values
    sma_30s = df["SMA_30"].values
    sma_200s = df["SMA_200"].values
    volumes = df["Volume"].values
    vol_avgs = df["Vol_SMA_10"].values

    for i in range(start_idx, len(df)):
        # Direct numpy array access is much faster than df.iloc[i]
        today_date_val = dates[i]
        # Format date for logging/output (handling numpy datetime64)
        current_date = pd.Timestamp(today_date_val).strftime("%Y-%m-%d")

        price = prices[i]
        ema_7 = ema_7s[i]
        sma_30 = sma_30s[i]
        sma_200 = sma_200s[i]
        vol = volumes[i]
        vol_avg = vol_avgs[i]

        # Previous day values
        prev_ema_7 = ema_7s[i - 1]
        prev_sma_30 = sma_30s[i - 1]

        # Check Crossover Logic
        # Buy Cross: Yesterday EMA7 <= Yesterday SMA30 AND Today EMA7 > Today SMA30
        buy_cross = (prev_ema_7 <= prev_sma_30) and (ema_7 > sma_30)

        # Sell Cross: Today EMA7 < Today SMA30 (Standard Death Cross)
        # Note: The user said "7 EMA crosses BELOW 30 SMA".
        sell_cross = (prev_ema_7 >= prev_sma_30) and (ema_7 < sma_30)

        action = "HOLD"

        # Trading Logic
        if btc_holdings == 0:
            # Look for Buy
            if buy_cross:
                # Check Filters
                if price > sma_200 and vol > config.volume_threshold * vol_avg:
                    # BUY
                    # Fee is taken from the cash amount before buying
                    # cost = amount spent including fee?
                    # Standard exchange:
                    # If I have $1000 and fee is 0.1%, I pay $1 fee and buy $999 worth of BTC.
                    # Or I buy $1000 worth and receive slightly less BTC.
                    # Let's assume: cash is fully used.
                    # fee = cash * fee_rate
                    # invested = cash - fee
                    # btc_holdings = invested / price

                    fee = cash * config.fee_rate
                    invested = cash - fee
                    btc_holdings = invested / price
                    cash = 0
                    action = "BUY"
                    trades_log.append(
                        {
                            "Date": current_date,
                            "Type": "BUY",
                            "Price": price,
                            "Amount": btc_holdings,
                            "Value": invested + fee,  # Total Cost Basis
                        }
                    )
        else:
            # Look for Sell
            if sell_cross:
                # SELL
                revenue = btc_holdings * price * (1 - config.fee_rate)
                cash = revenue
                btc_holdings = 0
                action = "SELL"
                trades_log.append(
                    {
                        "Date": current_date,
                        "Type": "SELL",
                        "Price": price,
                        "Amount": 0,  # Sold all
                        "Value": revenue,
                    }
                )

        # Calculate Daily Portfolio Value
        portfolio_value = cash + (btc_holdings * price)

        daily_ledger.append(
            {
                "Date": today_date_val,
                "Price": price,
                "EMA_7": ema_7,
                "SMA_30": sma_30,
                "SMA_200": sma_200,
                "Portfolio Value": portfolio_value,
                "Holdings": btc_holdings,
            }
        )

        logger.info(
            f"{current_date} | {price:10.2f} | {ema_7:10.2f} | {sma_30:10.2f} | {action:<6} | {portfolio_value:10.2f}"
        )

    return (
        cash + (btc_holdings * prices[-1]),
        trades_log,
        pd.DataFrame(daily_ledger),
    )


def plot_results(df, trades_log, filename="trading_simulation.png"):
    """
    Plots the price, indicators, and trade markers.

    Args:
        df (pd.DataFrame): DataFrame with OHLCV data and indicators.
        trades_log (list): List of trade dictionaries.
        filename (str): Output filename for the plot.

    Raises:
        ValueError: If filename contains path components (security check).
    """
    # Security Check: Prevent path traversal
    if Path(filename).name != filename:
        raise ValueError(f"Invalid filename: '{filename}'. Path components are not allowed.")

    # We only plot the last 60 days
    plot_data = df.iloc[-60:].copy()

    plt.figure(figsize=(14, 7))
    plt.plot(
        plot_data["Date"], plot_data["Close"], label="Price", color="black", alpha=0.6
    )
    plt.plot(
        plot_data["Date"], plot_data["EMA_7"], label="7 EMA", color="blue", alpha=0.8
    )
    plt.plot(
        plot_data["Date"],
        plot_data["SMA_30"],
        label="30 SMA",
        color="orange",
        alpha=0.8,
    )
    plt.plot(
        plot_data["Date"],
        plot_data["SMA_200"],
        label="200 SMA",
        color="red",
        alpha=0.8,
        linestyle="--",
    )

    # Plot Buy/Sell Markers
    for trade in trades_log:
        date = pd.to_datetime(trade["Date"])
        price = trade["Price"]
        if trade["Type"] == "BUY":
            plt.scatter(
                date,
                price,
                color="green",
                marker="^",
                s=100,
                label="Buy"
                if "Buy" not in plt.gca().get_legend_handles_labels()[1]
                else "",
            )
        elif trade["Type"] == "SELL":
            plt.scatter(
                date,
                price,
                color="red",
                marker="v",
                s=100,
                label="Sell"
                if "Sell" not in plt.gca().get_legend_handles_labels()[1]
                else "",
            )

    plt.title("Bitcoin Price Simulation & Golden Cross Strategy")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    logger.info(f"Plot saved to {filename}")


if __name__ == "__main__":
    # Initialize config
    config = SimConfig()

    # 1. Generate Data
    logger.info("Generating synthetic price data...")
    df = generate_synthetic_data(config)

    # 2. Calculate Indicators
    logger.info("Calculating technical indicators...")
    df = calculate_indicators(df)

    # 3. Drop NaN rows from indicator warm-up period (critical fix)
    rows_before = len(df)
    df = df.dropna().reset_index(drop=True)
    rows_after = len(df)
    logger.info(
        f"Dropped {rows_before - rows_after} NaN rows from indicator warm-up period"
    )

    # 4. Run Simulation
    logger.info("Running trading simulation...")
    final_value, trades, ledger = run_simulation(df, config)

    # 5. Calculate Stats
    net_profit = final_value - config.initial_capital
    roi = (net_profit / config.initial_capital) * 100

    # Max Drawdown
    ledger["Peak"] = ledger["Portfolio Value"].cummax()
    ledger["Drawdown"] = (ledger["Portfolio Value"] - ledger["Peak"]) / ledger["Peak"]
    max_drawdown = ledger["Drawdown"].min() * 100

    # Win Rate
    wins = 0
    total_closed_trades = 0
    last_buy_cost = 0

    for trade in trades:
        if trade["Type"] == "BUY":
            last_buy_cost = trade["Value"]
        elif trade["Type"] == "SELL":
            total_closed_trades += 1
            if trade["Value"] > last_buy_cost:
                wins += 1

    win_rate = (wins / total_closed_trades * 100) if total_closed_trades > 0 else 0.0

    logger.info("\n" + "=" * 30)
    logger.info("FINAL PERFORMANCE RESULTS")
    logger.info("=" * 30)
    logger.info(f"Initial Capital: ${config.initial_capital:.2f}")
    logger.info(f"Final Value:     ${final_value:.2f}")
    logger.info(f"Net Profit:      ${net_profit:.2f} ({roi:.2f}%)")
    logger.info(f"Max Drawdown:    {max_drawdown:.2f}%")
    logger.info(f"Total Trades:    {len(trades)}")
    logger.info(f"Win Rate:        {win_rate:.2f}%")
    logger.info("=" * 30)

    # 6. Plot Results
    plot_results(df, trades)
