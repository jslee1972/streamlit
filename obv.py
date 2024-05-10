import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(f'{symbol}.tw', start=start_date, end=end_date)
    data['30d MA'] = data['Adj Close'].rolling(window=30).mean()
    return data[['Adj Close', 'Volume', '30d MA']].copy()

def calculate_obv(data):
    data['OBV'] = 0
    data.loc[data.index[0], 'OBV'] = data.at[data.index[0], 'Volume']

    for i in range(1, len(data)):
        if data['Adj Close'].iloc[i] > data['Adj Close'].iloc[i-1]:
            data.loc[data.index[i], 'OBV'] = data['OBV'].iloc[i-1] + data['Volume'].iloc[i]
        elif data['Adj Close'].iloc[i] < data['Adj Close'].iloc[i-1]:
            data.loc[data.index[i], 'OBV'] = data['OBV'].iloc[i-1] - data['Volume'].iloc[i]
        else:
            data.loc[data.index[i], 'OBV'] = data['OBV'].iloc[i-1]
    # Calculate the rolling correlation
    data['Correlation'] = data['OBV'].rolling(window=30).corr(data['30d MA'])

def plot_obv_and_correlation(data, title):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Adj Close and 30d MA', color=color)
    ax1.plot(data.index, data['Adj Close'], label='Adj Close', color=color)
    ax1.plot(data.index, data['30d MA'], label='30-Day MA', color='tab:orange')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('OBV', color=color)
    ax2.plot(data.index, data['OBV'], label='OBV', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    # Add a second plot for correlation on a new figure
    fig2, ax3 = plt.subplots()
    ax3.plot(data.index, data['Correlation'], label='OBV/30d MA Correlation', color='tab:green')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Correlation')
    ax3.set_title('Correlation between OBV and 30-Day MA')
    ax3.legend()

    plt.title(title)
    plt.show()

# Example usage
symbol = '1109'  # Example: Apple Inc.
start_date = '2024-01-01'
end_date = '2024-04-25'
data = fetch_stock_data(symbol, start_date, end_date)
calculate_obv(data)
plot_obv_and_correlation(data, ' Stock, OBV, 30-Day MA, and Correlation')
