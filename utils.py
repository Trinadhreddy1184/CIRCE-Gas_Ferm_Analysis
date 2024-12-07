# utils.py

class Utils:
    @staticmethod
    def excel_column_names(n):
        # This method generates Excel-like column names (A, B, C, ..., Z, AA, AB, etc.)
        # for a given number of columns (n).
        result = []  # List to store all the column names
        for i in range(1, n + 1):  # Loop through numbers 1 to n (inclusive)
            column_name = []  # List to store individual characters of the column name
            while i > 0:
                # Calculate the current character index in the column name
                i, remainder = divmod(i - 1, 26)
                column_name.append(chr(ord('A') + remainder))  # Convert the remainder to the corresponding letter
            result.append(''.join(column_name[::-1]))  # Reverse the characters and form the complete column name
        return result  # Return the list of all column names

    @staticmethod
    def safe_mean(series):
        # This method calculates the mean of a given Pandas series,
        # but returns NaN if the series is empty.
        return series.mean() if not series.empty else float('nan')
