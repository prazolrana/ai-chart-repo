import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter

# Load and process stock data
def load_stock_data(csv_file):
    df = pd.read_csv(csv_file)

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%Y-%m-%d')

    # Ensure data from 2011 onwards is kept
    df = df[df['Date'] >= pd.Timestamp('2011-01-01')]

    # Sort data in chronological order
    df.sort_values('Date', inplace=True)

    # Convert 'Ltp' (Last Trading Price) to float
    df['Ltp'] = pd.to_numeric(df['Ltp'], errors='coerce')

    # Remove any rows with missing values
    df.dropna(subset=['Ltp', 'Date'], inplace=True)

    # Print data count per year to check missing years
    df['Year'] = df['Date'].dt.year
    print("Data points per year before sampling:")
    print(df['Year'].value_counts().sort_index())

    # Sample: Take at least 10 points per year (or more if available)
    df = df.groupby('Year', group_keys=False).apply(lambda x: x.iloc[::max(1, len(x)//10)])  

    # Print data count per year after sampling
    print("\nData points per year after sampling:")
    print(df['Year'].value_counts().sort_index())

    if df.empty:
        raise ValueError("The CSV file is empty or contains invalid data after filtering.")

    return df

# Calculate investment value over time
def calculate_values(df, initial_investment=100000):
    df['Investment Value'] = (initial_investment / df.iloc[0]['Ltp']) * df['Ltp']
    return df

# Create and animate the stock growth graph
def animate_stock_growth(df, output_file="stock_growth.mp4"):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.set_xlim(df['Date'].min(), df['Date'].max())
    ax.set_ylim(0, df['Investment Value'].max() * 1.1)

    line, = ax.plot([], [], 'b-', linewidth=2, label='Investment Value in NPR')
    point, = ax.plot([], [], 'ro')

    def update(frame):
        ax.clear()

        ax.set_xlim(df['Date'].min(), df['Date'].max())
        ax.set_ylim(0, df['Investment Value'].max() * 1.1)

        if frame >= len(df):
            frame = len(df) - 1  

        ax.plot(df['Date'][:frame+1], df['Investment Value'][:frame+1], 'b-', linewidth=2, label='Investment Value in NPR')
        ax.plot(df['Date'].iloc[frame], df['Investment Value'].iloc[frame], 'ro')  

        ax.text(df['Date'].iloc[frame], df['Investment Value'].iloc[frame], 
                f"Rs {df['Investment Value'].iloc[frame]:,.2f}",
                fontsize=10, verticalalignment='bottom', horizontalalignment='right')

        ax.set_title(f"Stock Investment Growth in NPR: {df['Date'].iloc[frame].strftime('%Y-%m-%d')}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Investment Value (NPR)")
        ax.legend()

    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=200, repeat=False)

    writer = FFMpegWriter(fps=10, metadata={"title": "Stock Growth Animation"})
    ani.save(output_file, writer=writer)
    plt.show()

# Main execution
if __name__ == "__main__":
    csv_file = "scb_price_history_cleaned.csv"  # Ensure the correct filename
    df = load_stock_data(csv_file)
    df = calculate_values(df)
    animate_stock_growth(df)
