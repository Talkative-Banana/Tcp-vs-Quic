import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend to prevent GTK errors

BD = ['1MB', '10MB', '150MB', '1000MB']
PZ = ['5KB', '500KB', '10MB', '50MB']

# Function to read average PLT from file
def read_avg_plt(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
        for line in lines:
            if "Average PageLoadTime" in line:
                return float(line.strip().split()[-1])
    except Exception as e:
        print(f"Error reading {file}: {e}")
    return None

# Create a 4x4 matrix for color values
color_matrix = np.zeros((len(PZ), len(BD), 3))

for i, pz in enumerate(PZ):
    for j, bd in enumerate(BD):
        pth = bd + '/' + pz + '/'
        quic_file = pth + "quic_results.txt"
        tcp_file = pth + "tcp_results.txt"
        quic_avg = read_avg_plt(quic_file)
        tcp_avg = read_avg_plt(tcp_file)

        if quic_avg is None or tcp_avg is None:
            print("Error: Could not retrieve average PLT values.")
            exit()

        # Compute color gradient from red (QUIC better) to blue (TCP better)
        color_intensity = (tcp_avg - quic_avg) / max(quic_avg, tcp_avg)
        color = (1 - abs(color_intensity), 1 - abs(color_intensity), 1) if color_intensity > 0 else (1, 1 - abs(color_intensity), 1 - abs(color_intensity))
        
        color_matrix[i, j] = color

# Plot the 4x4 grid without spaces
plt.figure(figsize=(4, 4))
plt.imshow(color_matrix, extent=[0, len(BD), 0, len(PZ)], aspect='auto')
plt.xticks(ticks=np.arange(len(BD)) + 0.5, labels=BD)
plt.yticks(ticks=np.arange(len(PZ)) + 0.5, labels=PZ)
plt.xlabel("Bandwidth")
plt.ylabel("Page Size")
plt.title("QUIC vs TCP Performance Gradient [Red (quic better)]")
plt.savefig("comparison.png", bbox_inches='tight', pad_inches=0)  # Remove spaces
print("Comparison saved as comparison.png")

