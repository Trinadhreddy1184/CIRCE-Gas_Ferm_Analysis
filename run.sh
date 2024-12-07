#!/bin/bash
#!/bin/bash

# This script will run the Python files for data processing and visualization.
# Usage: ./run_data_processing.sh input_filename.xlsx '2023-10-25 13:47:38'

# Check if the input file is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_filename.xlsx> <start_time>"
  exit 1
fi

INPUT_FILE=$1
START_TIME=$2

# Run the main Python script with the provided filename and log output to a file
LOG_FILE="run_data_processing.log"
echo "Starting data processing: $(date)" | tee -a "$LOG_FILE"

# Run the main Python script and handle any errors
{
  python3 main.py "$INPUT_FILE" "$START_TIME"
} 2>&1 | tee -a "$LOG_FILE"

if [ "${PIPESTATUS[0]}" -ne 0 ]; then
  echo "An error occurred during data processing: $(date)" | tee -a "$LOG_FILE"
  exit 1
fi

echo "Data processing completed: $(date)" | tee -a "$LOG_FILE"
