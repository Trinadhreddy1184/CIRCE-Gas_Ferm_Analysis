# CIRCE: Gas Analysis Automation

## Project Overview

### Description

The **Gas Analysis Automation** project aims to process raw gas detector output data into a summarized and more readable format for easier interpretation and decision-making. This automation replaces the manual Excel-based workflow, streamlining the handling of long and complex datasets. 

The project processes input data from fermentation processes, transforms it using pre-defined calculations, and generates summaries and visualizations that stakeholders can easily interpret.

### Key Features
- Automates data processing from raw Excel or CSV files.
- Ensures input data accuracy and transformation consistency.
- Summarizes the processed data into user-friendly formats.
- Provides clear visualizations to aid in data-driven decision-making.

## Components of the Project

### 1. **BlueVisData Class**
- Processes raw BlueVis gas data.
- Extracts headers and reformats the raw data for further calculations.
- **File:** `bluevis_data.py`

### 2. **SolarisData Class**
- Processes Solaris data by cleaning unnecessary rows and assigning column names.
- Outputs the cleaned data for integration with other components.
- **File:** `solaris_data.py`

### 3. **AveragedData Class**
- Combines BlueVis and Solaris processed data.
- Calculates averaged metrics for further analysis.
- **File:** `averaged_data.py`

### 4. **RunData Class**
- Integrates averaged data and calibration information.
- Computes derived metrics necessary for gas consumption analysis.
- **File:** `run_data.py`

### 5. **SummaryCalculator Class**
- Summarizes key metrics like gas consumption per biomass and volume.
- Outputs a JSON summary for easy sharing and reporting.
- **File:** `summary_calculator.py`

### 6. **DataVisualizer Class**
- Creates interactive visualizations of gas concentration trends.
- Outputs visualizations as both interactive plots and PNG images.
- **File:** `visualizer.py`

### 7. **Utils Class**
- Provides helper functions for generating Excel-style column names and safely calculating means.
- Reused across multiple classes.
- **File:** `utils.py`

## Installation Requirements

### Prerequisites
- Python 3.x
- Required Python libraries: `pandas`, `numpy`, `plotly`, `dash`

### Installation
Install all dependencies by running:
```sh
pip install -r requirements.txt
```

## How to Run the Project

1. **Prepare Input Data**
   - Ensure the raw data file (Excel/CSV) is formatted correctly.

2. **Execute the Bash Script**
   - Run the provided shell script with the input file name and start_time for Run data as a parameter:
   ```sh
   ./run.sh <input_filename.xlsx> 'start_time'
   ```
   This will execute all the necessary Python scripts sequentially.

3. **View Outputs**
   - Processed data is saved as:
     - `averaged_data.csv`
     - `run_data.csv`
   - The summary is saved as:
     - `summary.json`
   - Visualizations are saved as:
     - `summary_scatterplot.png`

## Interaction of Classes

### Workflow Description
1. **`BlueVisData` and `SolarisData`** handle the cleaning and reformatting of raw data.
2. The **`AveragedData`** class integrates the cleaned data to calculate averaged values.
3. **`RunData`** processes the averaged values with calibration data to generate detailed metrics.
4. **`SummaryCalculator`** computes high-level summaries from the processed data.
5. **`DataVisualizer`** creates visual outputs for the metrics.

### Class Interaction Flow
- **Input:** Raw data (BlueVis, Solaris) is processed.
- **Integration:** Averaged data is computed.
- **Analysis:** Run data and summary statistics are generated.
- **Visualization:** Data trends are plotted for stakeholder interpretation.
```
+-----------------------------+
|         Main Method         |
+-----------------------------+
             |
             v
+-----------------------------+
|      BlueVisData Class      |
| Process BlueVis raw data    |
+-----------------------------+
             |
             v
+-----------------------------+
|      SolarisData Class      |
| Process Solaris raw data    |
+-----------------------------+
             |
             v
+-----------------------------+
|     AveragedData Class      |
| Combine BlueVis and Solaris |
+-----------------------------+
             |
             v
+-----------------------------+
|       RunData Class         |
| Process with calibration    |
+-----------------------------+
             |
             v
+-----------------------------+
|   SummaryCalculator Class   |
| Calculate summary metrics   |
+-----------------------------+
             |
             v
+-----------------------------+
|     DataVisualizer Class    |
| Generate visualizations     |
+-----------------------------+

```
## Summary
The **Gas Analysis Automation** project simplifies the cumbersome manual workflow of processing gas detector data. It ensures accuracy, automates calculations, and delivers actionable insights in clear visual and summarized formats. This modular approach allows for easy adaptation and scaling for future needs.

