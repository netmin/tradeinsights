from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd


def read_csv_into_df(file_path: Union[str, Path]) -> pd.DataFrame:
    """Reads a csv file into a pandas DataFrame"""
    if not Path(file_path).exists():
        raise FileNotFoundError(f"No file found at: {file_path}")

    df = pd.read_csv(file_path)
    df["TS"] = pd.to_datetime(df["TS"])
    df.set_index("TS", inplace=True)

    return df


def form_candlesticks(df: pd.DataFrame, time_interval: str) -> pd.DataFrame:
    """Create candlestick charts for given time interval.
    :param df: The DataFrame containing the price data.
    :param time_interval: The time interval for resampling the price data.
    :return: A DataFrame containing the Open, High, Low, and Close prices for each interval.

    Note:
    - This method requires the `matplotlib`, `mplfinance`, `numpy`, `pandas`, and `pathlib` libraries.
    - The price data should be in the `PRICE` column of the DataFrame.
    - The `time_interval` should be a valid pandas resampling string, e.g., "5T" for 5 minutes, "1H" for 1 hour.
    - The returned DataFrame will have the resampled Open, High, Low, and Close prices for each interval.

    Example usage:
    ```python
    import pandas as pd
    from pathlib import Path
    import mplfinance as mpf

    # Load data from a CSV file
    data_file = Path("data.csv")
    df = pd.read_csv(data_file)

    # Convert date column to datetime format
    df["TS"] = pd.to_datetime(df["TS"])

    # Set the date column as the index of the DataFrame
    df = df.set_index("TS")

    # Resample the price data to 1 hour intervals
    resampled_df = form_candlesticks(df, "1H")

    # Plot the candlestick chart
    mpf.plot(resampled_df, type="candle")
    ```
    """
    return df["PRICE"].resample(time_interval).ohlc()


def calculate_ema(data_series: pd.Series, period: int) -> pd.Series:
    """
    Calculate EMA (Exponential Moving Average) for a given data series.

    :param data_series: A pandas Series containing the data points.
    :param period: An integer representing the period for calculating EMA.
    :return: A pandas Series containing the calculated EMA values.

    Raises:
        TypeError: If the data series does not contain numeric data.

    Example usage:
        >>> data = pd.Series([1, 2, 3, 4, 5])
        >>> ema = calculate_ema(data, 3)
        >>> print(ema)
        0 1.000000
        1 1.750000
        2 2.562500
        3 3.421875
        4 4.316406
        dtype: float64

    Note:
        - The data series should only contain numeric data.
        - EMA is calculated using the span parameter, which represents
          the number of periods to include in the calculation.
        - The adjust parameter is set to False to avoid adjusting the
          weights based on the number of periods.
    """
    if not np.issubdtype(data_series.dtype, np.number):
        raise TypeError("Series should only contain numeric data")
    return data_series.ewm(span=period, adjust=False).mean()


if __name__ == "__main__":
    file_path = "data/prices.csv"
    df = read_csv_into_df(file_path)

    candlesticks = form_candlesticks(df, "10H")
    ema_period = 14
    df["EMA"] = calculate_ema(df["PRICE"], ema_period)

    mpf.plot(candlesticks, type="candle", style="yahoo", title="Candlestick Chart")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df["PRICE"], label="Price")
    ax.plot(df.index, df["EMA"], label=f"EMA-{ema_period}", color="orange")

    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.set_title("Price Chart with EMA")
    ax.legend()

    plt.show()
