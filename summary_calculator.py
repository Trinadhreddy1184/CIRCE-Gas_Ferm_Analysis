import pandas as pd
import numpy as np
import json


class SummaryCalculator:
    @staticmethod
    def calculate_summary(df):
        # Function to get the hours corresponding to a given timestamp value
        def get_hrs(timestamp_value):
            try:
                # Find the closest matching timestamp in column 'B' and get the corresponding value in column 'C'
                res = df.loc[df['B'].searchsorted(timestamp_value), 'C']
            except:
                # If there is an issue, use the maximum timestamp value available
                res = df.loc[df['B'].searchsorted(df['B'].max()), 'C']
            return res

        # Function to calculate total consumption values
        def get_totals(val1, val2, st, end):
            try:
                # Calculate the sum for the given range and normalize using another value
                return (df.loc[(df['C'] >= st) & (df['C'] < end), val1].sum() / df.loc[df['C'].le(end).idxmax(), val2])
            except:
                return np.nan

        # Function to get the maximum value in a given range
        def get_max(val, st, end):
            try:
                # Get the maximum value for the specified column and range
                return df.loc[(df['C'] > st) & (df['C'] < end), val].max()
            except:
                return np.nan

        # Function to get the mean value in a given range
        def get_mean(val, val1, val2):
            try:
                # Calculate the mean for the specified column and range
                return df.loc[(df['C'] >= val1) & (df['C'] < val2), val].mean()
            except:
                return np.nan

        # Define important timestamps used in the summary calculations
        c5 = pd.Timestamp('10/25/23 1:47 PM')
        d5 = pd.Timestamp('10/26/23 12:05 PM')
        c6 = get_hrs(c5)
        d6 = get_hrs(d5)
        g5 = pd.Timestamp("10/26/23 4:50 PM")
        h5 = pd.Timestamp("10/27/23 3:07 PM")
        g6 = get_hrs(g5)
        h6 = get_hrs(h5)
        d22 = d6
        c22 = d22 - 1
        g22 = 27.050
        h22 = 30.000
        c7 = 20

        # Create the summary dictionary containing all relevant calculations
        summary = {
            "Growth": {
                "Start": c5.strftime('%Y/%m/%d %H:%M %p'),
                "End": d5.strftime('%Y/%m/%d %H:%M %p'),
                "Elapsed Fermentation Time": {"Start": c6, "End": d6, "Unit": "hrs"},
                "Stabilization Time of g/g Data": {"Value": c7, "Unit": "hrs"},
                "Totals": {
                    "Hydrogen Consumed/Biomass": {"Value": get_totals('BD', 'BB', c6, d6), "Unit": "g/g"},
                    "Carbon Dioxide Consumed/Biomass": {"Value": get_totals('BE', 'BB', c6, d6), "Unit": "g/g"},
                    "Oxygen Consumed/Biomass": {"Value": get_totals('BF', 'BB', c6, d6), "Unit": "g/g"},
                    "Hydrogen Consumed/Volume": {"Value": get_totals('BD', 'AN', c6, d6), "Unit": "g/L"},
                    "Carbon Dioxide Consumed/Volume": {"Value": get_totals('BE', 'AN', c6, d6), "Unit": "g/L"},
                    "Oxygen Consumed/Volume": {"Value": get_totals('BF', 'AN', c6, d6), "Unit": "g/L"}
                },
                "Maximums": {
                    "EFT Time Range": {"Start": c22, "End": d22, "Unit": "hrs"},
                    "Hydrogen Consumption Rate": {"Value": get_max('AR', c22, d22), "Unit": "mmol/L/hr"},
                    "Carbon Dioxide Consumption Rate": {"Value": get_max('AS', c22, d22), "Unit": "mmol/L/hr"},
                    "Oxygen Consumption Rate": {"Value": get_max('AT', c22, d22), "Unit": "mmol/L/hr"}
                },
                "Averages": {
                    "Hydrogen Consumption/Biomass/Hr": {"Value": get_mean('AU', c7, d6), "Unit": "g/g/hr"},
                    "Carbon Dioxide Consumption/Biomass/Hr": {"Value": get_mean('AV', c7, d6), "Unit": "g/g/hr"},
                    "Oxygen Consumption Rate /Hr": {"Value": get_mean('AW', c7, d6), "Unit": "g/g/hr"}
                },
                "Stoichiometry": {"Actual": "null", "Literature": "null"},
                "% Mixotrophy": "null"
            },
            "Production": {
                "Start": g5.strftime('%Y/%m/%d %H:%M %p'),
                "End": h5.strftime('%Y/%m/%d %H:%M %p'),
                "Elapsed Fermentation Time": {"Start": g6, "End": h6, "Unit": "hrs"},
                "Totals": {
                    "Hydrogen Consumed/Biomass": {"Value": get_totals('BD', 'BB', g6, h6), "Unit": "g/g"},
                    "Carbon Dioxide Consumed/Biomass": {"Value": get_totals('BE', 'BB', g6, h6), "Unit": "g/g"},
                    "Oxygen Consumed/Biomass": {"Value": get_totals('BF', 'BB', g6, h6), "Unit": "g/g"},
                    "Hydrogen Consumed/Volume": {"Value": get_totals('BD', 'AN', g6, h6), "Unit": "g/L"},
                    "Carbon Dioxide Consumed/Volume": {"Value": get_totals('BE', 'AN', g6, h6), "Unit": "g/L"},
                    "Oxygen Consumed/Volume": {"Value": get_totals('BF', 'AN', g6, h6), "Unit": "g/L"},
                    "Hydrogen Consumed/TAG": {"Value": get_totals('BF', 'BC', g6, h6), "Unit": "g/g"},
                    "Carbon Dioxide Consumed/TAG": {"Value": get_totals('BF', 'BC', g6, h6), "Unit": "g/g"},
                    "Oxygen Consumed/TAG": {"Value": get_totals('BF', 'BC', g6, h6), "Unit": "g/g"}
                },
                "Maximums": {
                    "EFT Time Range": {"Start": g22, "End": h22, "Unit": "hrs"},
                    "Hydrogen Consumption Rate": {"Value": get_max('AR', g22, h22), "Unit": "mmol/L/hr"},
                    "Carbon Dioxide Consumption Rate": {"Value": get_max('AS', g22, h22), "Unit": "mmol/L/hr"},
                    "Oxygen Consumption Rate": {"Value": get_max('AT', g22, h22), "Unit": "mmol/L/hr"}
                },
                "Averages": {
                    "Hydrogen Consumption/Biomass/Hr": {"Value": get_mean('AU', g6, h6), "Unit": "g/g/hr"},
                    "Carbon Dioxide Consumption/Biomass/Hr": {"Value": get_mean('AV', g6, h6), "Unit": "g/g/hr"},
                    "Oxygen Consumption Rate /Hr": {"Value": get_mean('AW', g6, h6), "Unit": "g/g/hr"}
                },
                "Stoichiometry": {"Actual": "", "Literature": ""},
                "% Mixotrophy": "Nan"
            }
        }

        # Write the summary to a JSON file
        with open('summary.json', 'w') as f:
            json.dump(summary, f, indent=20)

        return summary
