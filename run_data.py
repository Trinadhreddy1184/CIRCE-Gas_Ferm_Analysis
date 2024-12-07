import pandas as pd
from utils import Utils
import numpy as np

class RunData:
    def __init__(self, df, avg_df_processed, calibration_df,st):
        # Initialize with raw data, processed average data, and calibration data
        self.raw_df = df
        self.avg_df_processed = avg_df_processed
        self.calibration_df = calibration_df
        self.processed_df = None
        self.start_time=st

    def process(self):
        # Extract header rows from raw data
        header_rows = self.raw_df.iloc[:3].fillna('')
        # Create MultiIndex columns from header rows
        run_df_columns = pd.MultiIndex.from_arrays(header_rows.values)
        # Set columns of raw DataFrame using utils function
        self.raw_df.columns = Utils.excel_column_names(len(run_df_columns))
        # Extract run data from raw DataFrame, excluding header rows
        run_df = self.raw_df.iloc[3:].reset_index(drop=True)

        # Create a DataFrame for processed run data with appropriate column names
        self.processed_df = pd.DataFrame(columns=Utils.excel_column_names(len(run_df_columns)))
        # Define start time and create time range for processed data (1-minute intervals)
        start_time = pd.Timestamp(self.start_time)
        time_range = pd.date_range(start=start_time, end=start_time.replace(hour=23, minute=59, second=0), freq='1T')
        # Reindex processed DataFrame to match the time range
        self.processed_df = self.processed_df.reindex(range(len(time_range)))
        # Initialize some values in processed DataFrame
        self.processed_df.loc[0, 'A'] = 1
        self.processed_df['B'] = time_range
        # Calculate time difference in hours from the starting time
        self.processed_df['C'] = (self.processed_df['B'] - self.processed_df.iloc[0, 1]).dt.total_seconds() / 3600

        # Process columns D to K using data from averaged DataFrame
        # Iterate through columns D to K and corresponding columns in avg_df_processed (3 to 10)
        for col, avg_col in zip(['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], range(3, 11)):
            # Assign values from avg_df_processed based on time match, handle missing data with 0 or ""
            self.processed_df[col] = self.processed_df['B'].apply(
                lambda x: self.avg_df_processed.iloc[
                    self.avg_df_processed.index[self.avg_df_processed['C'] == x].tolist()[0], avg_col]
                if (self.avg_df_processed['C'] == x).any() else 0 if pd.notna(x) else ""
            )

        # Process calibration data
        # Extract header rows from calibration DataFrame
        header_rows = self.calibration_df.iloc[:9].fillna('')
        # Create MultiIndex columns from calibration header rows
        calibration_df_columns = pd.MultiIndex.from_arrays(header_rows.values)
        # Set columns of calibration DataFrame using utils function
        self.calibration_df.columns = Utils.excel_column_names(len(calibration_df_columns))
        # Extract a subset of calibration data for later use
        calibration_sep_df = self.calibration_df.iloc[1:5, 1:13].set_index('B')
        # Extract the main part of calibration data
        self.calibration_df = self.calibration_df.iloc[9:].reset_index(drop=True)


        #Process column M based on calibration data and column J
        self.processed_df['M'] = self.processed_df.apply(
            lambda row: (
                    row['J'] / 100
                    - (
                        calibration_sep_df['L'].iloc[2]
                        if row['J'] / 100 < self.calibration_df['I'].iloc[5] else
                        calibration_sep_df['L'].iloc[5]  # 'Calibration Data'!L$6
                        if calibration_sep_df['I'].iloc[5] <= row['J'] / 100 < self.calibration_df['I'].iloc[4] else
                        calibration_sep_df['L'].iloc[4]  # 'Calibration Data'!L$5
                        if calibration_sep_df['I'].iloc[4] <= row['J'] / 100 < self.calibration_df['I'].iloc[3] else
                        calibration_sep_df['L'].iloc[3]  # 'Calibration Data'!L$4
                    )
            ) if pd.notna(row['J']) else 0,
            axis=1
        )
        #Ensure values in column M are non-negative.
        self.processed_df['M'] = self.processed_df['M'].apply(lambda x: x if x >= 0 else 0)

        #Process column N based on calibration data and columns H and D
        self.processed_df['N'] = self.processed_df.apply(
            lambda row: (
                    (row['H'] / 100) / (1 - row['D'] / 100)
                    - (
                        calibration_sep_df.loc[
                            calibration_sep_df['J'] > row['H'] / 100, 'M'
                        ].iloc[0]  # Use the first match from calibration_df based on the condition
                    )
            ) if pd.notna(row['H']) and pd.notna(row['D']) else 0,
            axis=1
        )
        #Ensure values in column N are non-negative.
        self.processed_df['N'] = self.processed_df['N'].apply(lambda x: x if x >= 0 else 0)

        #Process column L based on calibration data and columns K, M, and N
        self.processed_df['L'] = self.processed_df.apply(
            lambda row: (
                    (row['K'] + (9.404 * row['M'] - 0.818 * row['N'])) / 100
                    - (
                        calibration_sep_df.loc[
                            calibration_sep_df['H'] > row['K'] / 100, 'K'
                        ].iloc[0]  # Use the first match from calibration_df for corresponding conditions
                    )
            ) if pd.notna(row['K']) and pd.notna(row['M']) and pd.notna(row['N']) else 0,
            axis=1
        )
        #Ensure values in column L are non-negative.
        self.processed_df['L'] = self.processed_df['L'].apply(lambda x: x if x >= 0 else 0)

        # Calculate columns O to U based on previously processed columns
        self.processed_df['O'] = (1 - (self.processed_df['L'] + self.processed_df['M'] + self.processed_df['N']))
        self.processed_df['P'] = self.processed_df['P'].apply(lambda x: 1.5)
        self.processed_df['Q'] = self.processed_df['P'] / self.processed_df['O']
        self.processed_df['R'] = self.processed_df['Q'] * self.processed_df['L']
        self.processed_df['S'] = self.processed_df['Q'] * self.processed_df['M']
        self.processed_df['T'] = self.processed_df['Q'] * self.processed_df['N']
        self.processed_df['U'] = self.processed_df['Q'] * self.processed_df['O']

        # Process columns V, W, X from averaged data
        self.processed_df['V'] = self.processed_df['B'].apply(
            lambda x: self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'X'].values[0]
            if (self.avg_df_processed['C'] == x).any() else None if pd.notna(x) else None
        )

        self.processed_df['W'] = self.processed_df['B'].apply(
            lambda x: self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'V'].values[0]
            if (self.avg_df_processed['C'] == x).any() else None if pd.notna(x) else None
        )

        self.processed_df['X'] = self.processed_df['B'].apply(
            lambda x: self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'T'].values[0]
            if (self.avg_df_processed['C'] == x).any() else None if pd.notna(x) else None
        )

        # Calculate columns Y to AD based on previously processed columns
        self.processed_df['Y'] = self.processed_df['R'] * 0.081505
        self.processed_df['Z'] = self.processed_df['S'] * 1.7893
        self.processed_df['AA'] = self.processed_df['T'] * 1.2954
        self.processed_df['AB'] = self.processed_df['V'] * 0.083732
        self.processed_df['AC'] = self.processed_df['W'] * 1.8389
        self.processed_df['AD'] = self.processed_df['X'] * 1.3309

        # Calculate columns AE to AG using a rolling calculation
        self.processed_df['AE'] = self.processed_df.index.map(
            lambda i: (
                (self.processed_df.loc[i, 'AB'] - self.processed_df.loc[i + 10, 'Y']) * 60
                if i <= self.processed_df.index.max() - 10
                else self.processed_df.loc[i, 'AB'] * 60
            )
        )
        self.processed_df['AF'] = self.processed_df.index.map(
            lambda i: (
                (self.processed_df.loc[i, 'AC'] - self.processed_df.loc[i + 10, 'Z']) * 60
                if i <= self.processed_df.index.max() - 10
                else self.processed_df.loc[i, 'AC'] * 60
            )
        )
        self.processed_df['AG'] = (self.processed_df.index.map(
            lambda i: (
                (self.processed_df.loc[i, 'AD'] - self.processed_df.loc[i + 10, 'AA']) * 60
                if i <= self.processed_df.index.max() - 10
                else self.processed_df.loc[i, 'AD'] * 60
            )
        ))

        # Process columns AH and AL from averaged data, handling potential zero values
        self.processed_df['AH'] = self.processed_df['B'].apply(
            lambda x: self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'AP'].values[0]
            if (self.avg_df_processed['C'] == x).any() and
               self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'AP'].values[0] != 0
            else 0 if pd.notna(x) else 0
        )

        self.processed_df['AL'] = self.processed_df['B'].apply(
            lambda x: self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'AN'].values[0]
            if (self.avg_df_processed['C'] == x).any() and
               self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'AN'].values[0] != 0
            else 0 if pd.notna(x) else 0
        )

        # Calculate columns AM to AT based on previously processed columns
        self.processed_df['AM'] = self.processed_df['AF'] + self.processed_df['AK']
        self.processed_df['AN'] = self.processed_df['AN'].apply(lambda x: 2.24)
        self.processed_df['AO'] = self.processed_df['AE'] / self.processed_df['AN']
        self.processed_df['AP'] = self.processed_df['AF'] / self.processed_df['AN']
        self.processed_df['AQ'] = self.processed_df['AG'] / self.processed_df['AN']
        self.processed_df['AR'] = self.processed_df['AO'] / 2.016 * 1000
        self.processed_df['AR'] = self.processed_df['AR'].apply(lambda x: x if x <= 100 and x >= -100 else 0)
        self.processed_df['AS'] = self.processed_df['AP'] / 44.01 * 1000
        self.processed_df['AS'] = self.processed_df['AS'].apply(lambda x: x if x <= 100 and x >= -100 else 0)
        self.processed_df['AT'] = self.processed_df['AQ'] / 31.999 * 1000
        self.processed_df['AT'] = self.processed_df['AT'].apply(lambda x: x if x <= 100 and x >= -100 else 0)

        # Calculate columns AU to AX based on previously processed columns, handling division by zero
        self.processed_df['AU'] = self.processed_df.apply(
            lambda row: (row['AO'] / row['BB']) if pd.notna(row['BB']) and row['BB'] != 0 else 0, axis=1)
        self.processed_df['AV'] = self.processed_df.apply(
            lambda row: (row['AP'] / row['BB']) if pd.notna(row['BB']) and row['BB'] != 0 else 0, axis=1)
        self.processed_df['AW'] = self.processed_df.apply(
            lambda row: (row['AQ'] / row['BB']) if pd.notna(row['BB']) and row['BB'] != 0 else 0, axis=1)
        self.processed_df['AX'] = self.processed_df.apply(
            lambda row: (row['AS'] * -1 / row['AT']) if pd.notna(row['AT']) and row['AT'] != 0 else 0, axis=1)

        # Process columns BB and BC from averaged data, handling missing data and zero values
        self.processed_df['BB'] = self.processed_df['B'].apply(
            lambda x: self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'AS'].values[0]
            if (self.avg_df_processed['C'] == x).any() and
               self.avg_df_processed.loc[self.avg_df_processed['C'] == x, 'AS'].values[0] != ""
            else None if pd.notna(x) else None
        )

        self.processed_df['BC'] = self.processed_df.apply(
            lambda row: row['BB'] * (
                        self.avg_df_processed.loc[self.avg_df_processed['C'] == row['B'], 'AT'].values[0] / 100)
            if (self.avg_df_processed['C'] == row['B']).any() and
               self.avg_df_processed.loc[self.avg_df_processed['C'] == row['B'], 'AT'].values[0] != ""
            else None if pd.notna(row['B']) else None, axis=1
        )

        # Calculate columns BD, BE, BF using rolling calculations, handling potential errors
        self.processed_df['BD'] = self.processed_df.apply(
            lambda row: self.processed_df.loc[row.name, ['AO', 'AO']].mean() * self.processed_df.loc[
                row.name, ['AN', 'AN']].mean() * (
                                self.processed_df.loc[row.name, 'C'] - self.processed_df.loc[row.name - 1, 'C'])
            if row.name > 0 else 0, axis=1
        )
        self.processed_df['BD'].fillna(0, inplace=True)

        self.processed_df['BE'] = self.processed_df.apply(
            lambda row: self.processed_df.loc[row.name, ['AP', 'AP']].mean() * self.processed_df.loc[
                row.name, ['AN', 'AN']].mean() * (
                                self.processed_df.loc[row.name, 'C'] - self.processed_df.loc[row.name - 1, 'C'])
            if row.name > 0 else 0, axis=1
        )
        self.processed_df['BE'].fillna(0, inplace=True)

        self.processed_df['BF'] = self.processed_df.apply(
            lambda row: self.processed_df.loc[row.name, ['AQ', 'AQ']].mean() * self.processed_df.loc[
                row.name, ['AN', 'AN']].mean() * (
                                self.processed_df.loc[row.name, 'C'] - self.processed_df.loc[row.name - 1, 'C'])
            if row.name > 0 else 0, axis=1
        )
        self.processed_df['BF'].fillna(0, inplace=True)


        # Process columns BG and BH from averaged data, handling missing data and empty strings
        self.processed_df['BG'] = self.processed_df['B'].apply(
            lambda b_value: self.avg_df_processed.loc[self.avg_df_processed['C'] == b_value, 'Q'].values[0]
            if len(self.avg_df_processed.loc[self.avg_df_processed['C'] == b_value, 'Q']) > 0 and
               self.avg_df_processed.loc[
                   self.avg_df_processed['C'] == b_value, 'Q'].values[0] != ""
            else None if pd.notna(b_value) else None
        )

        self.processed_df['BH'] = self.processed_df['B'].apply(
            lambda b_value: self.avg_df_processed.loc[self.avg_df_processed['C'] == b_value, 'R'].values[0]
            if len(self.avg_df_processed.loc[self.avg_df_processed['C'] == b_value, 'R']) > 0 and
               self.avg_df_processed.loc[
                   self.avg_df_processed['C'] == b_value, 'R'].values[0] != ""
            else None if pd.notna(b_value) else None
        )

        # Calculate column BI based on BG and BH, using a conditional statement
        self.processed_df['BI'] = self.processed_df.apply(
            lambda row: row['BH'] if (-1.69 * np.log(row['BG']) + 8.17) < row['BH'] else (
                        -1.69 * np.log(row['BG']) + 8.17),
            axis=1
        )

        # Calculate columns BJ and BK based on previously processed columns
        self.processed_df['BJ'] = (self.processed_df[['V', 'W', 'X']].sum(axis=1)) / (1000 * 60 * 0.1026)
        self.processed_df['BK'] = (self.processed_df['AQ'] / (3.5 - self.processed_df['BH'])) * 1000

        #This line seems to have an error, using arbitrary value for processed_df['BL'].iloc[2]
        self.processed_df['BL'] = 0.95 * (self.processed_df['BG'] / (self.processed_df['AN']) ** 0.6) * (
                    self.processed_df['BJ'] ** 0.6) * 3600 * self.processed_df['BL'].iloc[2] #Arbitrary value used here. Needs fixing.

        # Create copies of the processed DataFrame for different purposes
        run_df_processed = self.processed_df.copy()
        run_df = self.processed_df.copy()
        # Set the original MultiIndex columns back to the run_df DataFrame.
        run_df.columns = run_df_columns
        # Save the run data to a CSV file
        run_df.to_csv('run_data.csv', index=False)
        # Return the processed DataFrame
        return run_df_processed