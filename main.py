import pandas as pd
from bluevis_data import BlueVisData
from solaris_data import SolarisData
from averaged_data import AveragedData
from run_data import RunData
from summary_calculator import SummaryCalculator
from visualizer import DataVisualizer
import json
import sys
import logging
import warnings

warnings.filterwarnings("ignore")

# Set up logging to log to a file
logging.basicConfig(filename='data_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

if __name__ == "__main__":
    try:
        # Reading the Excel file
        logging.info("Reading the Excel file.")
        # Load the Excel file provided as a command-line argument
        df = pd.read_excel(sys.argv[1], sheet_name=None, engine="openpyxl")
        logging.info("Excel file read successfully.")

        # Instantiate and process BlueVisData
        logging.info("Instantiating and processing BlueVisData.")
        # Create an instance of BlueVisData and process it
        bluevis_data = BlueVisData(df['BlueVis Raw Data'])
        bluevis_processed = bluevis_data.process()
        logging.info("BlueVisData processed successfully.")

        # Instantiate and process SolarisData
        logging.info("Instantiating and processing SolarisData.")
        # Create an instance of SolarisData and process it
        solaris_data = SolarisData(df['Solaris Data'])
        solaris_processed = solaris_data.process()
        logging.info("SolarisData processed successfully.")

        # Instantiate and process AveragedData
        logging.info("Instantiating and processing AveragedData.")
        # Create an instance of AveragedData using BlueVis and Solaris processed data
        averaged_data = AveragedData(df['AveragedData'], bluevis_processed, solaris_processed)
        avg_df_processed = averaged_data.process()
        logging.info("AveragedData processed successfully.")

        # Instantiate and process RunData
        logging.info("Instantiating and processing RunData.")
        # Create an instance of RunData using AveragedData and Calibration Data
        run_data = RunData(df['Run Data'], avg_df_processed, df['Calibration Data'],sys.argv[2])
        run_df_processed = run_data.process()
        logging.info("RunData processed successfully.")

        # Calculate summary
        logging.info("Calculating summary.")
        # Create an instance of SummaryCalculator and calculate summary on RunData
        summary_calculator = SummaryCalculator()
        summary = summary_calculator.calculate_summary(run_df_processed)
        logging.info("Summary calculated successfully.")
        # Print the summary in JSON format

        # Visualize data
        logging.info("Visualizing data.")
        # Create an instance of DataVisualizer and generate interactive scatter plot
        visualizer = DataVisualizer(run_df_processed)
        visualizer.plot_interactive_scatter()
        logging.info("Data visualization completed successfully.")

    except Exception as e:
        # Log the exception if any error occurs and exit the script
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
