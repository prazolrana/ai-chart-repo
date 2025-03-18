"""" 
This program asks you for the csv file and the column for stock price data. Also 
asks user to imput the invested value and then makes the animated graph of the investment 
value. 

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter

# Load and process stock data
def load_stock_data(csv_file, price_column):
    df = pd.read_csv(csv_file, parse_dates=['Date'], dayfirst=False)
    df.sort_values('Date', inplace=True)  # Ensure chronological order
    df[price_column] = df[price_column].replace(r'[\$,]', '', regex=True).astype(float)  # Convert to float
    
    # Ensure there's data to process
    if df.empty:
        raise ValueError("The CSV file is empty or incorrectly formatted.")
    
    return df

# Calculate investment value over time
def calculate_values(df, price_column, initial_investment):
    df['Investment Value'] = (initial_investment / df.iloc[0][price_column]) * df[price_column]
    return df

# Create and animate the stock growth graph
def animate_stock_growth(df, output_file="stock_growth.mp4"):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Set fixed limits
    ax.set_xlim(df['Date'].min(), df['Date'].max())
    ax.set_ylim(0, df['Investment Value'].max() * 1.1)
    
    # Initialize graph elements
    line, = ax.plot([], [], 'b-', linewidth=2, label='Investment Value')
    point, = ax.plot([], [], 'ro')  # Red dot to highlight the last value

    # Update function for animation
    def update(frame):
        ax.clear()
        ax.set_xlim(df['Date'].min(), df['Date'].max())
        ax.set_ylim(0, df['Investment Value'].max() * 1.1)

        if frame >= len(df):  # Prevent out-of-bounds errors
            frame = len(df) - 1

        ax.plot(df['Date'][:frame+1], df['Investment Value'][:frame+1], 'b-', linewidth=2, label='Investment Value')
        ax.plot(df['Date'].iloc[frame], df['Investment Value'].iloc[frame], 'ro')  # Highlight last value
        
        ax.text(df['Date'].iloc[frame], df['Investment Value'].iloc[frame], f"${df['Investment Value'].iloc[frame]:,.2f}",
                fontsize=10, verticalalignment='bottom', horizontalalignment='right')

        ax.set_title(f"Stock Investment Growth: {df['Date'].iloc[frame].strftime('%Y-%m-%d')}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Investment Value ($)")
        ax.legend()

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=10, repeat=False)

    # Save animation
    writer = FFMpegWriter(fps=30, metadata={"title": "Stock Growth Animation"})
    ani.save(output_file, writer=writer)
    plt.show()

if __name__ == "__main__":
    csv_file = input("Enter the CSV file name: ")
    price_column = input("Enter the column name for stock price data: ")
    initial_investment = float(input("Enter the initial investment amount: "))
    
    df = load_stock_data(csv_file, price_column)
    df = calculate_values(df, price_column, initial_investment)
    animate_stock_growth(df)
