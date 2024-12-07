from utils import Utils


class SolarisData:
    def __init__(self, df):
        # Initialize the SolarisData class with the provided DataFrame
        self.raw_df = df  # Raw data from the Solaris input
        self.processed_df = None  # Placeholder for the processed DataFrame

    def process(self):
        # Process the data by removing the first three rows
        self.processed_df = self.raw_df.iloc[3:].reset_index(
            drop=True)  # Remove the first three rows and reset the index

        # Assign generated Excel-style column names to the DataFrame
        self.processed_df.columns = Utils.excel_column_names(len(self.raw_df.columns))  # Assign new column names

        return self.processed_df  # Return the processed DataFrame
