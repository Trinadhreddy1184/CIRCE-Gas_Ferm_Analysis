import pandas as pd
from utils import Utils


class AveragedData:
    def __init__(self, df, bluevis_df, solaris_df):
        # Initialize the AveragedData class with raw data, BlueVis processed data, and Solaris processed data
        self.raw_df = df
        self.bluevis_df = bluevis_df
        self.solaris_df = solaris_df
        self.processed_df = None

    def process(self):
        # Extract header rows and set columns for the dataframe
        header_rows = self.raw_df.iloc[:2].fillna('')
        avg_df_columns = pd.MultiIndex.from_arrays(header_rows.values)
        self.raw_df.columns = Utils.excel_column_names(len(avg_df_columns))
        avg_df = self.raw_df.iloc[2:].reset_index(drop=True)

        # Create and process 'avg_df_processed' DataFrame
        self.processed_df = pd.DataFrame(columns=Utils.excel_column_names(len(avg_df_columns)))

        # Determine the start and end datetime from BlueVis data
        start_datetime = self.bluevis_df.iloc[0, 1]
        end_datetime = self.bluevis_df.iloc[-1, 1]

        # Create a datetime series with 1-minute intervals
        datetime_series = pd.date_range(start=start_datetime,
                                        periods=int((end_datetime - start_datetime).total_seconds() / 60) + 1,
                                        freq='60S')

        # Set datetime columns in the processed DataFrame
        self.processed_df['C'] = datetime_series
        self.processed_df['B'] = self.processed_df['C'] + pd.to_timedelta(4, unit='h')

        # Calculate columns 'L' and 'M' based on BlueVis data
        self.processed_df['L'] = self.processed_df.apply(lambda row: self.bluevis_df['A'].searchsorted(row['B']) + 8,
                                                         axis=1)
        self.processed_df['M'] = self.processed_df['L'] + 1000

        # Set column 'A' based on conditions from BlueVis data
        self.processed_df['A'] = self.processed_df['C'].apply(
            lambda x: 1 if (self.bluevis_df['A'].searchsorted(x, side='right') - 1) else "" if pd.notna(x) else "")

        # Calculate columns 'D' to 'K' based on a range in BlueVis data and averaging
        for col, col_name in zip(['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], ['C', 'D', 'E', 'F', 'G', 'H', 'L', 'M']):
            self.processed_df[col] = self.processed_df.apply(
                lambda row: self.bluevis_df.loc[
                            round(row['L']):round(row['M']),
                            col_name
                            ][(self.bluevis_df.loc[round(row['L']):round(row['M']), 'A'] >= avg_df.iloc[row.name, 1]) &
                              (self.bluevis_df.loc[round(row['L']):round(row['M']), 'A'] < avg_df.iloc[
                                  min(row.name + 1, len(avg_df) - 1), 1])]
                .mean() if not self.bluevis_df.loc[round(row['L']):round(row['M']), col_name].empty else float('nan'),
                axis=1
            )

        # Convert column 'A' in Solaris data to handle NaT values
        self.solaris_df['A'] = self.solaris_df['A'].apply(
            lambda x: pd.NaT if pd.isnull(x) or isinstance(x, (float, int)) else x)

        # Calculate columns 'AK' and 'AL' based on Solaris data
        self.processed_df['AK'] = self.processed_df.apply(
            lambda row: self.solaris_df['A'].searchsorted(row['C'], side='right'), axis=1)
        self.processed_df['AL'] = self.processed_df['AK'] + 1000

        # Calculate columns 'N' to 'AJ' based on Solaris data and averaging
        for col, col_name in zip(
                ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF',
                 'AG', 'AH', 'AI', 'AJ'],
                ['E', 'G', 'I', 'K', 'M', 'P', 'Q', 'T', 'U', 'R', 'S', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD',
                 'AE', 'AF', 'AG']):
            self.processed_df[col] = self.processed_df.apply(
                lambda row: self.solaris_df.loc[
                            round(row['AK']):round(row['AL']),
                            col_name
                            ][(self.solaris_df.loc[round(row['AK']):round(row['AL']), 'A'] >= self.processed_df.iloc[
                    row.name, 2]) &
                              (self.solaris_df.loc[round(row['AK']):round(row['AL']), 'A'] < self.processed_df.iloc[
                                  min(row.name + 1, len(self.processed_df) - 1), 2])]
                .mean() if pd.notna(row['AK']) and pd.notna(row['AL']) else float('nan'),
                axis=1
            )

        # Adding additional columns to the processed DataFrame
        self.processed_df['AM'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 5]
            if x in self.processed_df['AM'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AN'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 8]
            if x in self.processed_df['AN'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AO'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 9]
            if x in self.processed_df['AO'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AP'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 11]
            if x in self.processed_df['AP'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AQ'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 12]
            if x in self.processed_df['AQ'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AR'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 13]
            if x in self.processed_df['AR'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AS'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 15]
            if x in self.processed_df['AS'].values else 0 if pd.notna(x) else ""
        )

        self.processed_df['AT'] = self.processed_df['A'].apply(
            lambda x: self.processed_df.iloc[self.processed_df.index[self.processed_df['A'] == x].tolist()[0], 5]
            if x in self.processed_df['AT'].values else 0 if pd.notna(x) else ""
        )

        # Copy the processed DataFrame and set appropriate column names
        avg_df_processed = self.processed_df.copy()
        avg_df = self.processed_df.copy()
        avg_df.columns = avg_df_columns

        # Save the averaged data to a CSV file
        avg_df.to_csv('averaged_data.csv', index=False)

        return avg_df_processed
