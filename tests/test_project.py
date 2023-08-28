from pathlib import Path

import pandas as pd
import pytest

from main import read_csv_into_df, form_candlesticks, calculate_ema


def test_read_csv_into_df():
    # Positive test case
    file_path = Path("data/prices.csv")
    df = read_csv_into_df(file_path)
    assert isinstance(df, pd.DataFrame)

    # Negative test case
    non_existent_file_path = Path("data/prices2.csv")
    with pytest.raises(FileNotFoundError):
        read_csv_into_df(non_existent_file_path)


def test_form_candlesticks():
    df = pd.DataFrame(
        {"PRICE": [1, 2, 3, 4, 5]}, index=pd.date_range(start="2023-01-01", periods=5)
    )
    candle_df = form_candlesticks(df, "2D")
    assert isinstance(candle_df, pd.DataFrame)
    assert len(candle_df) == 3


def test_form_candlesticks_empty_df():
    # Tests case where input DataFrame is empty
    df = pd.DataFrame()
    with pytest.raises(KeyError):
        form_candlesticks(df, "1D")


def test_form_candlesticks_invalid_resample_string():
    # Tests case where resample string is invalid
    df = pd.DataFrame(
        {"PRICE": [1, 2, 3, 4, 5]}, index=pd.date_range(start="2023-01-01", periods=5)
    )
    with pytest.raises(ValueError):
        form_candlesticks(df, "abc")


def test_calculate_ema():
    # Positive test case
    series = pd.Series([1, 2, 3, 4, 5])
    ema = calculate_ema(series, 2)
    assert isinstance(ema, pd.Series)

    # Negative test case
    series_with_non_numeric = pd.Series(["1", "a", "3", "4", "5"])
    with pytest.raises(TypeError):
        calculate_ema(series_with_non_numeric, 2)


def test_calculate_ema_zero_period():
    # Tests case where period is zero
    series = pd.Series([1, 2, 3, 4, 5])
    with pytest.raises(ValueError):
        calculate_ema(series, 0)


def test_calculate_ema_negative_period():
    # Tests case where period is negative
    series = pd.Series([1, 2, 3, 4, 5])
    with pytest.raises(ValueError):
        calculate_ema(series, -1)


def test_calculate_ema_empty_series():
    # Tests case where input Series is empty
    series = pd.Series(dtype=float)
    ema = calculate_ema(series, 2)
    assert len(ema) == 0, "Length should be zero for an empty series"
