import click
import yfinance as yf
import sys
import os
from pathlib import Path
import logging

# https://pypi.org/project/yfinance/
# https://ranaroussi.github.io/yfinance/
# https://ranaroussi.github.io/yfinance/reference/index.html

# =============== PATH

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, (parent_dir))

# =============== LOGGING

# set up logging to capture and display logs
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s."
)
logger = logging.getLogger(__name__)

# =============== STOCKS GROUP

@click.group(help="A CLI tool for executing yfinance API calls.")
def stocks():
    pass

# =============== STOCKS COMMAND

@click.command(help="Fetch info for a stock ticker from Yahoo Finance.")
@click.option("-i", "--info", required=True, help="Stock ticker (as listed on Yahoo Finance), e.g., 'GOOGL', 'TSLA', 'AMZN'.")
def get_info(info):
    """
    A CLI tool for executing yfinance API calls to fetch stock market data.\n\n"
         "Note: The ticker symbol must match Yahoo Finance's symbols exactly.\n"
         "Example: 'AAPL' for Apple, 'TSLA' for Tesla. Not all company names are available as tickers.\n"
         "Private companies like 'Winking Studios' may not be listed.
    """
    try:
        # attempt to fetch the stock information using Yahoo Finance's Ticker method
        dat = yf.Ticker(info)
        # retrieve information about the stock
        data = dat.info
        logger.info("Stock information:")
        # loop through the data and print each key-value pair
        for k, v in data.items():
            print(f"{k}: {v}")
    
    # handle ValueError (if any) and log it
    except ValueError as e:
        logger.error(f"Value error: {e}")
    
    # handle any other unexpected exceptions and log them
    except Exception as e:
        logger.error(f"Exception error: {e}")


# add command to stocks group
stocks.add_command(get_info)

# =============== MAIN ENTRYPOINT

if __name__ == "__main__":
    stocks()
