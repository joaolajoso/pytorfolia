import streamlit as st
import requests
import pandas as pd

def fetch_crypto_portfolio(api_key, api_secret, platform):
    """Fetch crypto portfolio from the given platform."""
    if platform == "Coinbase":
        url = f"https://api.coinbase.com/v2/accounts"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
    elif platform == "Binance":
        # Binance API requires a signed request (not implemented here)
        response = requests.get("https://api.binance.com/api/v3/account", headers={})
    elif platform == "Bit2Me":
        response = requests.get("https://api.bit2me.com/v1/user/portfolio", headers={})
    else:
        return None

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data from {platform}: {response.text}")
        return None

def fetch_stock_portfolio(api_key, platform):
    """Fetch stock portfolio from the given platform."""
    if platform == "Degiro":
        # Degiro API (you might need to implement authentication)
        response = requests.get("https://trading-api.degiro.com/v1/portfolio", headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from Degiro: {response.text}")
            return None
    else:
        st.error("Unsupported platform")
        return None

def main():
    st.title("Portfolio Tracker")

    st.sidebar.header("Settings")
    api_key = st.sidebar.text_input("API Key", type="password")
    api_secret = st.sidebar.text_input("API Secret", type="password")
    platform = st.sidebar.selectbox("Platform", ["Coinbase", "Binance", "Bit2Me", "Degiro"])

    if st.sidebar.button("Fetch Portfolio"):
        if platform in ["Coinbase", "Binance", "Bit2Me"]:
            data = fetch_crypto_portfolio(api_key, api_secret, platform)
        elif platform == "Degiro":
            data = fetch_stock_portfolio(api_key, platform)
        else:
            st.error("Unsupported platform")
            return

        if data:
            st.subheader(f"Portfolio from {platform}")
            # Process and display data (example for Coinbase)
            if platform == "Coinbase" and "data" in data:
                df = pd.DataFrame(data["data"])
                df = df[["name", "balance", "currency"]]
                st.write(df)
            else:
                st.json(data)

if __name__ == "__main__":
    main()
