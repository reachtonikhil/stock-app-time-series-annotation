import streamlit as st
import pandas as pd
import altair as alt
from nsepython import nse_eq

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Indian Stock Price Visualization",
    page_icon="📈",
    layout="centered"
)

# Title of the application
st.title("📈 Indian Stock Price Visualization")

# Input: Stock symbol
stock_symbol = st.text_input("Enter the NSE stock symbol (e.g., RELIANCE):", value="RELIANCE")

# Fetch stock data
if stock_symbol:
    try:
        # Fetch the latest stock data
        stock_data = nse_eq(stock_symbol)
        
        # Extract relevant information
        company_name = stock_data['info']['companyName']
        last_price = stock_data['priceInfo']['lastPrice']
        change = stock_data['priceInfo']['change']
        p_change = stock_data['priceInfo']['pChange']
        day_high = stock_data['priceInfo']['intraDayHighLow']['max']
        day_low = stock_data['priceInfo']['intraDayHighLow']['min']
        previous_close = stock_data['priceInfo']['previousClose']
        
        # Display stock information
        st.subheader(f"{company_name} ({stock_symbol})")
        st.metric(label="Last Price", value=f"₹{last_price}", delta=f"{p_change}%")
        st.write(f"**Day High:** ₹{day_high}")
        st.write(f"**Day Low:** ₹{day_low}")
        st.write(f"**Previous Close:** ₹{previous_close}")
        st.write(f"**Change:** ₹{change} ({p_change}%)")
        
        # Prepare data for visualization
        price_data = {
            'Metric': ['Last Price', 'Day High', 'Day Low', 'Previous Close'],
            'Price': [last_price, day_high, day_low, previous_close]
        }
        df = pd.DataFrame(price_data)
        
        # Create Altair chart
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Metric', sort=None),
            y='Price',
            color='Metric'
        ).properties(
            title=f"Price Metrics for {company_name}"
        )
        
        # Display the chart
        st.altair_chart(chart, use_container_width=True)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
