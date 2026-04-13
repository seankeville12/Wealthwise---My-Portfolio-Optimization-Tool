import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from datetime import datetime
import feedparser
from scipy.optimize import minimize
from functools import reduce
import plotly.graph_objects as go


#background
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #3b5998, #ffffff); /* Blue to white gradient */
        background-attachment: fixed;
        color: #000000; /* Black text for contrast */
    }
    .stApp {
        background: linear-gradient(to bottom, #3b5998, #ffffff); /* Blue to white gradient */
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Styled Title Section
st.markdown(
    """
    <style>
        .title-box {
            margin: 20px auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 80%;
        }
        .title-box h1 {
            font-size: 36px;
            font-weight: bold;
            margin: 0;
            color: #003366;
        }
        .title-box p {
            font-size: 18px;
            margin: 10px 0 0;
            color: #333333;
        }
    </style>
    <div class="title-box">
        <h1>Welcome to Wealthwise - The Investment Portfolio Optimisation Tool For You</h1>
        <p>Our platform customises portfolio allocations of S&P500 stocks based on your risk tolerance and budget, helping you make informed investment decisions. Enter your details in the sidebar and explore tailored recommendations in the tabs below.
    </div>
    """,
    unsafe_allow_html=True,
)



# Message for top of every section
st.markdown("""
    ## Portfolio Optimization Section
    Below you can view and evaluate your custom portfolio allocation.
""")

options = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5-9": 7,
    "10-14": 13,
    "15-19": 17,
    "20-24": 22,
    "25-29": 27,
    "30-34": 32,
    "35-39": 37,
    "40-44": 42,
    "45-50": 47.5
}


# Sidebar for user inputs
st.sidebar.header("Input Portfolio Information")
num_stocks = st.sidebar.number_input("Select the Number of Stocks for your Portfolio", min_value=1, max_value=500, value=10)
budget = st.sidebar.number_input("Maximum Portfolio Budget ($)", min_value=1000.0, max_value = 1000000.0, value=10000.0)
selected_option = st.sidebar.selectbox(
    "Set Risk Tolerance (VaR %)",
    options=list(options.keys()),  # Display the range labels
    index=0  # Default to the first option ("1")
)
risk_tolerance = options[selected_option]



# Navigation
page = st.radio("Choose a section", [
    "Portfolio Optimization",
    "Risk Metrics",
    "Real-Time News",
    "Portfolio Value Forecast"
])

# Load S&P 500 tickers
tickers_list = ["AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEP", "AES", "AFL",
    "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT",
    "AMTM", "AMZN", "ANET", "ANSS", "AON", "AOS", "APA", "APD", "APH", "APTV", "ARE", "ATO", "AVB", "AVGO", "AVY",
    "AWK", "AXON", "AXP", "AZO", "BA", "BAC", "BALL", "BAX", "BBY", "BDX", "BEN", "BF.B", "BG", "BIIB", "BK", "BKNG",
    "BKR", "BLDR", "BLK", "BMY", "BR", "BRK.B", "BRO", "BSX", "BWA", "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT",
    "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CE", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF",
    "CL", "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COO", "COP", "COR", "COST", "CPAY", "CPB",
    "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS", "CTLT", "CTRA", "CTSH", "CTVA", "CVS", "CVX",
    "CZR", "D", "DAL", "DAY", "DD", "DE", "DECK", "DELL", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOC",
    "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA", "DVN", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL",
    "ELV", "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ERIE", "ES", "ESS", "ETN", "ETR", "EVRG", "EW",
    "EXC", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FI", "FICO", "FIS", "FITB",
    "FMC", "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GDDY", "GE", "GEHC", "GEN", "GEV", "GILD", "GIS", "GL",
    "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC", "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HES",
    "HIG", "HII", "HLT", "HOLX", "HON", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", "HWM", "IBM", "ICE",
    "IDXX", "IEX", "IFF", "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ",
    "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", "JNPR", "JPM", "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KKR", "KLAC",
    "KMB", "KMI", "KMX", "KO", "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", "LIN", "LKQ", "LLY", "LMT", "LNT", "LOW",
    "LRCX", "LULU", "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ",
    "MDT", "MET", "META", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR",
    "MRK", "MRNA", "MRO", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM",
    "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI", "O",
    "ODFL", "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", "PANW", "PARA", "PAYC", "PAYX", "PCAR", "PCG", "PEG",
    "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PLTR", "PM", "PNC", "PNR", "PNW", "PODD", "POOL",
    "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PWR", "PYPL", "QCOM", "QRVO", "RCL", "REG", "REGN", "RF", "RJF", "RL",
    "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB", "SMCI",
    "SNA", "SNPS", "SO", "SOLV", "SPG", "SPGI", "SRE", "STE", "STLD", "STT", "STX", "STZ", "SW", "SWK", "SWKS", "SYF",
    "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TFX", "TGT", "TJX", "TMO", "TMUS", "TPR",
    "TRGP", "TRMB", "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO", "TXN", "TXT", "TYL", "UAL", "UBER", "UDR",
    "UHS", "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VICI", "VLO", "VLTO", "VMC", "VRSK", "VRSN", "VRTX",
    "VST", "VTR", "VTRS", "VZ", "WAB", "WAT", "WBA", "WBD", "WDC", "WEC", "WELL", "WFC", "WM", "WMB", "WMT", "WRB",
    "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XYL", "YUM", "ZBH", "ZBRA", "ZTS"
]

def optimize_portfolio_max_return(tickers_data, num_stocks, budget, risk_tolerance):
    """
    Optimises portfolio allocation to maximize expected return based on the user's risk tolerance.

    The function recommends an investment strategy that maximizes returns while considering the user's risk tolerance.
    It uses historical data on returns and volatility to calculate a risk-adjusted return metric and selects the
    top stocks based on this metric. The function then calculates optimal weights and investment amounts for the selected
    stocks, and returns the optimised portfolio along with the portfolio's expected return.

    Parameters:
    - tickers_data (pd.DataFrame): DataFrame containing stock tickers, expected returns, and volatility data.
    - num_stocks (int): The number of stocks to include in the optimised portfolio.
    - budget (float): Total budget to allocate across the selected stocks.
    - risk_tolerance (float): Risk tolerance level (on a scale of 1-50), with higher values indicating higher risk tolerance.

    Returns:
    - pd.DataFrame: Optimized portfolio details including tickers, expected return, volatility, weight, and investment allocation.
    - float: The expected portfolio return.
    """

    def recommend_risk_free_investment():
        """
        Recommends a safer investment in government bonds if the user's risk tolerance is low.

        If the user's risk tolerance is 10% or lower, this function suggests allocating more funds to government bonds.
        It provides an example bond with a 3% annual yield and recommends adjusting the portfolio allocation accordingly.

        Returns:
        None
        """
        bond_yield = 0.03  # Example annual yield for a government bond (3%)
        st.subheader("Recommended Investment: Government Bonds")
        st.write(f"Since your risk tolerance is low, consider allocating more to government bonds.")
        st.write(f"A government bond with an annual yield of {bond_yield * 100:.2f}% could be a safer choice.")
        st.write("You can adjust your portfolio allocation to maximize returns with lower risk.")
        st.write(f"Suggested allocation: {risk_tolerance * 10:.2f}% stocks, {(10-risk_tolerance) * 10:.2f}% bonds.")

    # If the user's risk tolerance is low (<=10), suggest government bonds
    if risk_tolerance <= 10:
        recommend_risk_free_investment()

    # Adjust the risk tolerance factor (1-50 scale)
    risk_weight = risk_tolerance / 50

    # Calculate risk-adjusted return combining expected return and volatility based on risk tolerance
    tickers_data['Risk_Adjusted_Return'] = (
        tickers_data['Expected Return'] * risk_weight - tickers_data['Volatility'] * (1 - risk_weight)
    )

    # Select top stocks based on risk-adjusted return
    top_stocks = tickers_data.nlargest(num_stocks, 'Risk_Adjusted_Return')

    # Calculate weights for each stock based on the risk-adjusted return
    total_risk_adjusted_return = top_stocks['Risk_Adjusted_Return'].sum()
    top_stocks['Weight'] = top_stocks['Risk_Adjusted_Return'] / total_risk_adjusted_return

    # Filter out stocks with zero or negative weight
    top_stocks = top_stocks[top_stocks['Weight'] > 0]

    # Allocate investment amounts based on weights
    top_stocks['Investment'] = top_stocks['Weight'] * budget

    # Round the Investment values to two decimal places
    top_stocks['Investment'] = top_stocks['Investment'].round(2)

    # Calculate the overall expected return of the portfolio
    portfolio_return = (top_stocks['Expected Return'] * top_stocks['Weight']).sum()

    # Return the optimized portfolio and portfolio return
    return top_stocks[['Ticker', 'Expected Return', 'Volatility', 'Weight', 'Investment']], portfolio_return


def portfolio_optimization():
    """
    Handles the portfolio optimisation process by calling the optimisation function and displaying the results.

    This function uses user inputs such as the number of stocks, budget, and risk tolerance to optimise a portfolio using
    the `optimize_portfolio_max_return` function. It displays the optimized portfolio's allocation, expected return,
    and visualizes the investment distribution.

    Returns:
    None
    """
    st.title("Portfolio Optimisation to Maximize Expected Return")

    # Check if the stock data is available for optimization
    if not tickers_data.empty:
        # Perform the portfolio optimization
        optimized_portfolio, portfolio_return = optimize_portfolio_max_return(tickers_data, num_stocks, budget, risk_tolerance)

        if not optimized_portfolio.empty:
            st.write(f"Expected Portfolio Return: {portfolio_return:.2%}")

            # Store the optimized portfolio and return in session state
            st.session_state['optimized_portfolio'] = optimized_portfolio
            st.session_state['portfolio_return'] = portfolio_return

            # Display the optimized portfolio allocation as a table
            st.subheader("Optimized Portfolio Allocation")
            st.write(optimized_portfolio[['Ticker', 'Investment', 'Weight', 'Expected Return', 'Volatility']])

            # Create a simulated time series of portfolio values (daily over the past year)
            dates = pd.date_range(start="2023-11-14", end="2024-11-14", freq='B')
            daily_returns = np.dot(optimized_portfolio['Expected Return'], optimized_portfolio['Weight'])
            portfolio_values = (1 + daily_returns / 252) ** np.arange(len(dates)) * budget
            portfolio_value = pd.Series(portfolio_values, index=dates)

            # Store portfolio value in session state for use in other sections
            st.session_state['portfolio_value'] = portfolio_value

            # Display the investment distribution as a bar chart
            st.subheader("Investment Distribution")

            font_size = 10 if len(optimized_portfolio['Ticker']) < 20 else 8 if len(optimized_portfolio['Ticker']) < 50 else 6 if len(optimized_portfolio['Ticker']) < 65 else 4 if len(optimized_portfolio['Ticker']) < 85 else 3
            fig = go.Figure()

            # Add bars to the chart representing investment allocation
            fig.add_trace(go.Bar(
                x=optimized_portfolio['Ticker'],  # Stock tickers
                y=optimized_portfolio['Investment'],  # Investment values
                text=optimized_portfolio['Ticker'],  # Hover text (stock ticker)
                hoverinfo='text+y',  # Display ticker and investment on hover
                marker=dict(color='orange'),  # Bar color
            ))

            # Customize the layout of the chart
            fig.update_layout(
                title="Investment Distribution Across S&P 500 Stocks",
                xaxis_title="Stock Ticker",
                yaxis_title="Investment ($)",
                xaxis=dict(
                    tickangle=90,  # Rotate tickers vertically
                    tickfont=dict(size=font_size),  # Adjust font size dynamically
                ),
                template="plotly_white",  # Use a clean white template
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),  # Hover label style
            )

            # Display the chart in the Streamlit app
            st.plotly_chart(fig, use_container_width=True, config={'modeBarButtonsToRemove': ['select2d', 'lasso2d']})

            # Create an expandable section to explain the optimization methodology
            with st.expander("Portfolio Optimisation Methodology"):
                st.markdown("""
                ### Methodology
                The portfolio optimisation algorithm follows these steps:

                1. **Input Collection:**
                   - User inputs:
                     - Number of stocks to include in the portfolio.
                     - Maximum budget.
                     - Risk tolerance (VaR percentage).

                2. **Data Analysis:**
                   - Use historical data to calculate:
                     - **Expected Return**: Average historical return for each stock.
                     - **Volatility**: Standard deviation of historical returns.
                     - **Risk-Adjusted Return**: A metric that balances expected return and risk based on user-defined risk tolerance.

                     Risk Adjusted Return = (Expected Return x Risk Weight) - Volatility x (1 - Risk Weight)

                3. **Optimization Process:**
                   - Rank stocks by their Risk-Adjusted Return.
                   - Select the top `N` stocks (based on user input) while staying within the budget.
                   - Allocate weights to selected stocks proportionally based on Risk-Adjusted Return.

                4. **Portfolio Metrics:**
                   - Calculate the overall **Expected Return**, **Weighted Volatility**, and **Portfolio Beta**.

                5. **Visualization:**
                   - Present results using tables and charts for better understanding.

                ### Why Use This Methodology?
                - **Customizability**: Tailored to your risk tolerance.
                - **Simplicity**: Combines key metrics into one optimized measure.
                - **Efficiency**: Finds the best-performing stocks within your budget.
                """)
        else:
            st.error("The optimized portfolio does not contain enough data.")
    else:
        st.write("No data available for the selected tickers.")


# Define the function to get stock data from Yahoo Finance
def get_stock_data(tickers, start, end):
    """
    Fetch adjusted closing prices for given stock tickers over a specified date range from Yahoo Finance.

    Parameters:
    - tickers (list or str): List of stock ticker symbols or a single ticker string.
    - start (str): Start date for fetching historical data in 'YYYY-MM-DD' format.
    - end (str): End date for fetching historical data in 'YYYY-MM-DD' format.

    Returns:
    - DataFrame: Adjusted closing prices of the specified stocks over the given date range.
    """
    stock_data = yf.download(tickers, start=start, end=end)['Adj Close']
    return stock_data

# Main function to display risk metrics
def risk_metrics():
    """
    Calculate and display key risk metrics for the user's optimised portfolio.

    The function assumes that an optimized portfolio has been created and stored in
    Streamlit session state under 'optimized_portfolio'. The metrics include:
    - Annualised Volatility
    - Portfolio Beta
    - Value-at-Risk (VaR) at a 95% confidence level

    If no optimised portfolio is found, an error message is displayed.
    """
    st.title("Risk Metrics")

    # Check if 'optimized_portfolio' is available in session state
    if 'optimized_portfolio' in st.session_state:
        optimized_portfolio = st.session_state['optimized_portfolio']
        tickers = optimized_portfolio['Ticker'].tolist()
        portfolio_weights = optimized_portfolio['Weight'].values  # Extract weights from the optimized portfolio
    else:
        st.write("No optimized portfolio found. Please run the Portfolio Optimization section.")
        return

    # Fetch portfolio historical data for 1 year (14/11/2023 to 14/11/2024)
    stock_data = get_stock_data(tickers, "2023-11-14", "2024-11-14")
    portfolio_returns = stock_data.pct_change().dropna()

    # Calculate the individual volatilities of each stock in the portfolio
    volatilities = portfolio_returns.std() * np.sqrt(252)

    # Calculate the weighted volatility (using portfolio weights)
    weighted_volatility = np.dot(portfolio_weights, volatilities)

    # Fetch S&P 500 historical data for market comparison
    sp500_data = get_stock_data('^GSPC', "2023-11-14", "2024-11-14")
    sp500_returns = sp500_data.pct_change().dropna()

    # Align portfolio returns with market returns
    aligned_returns = pd.concat([portfolio_returns.mean(axis=1), sp500_returns], axis=1).dropna()
    portfolio_returns_aligned = aligned_returns.iloc[:, 0]
    market_returns_aligned = aligned_returns.iloc[:, 1]

    # Calculate Beta
    cov_matrix_portfolio_market = np.cov(portfolio_returns_aligned, market_returns_aligned)
    portfolio_beta = cov_matrix_portfolio_market[0, 1] / np.var(market_returns_aligned)

    # Calculate portfolio returns weighted by portfolio weights
    portfolio_daily_returns = (portfolio_returns * portfolio_weights).sum(axis=1)

    # Calculate 95% Value-at-Risk (VaR) using the 5th percentile of the portfolio returns
    var_95 = np.percentile(portfolio_daily_returns.dropna(), 5)  # Historical 5th percentile of portfolio returns

    # Display the risk metrics
    st.subheader("Risk Metrics")
    st.write(f"**Annualized Volatility (Weighted)**: {weighted_volatility:.2%}" if weighted_volatility != 0 else "Annualized Volatility: Not Available")
    st.write(f"**Portfolio Beta**: {portfolio_beta:.2f}")
    st.write(f"**Value-at-Risk (95% Confidence Level)**: {var_95:.2%}")  # VaR at 95% Confidence Level

    # Create a dropdown to explain and interpret the risk metrics
    with st.expander("Risk Metrics Explained and Interpreted"):
        st.markdown("""
        ### Risk Metrics Explained
        **1. Annualized Volatility (Weighted):**
        - Measures the degree of variation in the portfolio's returns over a year.
        - Higher volatility indicates higher risk and larger potential swings in returns.
        """)

        # Interpretation of Volatility
        if weighted_volatility < 0.15:
            st.write("📉 Your portfolio's volatility is low, indicating relatively stable returns. This is suitable for conservative investors.")
        elif 0.15 <= weighted_volatility <= 0.30:
            st.write("📊 Your portfolio's volatility is moderate, balancing risk and reward. This is suitable for moderate risk-tolerant investors.")
        else:
            st.write("📈 Your portfolio's volatility is high, indicating larger potential returns but also higher risk. This is suitable for aggressive investors.")

        st.markdown("""
        **2. Portfolio Beta:**
        - Represents the sensitivity of the portfolio's returns to the overall market.
        - A beta of 1 means the portfolio moves in line with the market,
          while a beta > 1 indicates higher sensitivity to market changes.
        """)

        # Interpretation of Beta
        if portfolio_beta < 0.8:
            st.write("🛡️ Your portfolio has a low beta, meaning it is less sensitive to market changes and may perform better during market downturns.")
        elif 0.8 <= portfolio_beta <= 1.2:
            st.write("🔄 Your portfolio has a beta close to 1, meaning it generally follows the market's movements.")
        else:
            st.write("⚡ Your portfolio has a high beta, meaning it is highly sensitive to market changes and may experience higher gains or losses.")

        st.markdown("""
        **3. Value-at-Risk (VaR):**
        - Estimates the potential loss in portfolio value at a 95% confidence level.
        - For example, a VaR of -5% means there is a 95% chance the portfolio will not lose more than 5% in a given period.
        """)

        # Interpretation of VaR
        if var_95 > -0.05:
            st.write("✅ Your portfolio's Value-at-Risk is low, indicating a minimal risk of significant losses over the specified period.")
        elif -0.10 <= var_95 <= -0.05:
            st.write("⚠️ Your portfolio's Value-at-Risk is moderate, indicating some potential for losses but still within acceptable limits for many investors.")
        else:
            st.write("❌ Your portfolio's Value-at-Risk is high, suggesting a significant risk of large losses. This may not be suitable for risk-averse investors.")

def real_time_news():
    """
    Displays real-time news for portfolio stocks based on the optimised portfolio.
    Allows users to search for a specific stock ticker and view relevant news articles.

    The function performs the following steps:
    - Displays a search bar to enter a stock ticker.
    - Checks if an optimised portfolio exists in the session state.
    - Merges the portfolio with logo data to show logos of the stocks.
    - Fetches real-time news articles related to the selected ticker using Google News RSS feed.
    - Displays logos (if available) and news articles for each ticker in the portfolio.
    """
    st.title("Real-Time News for Portfolio Stocks")

    # Add a search bar for users to enter a stock ticker
    search_ticker = st.text_input("Search for a stock ticker to view its news", "").strip().upper()

    # Ensure there is an optimized portfolio in the session state
    if 'optimized_portfolio' in st.session_state:
        optimized_portfolio = st.session_state['optimized_portfolio']
        tickers = optimized_portfolio['Ticker'].tolist()

        # Merge with tickers_data to get logo URLs
        merged_data = pd.merge(
            optimized_portfolio,
            tickers_data[['Ticker', 'Logo URL']],
            on='Ticker',
            how='left'
        )

        # Filter for the searched ticker if a search is performed
        if search_ticker:
            if search_ticker in tickers:
                merged_data = merged_data[merged_data['Ticker'] == search_ticker]
            else:
                st.warning(f"Ticker '{search_ticker}' not found in the optimized portfolio.")
                return

        # Loop through the filtered merged data to display news and logos
        for _, row in merged_data.iterrows():
            ticker = row['Ticker']
            logo_url = row.get('Logo URL', None)

            st.subheader(f"Real-Time News for {ticker}")

            # Display logo if URL is valid
            if isinstance(logo_url, str) and logo_url.startswith(("http://", "https://")):
                st.image(logo_url, width=70)
            else:
                st.write(f"Logo not available for {ticker}")

            # Fetch and display news
            news = get_news_rss(ticker)
            if news:
                for entry in news:
                    st.write(f"[{entry.title}]({entry.link})")
            else:
                st.write("No recent news available for this ticker.")
    else:
        st.write("Please go to the 'Portfolio Optimization' section first to generate a portfolio.")


# Example function to load CSV data with logo URLs
def load_csv_data_with_logos(file_path):
    data = pd.read_csv(file_path)
    # Ensure the CSV contains required columns
    required_columns = ['Ticker', 'Expected Return', 'Volatility', 'Logo URL']
    if all(col in data.columns for col in required_columns):
        return data
    else:
        st.error("CSV file does not contain required columns: 'Ticker', 'Expected Return', 'Volatility', 'Logo URL'.")
        return pd.DataFrame()

def get_news_rss(ticker):
        """Fetch the latest news articles for a given stock ticker using an RSS feed from Google News.

        Parameters:
        - ticker (str): The stock ticker for which to fetch news.

        Returns:
        - list: A list of the top 5 latest news entries related to the ticker.
        """
        rss_url = f"https://news.google.com/rss/search?q={ticker}+stock"
        feed = feedparser.parse(rss_url)
        return feed.entries[:5]

# Load CSV data with Portfolio Return and Volatility
def load_csv_data(file_path):
        """Load a CSV file containing portfolio data and ensure it includes the required columns.

        Parameters:
        - file_path (str): The file path of the CSV to be loaded.

        Returns:
        - pandas.DataFrame: The data from the CSV if it contains the required columns ('Ticker', 'Expected Return', 'Volatility').
        - If the required columns are missing, an error is displayed, and an empty DataFrame is returned.
            """
        data = pd.read_csv(file_path)
        # Ensure the CSV contains 'Ticker', 'Expected Return', and 'Volatility' columns
        if 'Ticker' in data.columns and 'Expected Return' in data.columns and 'Volatility' in data.columns:
            return data
        else:
            st.error("CSV file does not contain required columns: 'Ticker', 'Expected Return', 'Volatility'.")
            return pd.DataFrame()

# Load the CSV file with stock data
file_path = "sp500data.csv"
tickers_data = load_csv_data(file_path)

# MONTE CARLO SIMULATION

# Portfolio Return and Volatility from the CSV
portfolio_return = tickers_data['Expected Return'].mean()  # Mean of expected returns
portfolio_volatility = tickers_data['Volatility'].mean()  # Mean of volatilities

# Function to simulate future portfolio values
def simulate_portfolio_value(initial_value, return_mean, volatility, num_simulations, num_days):
    """
    Simulates the future portfolio values using Monte Carlo simulations.

    Parameters:
    - initial_value (float): The initial portfolio value
    - return_mean (float): The average expected return of the portfolio
    - volatility (float): The volatility of the portfolio
    - num_simulations (int): The number of simulation paths
    - num_days (int): The number of days to simulate (future horizon)

    Returns:
    - future_values (array): Simulated future portfolio values at the end date
    """
    daily_return = return_mean / 252  # Assuming 252 trading days in a year
    daily_volatility = volatility / np.sqrt(252)

    # Simulate portfolio values
    simulated_values = []
    for _ in range(num_simulations):
        daily_returns = np.random.normal(daily_return, daily_volatility, num_days)
        portfolio_values = initial_value * np.cumprod(1 + daily_returns)  # Compound the returns
        simulated_values.append(portfolio_values[-1])  # Save the final value

    return np.array(simulated_values)

# Portfolio Value Forecast Calculator function
def investment_return_calculator():
    """
    This function allows the user to simulate future portfolio values using a Monte Carlo simulation.
    It calculates the potential future value of the portfolio based on its expected return and volatility.
    The function then visualizes the distribution of simulated values, displaying a 95% confidence interval
    and the mean estimate of the portfolio's future value.

    User input includes:
    - Initial portfolio value
    - End date for the forecast

    The function then:
    - Runs Monte Carlo simulations to predict portfolio values
    - Displays results including the mean estimate and confidence intervals
    - Plots the simulation distribution with key statistical indicators (mean, 2.5%, and 97.5% percentiles)
    """

    st.title("Portfolio Value Forecast")

    # Get user input for portfolio initial value and simulation end date
    initial_value = budget  # Assuming 'budget' is predefined elsewhere in your code
    end_date = st.date_input("Select End Date")

    # Calculate the number of days to simulate based on the selected end date
    current_date = pd.to_datetime("today").date()  # Convert to datetime.date object
    num_days = (end_date - current_date).days  # Now this will work because both are datetime.date

    if num_days <= 0:
        st.error("The end date must be in the future.")
        return

    # Number of simulations
    num_simulations = 10000

    # Run Monte Carlo simulations
    simulated_values = simulate_portfolio_value(initial_value, portfolio_return, portfolio_volatility, num_simulations, num_days)

    # Calculate 95% Confidence Interval
    lower_bound = np.percentile(simulated_values, 2.5)  # 2.5th percentile
    upper_bound = np.percentile(simulated_values, 97.5)  # 97.5th percentile
    mean_estimate = np.mean(simulated_values)

    # Display results
    st.subheader(f"Portfolio Value Estimate on {end_date.strftime('%Y-%m-%d')}")
    st.write(f"Simulated mean portfolio value: ${mean_estimate:,.2f}")
    st.write(f"95% Confidence Interval: \${lower_bound:,.2f} - \${upper_bound:,.2f}")

    # Plot the simulation results
    fig, ax = plt.subplots()
    ax.hist(simulated_values, bins=50, edgecolor='black', color='orange', alpha=0.7)
    ax.axvline(lower_bound, color='red', linestyle='dashed', label=f'2.5% Percentile: ${lower_bound:,.2f}')
    ax.axvline(upper_bound, color='red', linestyle='dashed', label=f'97.5% Percentile: ${upper_bound:,.2f}')
    ax.axvline(mean_estimate, color='green', linestyle='solid', label=f'Mean Estimate: ${mean_estimate:,.2f}')
    ax.set_title('Monte Carlo Simulation of Future Portfolio Values')
    ax.set_xlabel('Portfolio Value ($)')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)

    # Create dropdown to explain the Monte Carlo Simulation
    with st.expander("Monte Carlo Simulation Explained and Interpreted"):
        st.markdown("""
        ### Monte Carlo Simulation
        **1. Explanation:**
        - The Monte Carlo simulation is a statistical method used to predict potential future portfolio values by running thousands of simulations (10,000 in this case).
        - This model takes into account historical returns and volatility to simulate daily returns into the future.
""")
        st.markdown(f"""
        **2. Interpretation of Results:**
        - Simulated Mean Portfolio Value - This is the best prediction of the future value of the portfolio based on the simulation.
        - Percentiles - In 95 percent of cases, the portfolio value on the date selected will fall between the lower bound (\${lower_bound:,.2f}) and the upper bound (\${upper_bound:,.2f}) based on the model.
        """)

        st.markdown("""
        **3. Reasons for Using a Monte Carlo Simulation:**
        - Risk and Uncertainty - The model captures the risk inherent in stock market investments by simulating a range of possible outcomes.
        - Better Decision-Making - Instead of relying on a single point estimate, it provides a realistic view of the potential risks and returns of the selected portfolio.
""")

# Placeholder for page navigation based on the selected page
# Render the selected page
if page == "Portfolio Optimization":
    portfolio_optimization()
elif page == "Risk Metrics":
    risk_metrics()
elif page == "Real-Time News":
    real_time_news()
elif page == "Portfolio Value Forecast":
    investment_return_calculator()