# Wealthwise - Investment Portfolio Optimization Tool
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
## Overview
**Wealthwise** is an interactive investment portfolio optimization web application built with Streamlit.
It helps users create customized S&P 500 portfolios based on their risk tolerance and budget, then provides comprehensive analytics
including risk metrics, real-time news, and future value forecasting.
## Live Demo Features
The application guides users through four main sections:
### 1. Portfolio Optimization
- Select number of stocks (1-500) from S&P 500
- Set maximum portfolio budget ($1,000 - $1,000,000)
- Choose risk tolerance (1-50% VaR scale)
- Automatically generates optimized portfolio allocations
- Visualizes investment distribution with interactive bar charts
### 2. Risk Metrics
- **Annualized Volatility** - Measures portfolio return variation
- **Portfolio Beta** - Market sensitivity indicator
- **Value-at-Risk (VaR)** - 95% confidence level loss estimation
- Includes interpretative guidance for each metric
### 3. Real-Time News
- Search and view latest news for any portfolio stock
- Fetches RSS feeds from Google News
- Displays stock logos where available
### 4. Portfolio Value Forecast
- Monte Carlo simulation (10,000 paths)
- Projects future portfolio values based on historical returns
- Provides 95% confidence intervals
- Visualizes simulation distribution
## Key Features
- **Risk-Adjusted Optimization**: Balances expected returns against volatility based on user's risk tolerance
- **Dynamic Portfolio Allocation**: Weights stocks proportionally by risk-adjusted return
- **Robust Data Source**: Real-time S&P 500 data via Yahoo Finance API
- **Monte Carlo Forecasting**: Statistical simulation for future value prediction
- **Interactive Visualizations**: Plotly charts with responsive design
- **Educational Components**: Expandable sections explaining methodology
## Technology Stack
- **Frontend/UI**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Financial Data**: yfinance
- **Visualization**: Matplotlib, Plotly
- **Optimization**: SciPy
- **News Feed**: feedparser (RSS)
### Prerequisites
```bash
Python 3.8 or higher
pip package manager
