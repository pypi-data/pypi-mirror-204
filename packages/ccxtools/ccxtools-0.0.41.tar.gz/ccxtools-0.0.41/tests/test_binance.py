import pytest
import math
from src.ccxtools.tools import get_env_vars
from src.ccxtools.binance import Binance


@pytest.fixture
def config():
    return get_env_vars()


@pytest.fixture
def binance(config):
    return Binance('', 'USDT', config)


def test_get_contract_sizes(binance):
    sizes = binance.get_contract_sizes()
    assert isinstance(sizes, dict)
    assert sizes['BTC'] == 0.001
    assert sizes['ETH'] == 0.001


def test_get_max_position_qtys(binance):
    qtys = binance.get_max_position_qtys()
    assert 'BTC' in qtys
    assert isinstance(qtys['BTC'], int)
    assert 'ETH' in qtys
    assert isinstance(qtys['ETH'], int)


def test_get_balance(binance):
    # Test input Start
    ticker = 'USDT'
    balance_input = 4109
    # Test input End

    balance = binance.get_balance(ticker)
    assert balance_input * 0.9 <= balance <= balance_input * 1.1


def test_get_position(binance):
    # Test input Start
    ticker = 'LPT'
    amount = -36
    # Test input End
    position = binance.get_position(ticker)
    assert isinstance(position, float)
    if amount:
        assert math.isclose(position, amount)


def test_post_market_order(binance):
    # Test input Start
    ticker = 'XRP'
    amount = 20
    # Test input End

    last_price = binance.ccxt_inst.fetch_ticker(f'{ticker}USDT')['last']

    buy_open_price = binance.post_market_order(ticker, 'buy', 'open', amount)
    assert 0.9 * last_price < buy_open_price < 1.1 * last_price
    sell_close_price = binance.post_market_order(ticker, 'sell', 'close', amount)
    assert 0.9 * last_price < sell_close_price < 1.1 * last_price
    sell_open_price = binance.post_market_order(ticker, 'sell', 'open', amount)
    assert 0.9 * last_price < sell_open_price < 1.1 * last_price
    buy_close_price = binance.post_market_order(ticker, 'buy', 'close', amount)
    assert 0.9 * last_price < buy_close_price < 1.1 * last_price


def test_get_precise_order_amount(binance):
    ticker = 'BTC'
    ticker_amount = 0.00111
    assert binance.get_precise_order_amount(ticker, ticker_amount) == 0.001


def test_get_max_trading_qtys(binance):
    max_qtys = binance.get_max_trading_qtys()
    assert isinstance(max_qtys, dict)
    assert 'BTC' in max_qtys
    assert max_qtys['BTC'] == 120
