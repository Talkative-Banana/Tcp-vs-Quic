#!/bin/bash

# Ensure the required Python script is available
PYTHON_SCRIPT="page_load_time.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT not found!"
    exit 1
fi

# Parameters
RESULTS_DIR="results"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

# Function to capture CPU utilization
capture_cpu_usage() {
    local file=$1
    mpstat -P 0 1 > "$file" &
    echo $!  # Return the PID of the background process
}

# Function to stop capturing CPU stats
stop_cpu_usage_capture() {
    kill $1
}

# Function to run your Python script and track its performance
run_python_script() {
    local mode=$1  # quic or tcp
    local pgsz=$2  # page size
    local results_file=$3  # Output file

    taskset -c 0 python3 "$PYTHON_SCRIPT" 3 --$mode "$pgsz" >> "$results_file" &
    python_pid=$!
    wait $python_pid  # Wait for completion
}

# Parameter values to iterate over
ITERATION_VALUES=(700)

# Loop through the iteration values
for iter in "${ITERATION_VALUES[@]}"; do
    # Create a folder for the current iteration value
    ITERATION_DIR="$RESULTS_DIR/$iter"
    mkdir -p "$ITERATION_DIR"

    # File paths for the results and CPU stats
    QUIC_RESULTS="$ITERATION_DIR/quic_results.txt"
    TCP_RESULTS="$ITERATION_DIR/tcp_results.txt"
    CPU_STATS_QUIC="$ITERATION_DIR/cpu_utilization_quic.txt"
    CPU_STATS_TCP="$ITERATION_DIR/cpu_utilization_tcp.txt"

    echo "Measuring Page Load Time for QUIC with $iter page size..."
    cpu_pid=$(capture_cpu_usage "$CPU_STATS_QUIC")
    run_python_script "quic" "$iter" "$QUIC_RESULTS"
    stop_cpu_usage_capture $cpu_pid

    sleep 1  # Short pause
    
    echo "Measuring Page Load Time for TCP with $iter page size..."
    cpu_pid=$(capture_cpu_usage "$CPU_STATS_TCP")
    run_python_script "tcp" "$iter" "$TCP_RESULTS"
    stop_cpu_usage_capture $cpu_pid
    
    sleep 1  # Short pause to avoid overlapping measurements
done

echo "Experiments completed. Results stored in $RESULTS_DIR."

