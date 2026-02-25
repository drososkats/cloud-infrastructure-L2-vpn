import pandas as pd
import matplotlib
# Use 'Agg' backend for headless environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# Configuration
csv_file = 'vm_metrics.csv'
output_image = 'vm_performance_chart.png'

def generate_chart():
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return

    # Load data
    try:
        df = pd.read_csv(csv_file)

        # Data Cleaning: Convert columns to numeric
        # errors='coerce' will turn any text/headers found in rows into NaN (Not a Number)
        df['cpu'] = pd.to_numeric(df['cpu'], errors='coerce')
        df['mem'] = pd.to_numeric(df['mem'], errors='coerce')

        # Drop rows that have NaN values (like repeated headers)
        df = df.dropna(subset=['cpu', 'mem', 'Time'])

        # Take only the last 30 valid entries
        df = df.tail(30)

    except Exception as e:
        print(f"Error processing CSV data: {e}")
        return

    if df.empty:
        print("Error: No valid numeric data found in CSV.")
        return

    # Calculations
    df['cpu_pct'] = df['cpu'] * 100
    df['mem_mb'] = df['mem'] / (1024 * 1024)

    # Create the Plot (Dual Axis)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # CPU Axis (Left)
    color_cpu = 'tab:red'
    ax1.set_xlabel('Time (HH:MM:SS)')
    ax1.set_ylabel('CPU Usage (%)', color=color_cpu)
    ax1.plot(df['Time'], df['cpu_pct'], marker='o', color=color_cpu, linewidth=2, label='CPU %')
    ax1.tick_params(axis='y', labelcolor=color_cpu)
    ax1.set_ylim(0, 105)

    # RAM Axis (Right)
    ax2 = ax1.twinx()
    color_mem = 'tab:blue'
    ax2.set_ylabel('RAM Usage (MB)', color=color_mem)
    ax2.plot(df['Time'], df['mem_mb'], marker='s', color=color_mem, linewidth=2, label='RAM MB')
    ax2.tick_params(axis='y', labelcolor=color_mem)

    # Styling and Safety Fixes
    plt.title('Proxmox VM Metrics: CPU & RAM Utilization', fontsize=14)

    # Fix for Raster Overflow: Limit ticks and rotate
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')

    ax1.grid(True, linestyle='--', alpha=0.4)
    fig.tight_layout()

    # Save the Output
    try:
        plt.savefig(output_image, dpi=100)
        print(f"Success! Performance chart generated: {output_image}")
    except Exception as e:
        print(f"Error saving chart: {e}")
    finally:
        plt.close(fig)

if __name__ == "__main__":
    generate_chart()