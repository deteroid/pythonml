# Import necessary libraries
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pandas.plotting import lag_plot, autocorrelation_plot
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# Load the dataset
url = "https://raw.githubusercontent.com/deteroid/pythonml/main/AirQualityUCI.csv"
df = pd.read_csv(url, sep=';', decimal=',')

# Convert 'Date' and 'Time' columns to datetime format with a specified format
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S')
df.set_index('Datetime', inplace=True)

# Select the new target variable for forecasting, i.e., 'CO(GT)'
target_variable = 'CO(GT)'

# Filter data for positive values only
positive_values_df = df[df[target_variable] > 0]

# Split the dataset into training and testing sets for positive values
train_size = int(len(positive_values_df) * 0.8)
train, test = positive_values_df[target_variable][:train_size], positive_values_df[target_variable][train_size:]

# Fit a more complex ARIMA model with hyperparameter tuning
order = (5, 1, 1)  # You may need to experiment with different orders
model = ARIMA(train, order=order)
fit_model = model.fit()

# Forecast using the fitted model for positive values
forecast_index = test.index
forecast = fit_model.forecast(steps=len(test), index=forecast_index)

# Drop rows with NaN values in both test and forecast
test = test.dropna()
forecast = forecast[test.index]

# Evaluate the model performance for positive values
rmse = sqrt(mean_squared_error(test, forecast))

# Dash application
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("ARIMA Forecast Dashboard"),
    
    # Dropdown for selecting different graphs
    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Original Time Series', 'value': 'original'},
            {'label': 'Histogram of CO(GT) Values', 'value': 'histogram'},
            {'label': 'Autocorrelation Plot', 'value': 'autocorrelation'},
            {'label': 'Scatter Plot of Forecast', 'value': 'scatter'},
            {'label': 'Residuals Plot', 'value': 'residuals'},
        ],
        value='original',  # Default selected value
        style={'width': '50%'}
    ),
    
    # Graph container
    dcc.Graph(id='selected-graph'),
    
    # Display RMSE
    html.Div(f'Root Mean Squared Error (RMSE) for Positive Values: {rmse}')
])

# Callback to update the selected graph based on the dropdown value
@app.callback(
    Output('selected-graph', 'figure'),
    [Input('graph-selector', 'value')]
)
def update_graph(selected_value):
    if selected_value == 'original':
        fig = go.Figure(data=[go.Scatter(x=positive_values_df.index, y=positive_values_df[target_variable], mode='lines', name='Original Time Series', line=dict(color='blue'))])
        fig.update_layout(title='Original Time Series', xaxis_title='Time', yaxis_title=target_variable)
    elif selected_value == 'histogram':
        fig = go.Figure(data=[go.Histogram(x=positive_values_df[target_variable], nbinsx=30, marker=dict(color='green', opacity=0.7))])
        fig.update_layout(title='Histogram of CO(GT) Values (Positive Values Only)', xaxis_title=target_variable, yaxis_title='Frequency')
    elif selected_value == 'autocorrelation':
        fig = go.Figure(data=[go.Scatter(x=lag_plot(positive_values_df[target_variable], lag=1).get_offsets()[:, 0], y=lag_plot(positive_values_df[target_variable], lag=1).get_offsets()[:, 1], mode='markers', marker=dict(color='orange'))])
        fig.update_layout(title='Autocorrelation Plot', xaxis_title='Lag', yaxis_title='Autocorrelation')
    elif selected_value == 'scatter':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=train.index, y=train, mode='markers', name='Train', marker=dict(color='blue', opacity=0.5)))
        fig.add_trace(go.Scatter(x=test.index, y=test, mode='markers', name='Test', marker=dict(color='green', opacity=0.5)))
        fig.add_trace(go.Scatter(x=test.index, y=forecast, mode='markers', name='ARIMA Forecast', marker=dict(color='red', opacity=0.5)))
        fig.update_layout(title='Scatter Plot of CO(GT) with Improved ARIMA Forecast (Positive Values Only)', xaxis_title='Time', yaxis_title=target_variable)
    elif selected_value == 'residuals':
        fig = go.Figure(data=[go.Scatter(x=residuals.index, y=residuals, mode='lines', name='Residuals', line=dict(color='purple'))])
        fig.update_layout(title='Residuals Plot', xaxis_title='Time', yaxis_title='Residuals')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
