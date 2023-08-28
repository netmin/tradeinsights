
# Trade Insights

This project is designed to retrieve trades data from a CSV file, form candlestick charts, and calculate Exponential Moving Averages (EMA) using Python.

![Candlestick Chart](https://i.imgur.com/S6c65Ul.png)
![Candlestick Chart](https://i.imgur.com/HuNyrfp.png)

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/netmin/tradeinsights.git
   cd tradeinsights
   ```

2. Install dependencies using [Poetry](https://python-poetry.org/):
   ```bash
   poetry install
   ```

3. Run the program:
   ```bash
   poetry run python main.py
   ```

## Features

- Retrieve Trades: Reads trades data from a provided CSV file.
- Form Candlesticks: Aggregates trades into candlesticks based on the given time interval.
- Calculate EMA: Calculates Exponential Moving Averages (EMA) for the given length.

## Usage

Modify the `data/prices.csv` file to include your trades data. Adjust the code and parameters in `main.py` to customize the candlestick interval and EMA calculation.
