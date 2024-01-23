import logging
import os
import time
import pandas as pd
import seaborn as sns
import ta
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import plotly.express as px
from flask import Flask, render_template_string
print(sns.__version__)
print(pd.__version__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("dataprocessor.log"), logging.StreamHandler()]
)

# Dynamic Grid Layout UI   pie chart
class DataProcessor:
    def __init__(self, file_path: str, short_window=10, long_window=20):
        self.file_path = file_path
        self.df = None
        self.short_window = short_window
        self.long_window = long_window
        self.logger = self.configure_logging()

    @staticmethod
    def configure_logging():
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('DataProcessor')

    def read_data(self):
        """Reads the data from the file path."""
        if not os.path.exists(self.file_path):
            self.logger.error(f"File {self.file_path} not found.")
            return
        try:
            self.df = pd.read_csv(self.file_path)
            self.df.replace([np.inf, -np.inf], np.nan, inplace=True)
            self.drop_columns(['EVENT_TYPE', 'SYMBOL'])
            self.logger.info(f"Successfully read data from {self.file_path}")
            self.log_memory_usage()
            self.log_dataframe_shape()
        except Exception as e:
            self.logger.error(
                "Unexpected error while reading data from "
                f"{self.file_path}: {e}",
                exc_info=True
            )

    def drop_columns(self, columns):
        """Drops specified columns if they exist."""
        self.df.drop(columns=columns, errors='ignore', inplace=True)

    @staticmethod
    def handle_missing_values(df):
        """Handles missing values in the dataframe."""
        df.ffill(inplace=True)
        return df

    def log_memory_usage(self):
        """Logs memory usage of the dataframe."""
        try:
            if self.df is None:
                self.logger.error("DataFrame is None. Cannot log memory usage.")
                return
            total_memory_bytes = self.df.memory_usage(deep=True).sum()
            total_memory_kilobytes = total_memory_bytes / 1024
            total_memory_gigabytes = total_memory_bytes / (1024 ** 3)
            self.logger.info(f"The DataFrame uses {total_memory_bytes} bytes, "
                             f"{total_memory_kilobytes:.2f} KB, "
                             f"{total_memory_gigabytes:.2f} GB.")
        except Exception as e:
            self.logger.error(f"Error logging memory usage: {e}", exc_info=True)


    def log_dataframe_shape(self):
        """Logs the number of rows and columns."""
        num_rows, num_cols = self.df.shape
        self.logger.info(
            f"The DataFrame has {num_rows} rows and "
            f"{num_cols} columns."
        )

    def preprocess(self):
        """Preprocesses the dataframe."""
        if self.df is None:
            self.logger.error("Dataframe is None in preprocess method.")
            return

        self.convert_to_datetime()
        self.extract_datetime_components()
        self.handle_missing_values(self.df)
        self.encode_columns()
        self.drop_columns(["EVENT_TIME"])

    def convert_to_datetime(self):
        """Convert TRADE_TIME column to datetime format."""
        self.df['TRADE_TIME'] = pd.to_datetime(
            self.df['TRADE_TIME'], errors='coerce'
        )

    def extract_datetime_components(self):
        """Extract datetime components."""
        self.df['TRADE_YEAR'] = self.df['TRADE_TIME'].dt.year
        self.df['TRADE_MONTH'] = self.df['TRADE_TIME'].dt.month
        self.df['TRADE_DAY'] = self.df['TRADE_TIME'].dt.day
        self.df['TRADE_HOUR'] = self.df['TRADE_TIME'].dt.hour
        self.df['TRADE_MINUTE'] = self.df['TRADE_TIME'].dt.minute
        self.df['TRADE_SECOND'] = self.df['TRADE_TIME'].dt.second

    def encode_columns(self):
        """Encode specified columns."""
        self.df['IS_BUYER_MARKET_MAKER'] = (
            self.df['IS_BUYER_MARKET_MAKER']
            .map({'Y': 1, 'N': 0}, na_action='ignore')
        )

    def compute_trading_indicators(self):
        """Computes various trading indicators for the dataframe."""
        if self.df is None:
            self.logger.error(
                "Dataframe is None in "
                "compute_trading_indicators method."
            )
            return
        # Exponential Moving Average (EMA)
        self.df['EMA_short'] = ta.trend.EMAIndicator(
            self.df['PRICE'],
            window=self.short_window
        ).ema_indicator()
        self.df['EMA_long'] = ta.trend.EMAIndicator(
            self.df['PRICE'],
            window=self.long_window
        ).ema_indicator()
        # Relative Strength Index (RSI)
        self.df['RSI'] = ta.momentum.RSIIndicator(
            self.df['PRICE'], window=self.short_window
        ).rsi()
        # On Balance Volume (OBV)
        self.df['OBV'] = ta.volume.OnBalanceVolumeIndicator(
            self.df['PRICE'], self.df['QUANTITY']
        ).on_balance_volume()
        # Volume Weighted Average Price (VWAP)
        self.df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(
            high=self.df['PRICE'], low=self.df['PRICE'],
            close=self.df['PRICE'], volume=self.df['QUANTITY']
        ).volume_weighted_average_price()
        # Average True Range (ATR)
        self.df['ATR'] = ta.volatility.AverageTrueRange(
            high=self.df['PRICE'], low=self.df['PRICE'],
            close=self.df['PRICE'], window=self.short_window
        ).average_true_range()
        # Parabolic SAR (Stop and Reverse)
        self.df['Parabolic_SAR'] = ta.trend.PSARIndicator(
            high=self.df['PRICE'], low=self.df['PRICE'],
            close=self.df['PRICE']
        ).psar()

    def save_dataframe(self, save_path=None):
        if save_path is None:
            save_path = os.path.join("/data", "works", "codes", "neiron4_model_ML", "47991_data_processorv1.csv")
        try:
            self.df.fillna(0, inplace=True)
            self.df.to_csv(save_path, index=False)
            self.logger.info(f"Dataframe saved to {save_path}")
            print(self.df.head())
        except Exception as e:
            self.logger.error(f"Error saving dataframe: {e}", exc_info=True)

    def plot_distribution(self):
        if self.df is None:
            self.logger.error("DataFrame is None in plot_distribution method.")
            return
        fig = px.histogram(self.df, x="PRICE")
        return fig  # Return the fig object instead of showing it directly

app = Flask(__name__)

@app.route('/plot')
def plot():
    processor = DataProcessor('/data/works/codes/neiron4_model_ML/TABLE_10_10_23_1H.csv')  # Create an instance of DataProcessor
    processor.read_data()
    processor.preprocess()
    processor.compute_trading_indicators()  # Compute the trading indicators
    fig = processor.plot_distribution()  # Call plot_distribution on the processor instance
    plot_html = fig.to_html(full_html=False)
    return render_template_string("<html><body>{{ plot_html | safe }}</body></html>", plot_html=plot_html)


if __name__ == '__main__':
    start_time = time.time()  # Start timing
    file_path = '/data/works/codes/neiron4_model_ML/TABLE_10_10_23_1H.csv'
    processor = DataProcessor(file_path)
    processor.read_data()
    processor.preprocess()
    processor.compute_trading_indicators()  # Compute the trading indicators
    processor.save_dataframe()
    app.run(debug=True)


    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"Execution time: {elapsed_time:.2f} seconds")