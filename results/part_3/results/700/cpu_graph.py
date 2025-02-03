import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import datetime


def parse_cpu_data(log_file):
    timestamps = []
    cpu_usages = []

    with open(log_file, 'r') as file:
        for line in file:
            parts = line.split()

            # Skip headers and repeated column headers
            if "Linux" in line or "CPU" in parts or len(parts) < 12:
                continue

            try:
                # Extract timestamp (first 3 columns)
                timestamp_str = f"{parts[0]} {parts[1]} {parts[2]}"  # e.g., "10:31:43 PM IST"
                timestamp = datetime.datetime.strptime(timestamp_str, "%I:%M:%S %p IST")

                # Try extracting CPU usage from column 3 or 4
                print(parts)
                cpu_usage = float(parts[4])  # %usr column (index 3)
                if cpu_usage == 0.0:
                    print(f"Warning: Extracted zero CPU usage at {timestamp_str} - Check column index!")

                timestamps.append(timestamp)
                cpu_usages.append(cpu_usage)

            except ValueError:
                continue  # Skip lines that can't be parsed

    return timestamps, cpu_usages



# Function to plot CPU utilization
def plot_cpu_utilization(log_file):
    timestamps, cpu_usages = parse_cpu_data(log_file)
    if not timestamps:
        print("No valid CPU data found.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_usages, marker='o', linestyle='-', color='b', label='CPU Usage (%)')
    plt.xlabel('Time')
    plt.ylabel('CPU Utilization (%)')
    plt.title('CPU Utilization Over Time')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example usage
log_file = "cpu_utilization_tcp.txt"  # Change this if using TCP results
plot_cpu_utilization(log_file)
plt.savefig("cpu_plot.png")
