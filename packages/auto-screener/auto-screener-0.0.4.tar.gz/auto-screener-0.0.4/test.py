# test.py

from auto_screener.screening import MultiScreener
from auto_screener.screening import collect_exchanges
from auto_screener.progress import Spinner

MATCHES = [("USD", "USDT")]

ASSETS = [
    "GRT", "FIL", "ETH", "BTC", "AAVE", "AVAX",
    "LTC", "EOS", "NEAR", "APE", "MATIC", "XTZ",
    "DAI", "ADA", "KSM", "DOT", "DOGE", "XLM"
]

PAIRS = {
    "USDT": ASSETS,
    "USD": ASSETS,
    "EUR": ASSETS
}

CURRENCIES = {
    "bittrex": ["USDT", "USD", "EUR"],
    "kraken": ["USDT", "EUR"],
    "binance": ["USDT", "EUR"],
    "kucoin": ["USDT", "EUR"]
}

EXCLUDED = {
    "bittrex": [
        "NEAR/USD", "NEAR/USDT"
    ],
    "kraken": [
        "KSM/USDT", "AAVE/USDT",
        "FIL/USDT", "GRT/USDT",
        "XLM/USDT", "NEAR/USDT"
    ],
    "kucoin": [
        "DAI/USDT"
    ]
}

LENGTH = 0
DELAY = 1

PRO = True

INTERVAL = "1m"
LOCATION = "datasets"

def main() -> None:
    """Runs the program to test the module."""

    exchanges = collect_exchanges(
        pairs=PAIRS, currencies=CURRENCIES,
        excluded=EXCLUDED
    )

    screener = MultiScreener(
        exchanges=exchanges, length=LENGTH,
        delay=DELAY, location=LOCATION,
        pro=PRO, interval=INTERVAL
    )

    with Spinner(message='Initializing Screeners'):
        screener.initialize_screeners()
    # end Spinner

    screener.run(block=True)
# end main

if __name__ == "__main__":
    main()
# end if