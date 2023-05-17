import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Function to retrieve cryptocurrency price data from CoinGecko API
def get_crypto_price(crypto_id):
    response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true")
    data = response.json()
    return data.get(crypto_id)

# Function to retrieve cryptocurrency historical price data from CoinGecko API
def get_crypto_history(crypto_id, days):
    response = requests.get(f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}")
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    return df

# Main app code
def main():
    st.title("Cryptocurrency Price Tracker")

    # Cryptocurrency selection
    crypto_id = st.selectbox("Select a cryptocurrency", ["bitcoin", "ethereum", "litecoin"])

    # Current price
    price_data = get_crypto_price(crypto_id)
    price = price_data.get('usd')
    market_cap = price_data.get('usd_market_cap')
    volume_24h = price_data.get('usd_24h_vol')
    change_24h = price_data.get('usd_24h_change')
    last_updated = pd.to_datetime(price_data.get('last_updated_at'), unit='s')
    st.write(f"**Current Price**: ${price:.2f}")
    st.write(f"**Market Cap**: ${market_cap:.2f}")
    st.write(f"**Volume (24h)**: ${volume_24h:.2f}")
    st.write(f"**Change (24h)**: {change_24h:.2f}%")
    st.write(f"Last Updated: {last_updated}")

    # Historical price chart
    days = st.slider("Select the number of days for historical data", 7, 30, 7)
    df = get_crypto_history(crypto_id, days)
    fig = px.line(df, x='Timestamp', y='Price', title=f"{crypto_id.capitalize()} Price Chart")
    st.plotly_chart(fig)

# Run the app
if __name__ == '__main__':
    main()
