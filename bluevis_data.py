import pandas as pd
from utils import Utils


class BlueVisData:
    def __init__(self, df):
        # Initialize the BlueVisData class with the provided DataFrame
        self.raw_df = df  # Raw data from the BlueVis input
        self.processed_df = None  # Placeholder for the processed DataFrame

    def process(self):
        # Extract header rows to create multi-level column headers
        header_rows = self.raw_df.iloc[:6].fillna('')  # Extract the first 6 rows which contain the headers
        multi_index_columns = pd.MultiIndex.from_arrays(
            header_rows.values)  # Create MultiIndex for hierarchical columns

        # Assign generated Excel-style column names to the DataFrame
        self.raw_df.columns = Utils.excel_column_names(len(multi_index_columns))

        # Process the data by removing the header rows
        self.processed_df = self.raw_df.iloc[6:].reset_index(drop=True)  # Remove the header rows and reset index

        return self.processed_df  # Return the processed DataFrame
