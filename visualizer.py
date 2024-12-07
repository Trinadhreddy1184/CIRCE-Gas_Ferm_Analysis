import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly as px
from dash import Dash, dcc, html
import plotly.graph_objs as go


class DataVisualizer:
    def __init__(self, df):
        # Initialize the DataVisualizer class with the provided DataFrame
        self.df = df

    def plot_interactive_scatter(self):
        # Extracting x-values (time) and y-values (gas concentrations) for the scatter plot
        x_values = self.df['C']
        y_values = {
            "O2": self.df['AT'],  # Oxygen concentration data
            "CO2": self.df['AS'],  # Carbon Dioxide concentration data
            "H2": self.df['AR']  # Hydrogen concentration data
        }

        # Create a DataFrame that consolidates all x and y values for easier plotting
        plot_df = pd.DataFrame({
            "X": pd.concat([x_values] * 3, ignore_index=True),
            "Y": pd.concat([y_values["O2"], y_values["CO2"], y_values["H2"]], ignore_index=True),
            "Gas": ["O2"] * len(x_values) + ["CO2"] * len(x_values) + ["H2"] * len(self.df['AR'])
        })

        # Create an interactive scatter plot using Plotly
        fig = go.Figure()

        # Adding traces for each gas type (O2, CO2, H2) to the figure
        fig.add_trace(go.Scatter(x=x_values, y=y_values['O2'], mode='markers', name='O2'))
        fig.add_trace(go.Scatter(x=x_values, y=y_values['CO2'], mode='markers', name='CO2'))
        fig.add_trace(go.Scatter(x=x_values, y=y_values['H2'], mode='markers', name='H2'))

        # Update the layout of the plot to add titles and labels
        fig.update_layout(
            title="Gas Consumption Rate",
            xaxis_title="Hours from Inoculation",
            yaxis_title="Consumption rate (mmol/L/hr)",
            legend_title="Gas Type",
            title_font_size=14,
            xaxis_title_font_size=12,
            yaxis_title_font_size=12,
            legend_title_font_size=10
        )

        # Save the plot as a PNG image
        fig.write_image('summary_scatterplot.png')

        # Display the interactive plot
        fig.show()

        # Uncomment below code to run the Dash server for a more interactive web-based visualization
        # app = Dash()
        # app.layout = html.Div([
        #     dcc.Graph(figure=fig)
        # ])
        # app.run_server(debug=True, use_reloader=False)
