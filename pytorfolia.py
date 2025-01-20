import streamlit as st
import pandas as pd
from coinbase.wallet.client import Client as CoinbaseClient
from binance.client import Client as BinanceClient
from degiro_connector.trading.api import API as DegiroAPI
# Bit2Me does not have an official Python library, so HTTP requests are used for it
import requests

def fetch_coinbase_portfolio(api_key, api_secret):
    """Fetch portfolio data from Coinbase using the official library."""
    client = CoinbaseClient(api_key, api_secret)
    accounts = client.get_accounts()
    data = []
    for account in accounts['data']:
        if float(account['balance']['amount']) > 0:
            data.append({
                'Asset': account['balance']['currency'],
                'Balance': account['balance']['amount']
            })
    return pd.DataFrame(data)

def fetch_binance_portfolio(api_key, api_secret):
    """Fetch portfolio data from Binance using the official library."""
    client = BinanceClient(api_key, api_secret)
    account = client.get_account()
    balances = account['balances']
    data = []
    for balance in balances:
        if float(balance['free']) > 0 or float(balance['locked']) > 0:
            data.append({
                'Asset': balance['asset'],
                'Free': balance['free'],
                'Locked': balance['locked']
            })
    return pd.DataFrame(data)

def fetch_degiro_portfolio(username, password):
    """Fetch portfolio data from Degiro using the official library."""
    degiro_api = DegiroAPI()
    session = degiro_api.login(username=username, password=password)
    portfolio = degiro_api.get_portfolio_full(session=session)
    data = []
    for item in portfolio:
        data.append({
            'Product': item['name'],
            'ISIN': item['id'],
            'Quantity': item['size'],
            'Price': item['price'],
            'Value': item['value'],
        })
    return pd.DataFrame(data)

def fetch_bit2me_portfolio(api_key):
    """Fetch portfolio data from Bit2Me using HTTP requests."""
    url = "https://api.bit2me.com/v1/user/portfolio"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        portfolio = data.get('portfolio', [])
        return pd.DataFrame(portfolio)
    else:
        st.error(f"Failed to fetch data from Bit2Me: {response.text}")
        return pd.DataFrame()

def main():
    st.title("Portfolio Tracker")

    st.sidebar.header("Settings")
    platform = st.sidebar.selectbox("Platform", ["Coinbase", "Binance", "Degiro", "Bit2Me"])

    if platform == "Coinbase":
        api_key = st.sidebar.text_input("API Key", type="password")
        api_secret = st.sidebar.text_input("API Secret", type="password")
        if st.sidebar.button("Fetch Portfolio"):
            df = fetch_coinbase_portfolio(api_key, api_secret)
            st.write(df)

    elif platform == "Binance":
        api_key = st.sidebar.text_input("API Key", type="password")
        api_secret = st.sidebar.text_input("API Secret", type="password")
        if st.sidebar.button("Fetch Portfolio"):
            df = fetch_binance_portfolio(api_key, api_secret)
            st.write(df)

    elif platform == "Degiro":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Fetch Portfolio"):
            df = fetch_degiro_portfolio(username, password)
            st.write(df)

    elif platform == "Bit2Me":
        api_key = st.sidebar.text_input("API Key", type="password")
        if st.sidebar.button("Fetch Portfolio"):
            df = fetch_bit2me_portfolio(api_key)
            st.write(df)

if __name__ == "__main__":
    main()
