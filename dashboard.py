import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# Load the dataset
url = "https://raw.githubusercontent.com/deteroid/pythonml/main/AirQualityUCI.csv"
df = pd.read_csv(url, sep=';', decimal=',')
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S')
df.set_index('Datetime', inplace=True)

# Filter data for positive values only
positive_values_df = df[df['CO(GT)'] > 0]

# Split the dataset into training and testing sets for positive values
train_size = int(len(positive_values_df) * 0.8)
train, test = positive_values_df['CO(GT)'][:train_size], positive_values_df['CO(GT)'][train_size:]

# Fit ARIMA model
order = (5, 1, 1)
model = ARIMA(train, order=order)
fit_model = model.fit()

# Forecast using the fitted model
forecast = fit_model.forecast(steps=len(test))

# Evaluate model performance
rmse = sqrt(mean_squared_error(test, forecast))

# Dash application
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("ARIMA Forecast Dashboard"),
    
    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Original Time Series', 'value': 'original'},
            {'label': 'CO(GT) Histogram Against Time', 'value': 'histogram'},
            {'label': 'Autocorrelation Plot', 'value': 'autocorrelation'},
            {'label': 'Scatter Plot', 'value': 'scatter'},
        ],
        value='original',  
        style={'width': '50%'}
    ),
    
    dcc.Graph(id='selected-graph'),
    
    html.Div(f'RMSE for Positive Values: {rmse}')
])

# Callback to update the selected graph based on the dropdown value
@app.callback(
    Output('selected-graph', 'figure'),
    [Input('graph-selector', 'value')]
)
def update_graph(selected_value):
    fig = go.Figure()

    if selected_value == 'original':
        fig.add_trace(go.Scatter(x=positive_values_df.index, y=positive_values_df['CO(GT)'], mode='lines', name='Original Time Series', line=dict(color='blue')))
        fig.update_layout(title='Original Time Series', xaxis_title='Time', yaxis_title='CO(GT)')
    elif selected_value == 'histogram':
        fig.add_trace(go.Histogram(x=positive_values_df.index, y=positive_values_df['CO(GT)'], nbinsx=30, marker=dict(color='green', opacity=0.7)))
        fig.update_layout(title='CO(GT) Histogram Against Time', xaxis_title='Time', yaxis_title='Frequency')
    elif selected_value == 'autocorrelation':
        lag_plot_df = pd.DataFrame({'lag1': positive_values_df['CO(GT)'].shift(1)})
        fig.add_trace(go.Scatter(x=lag_plot_df['lag1'], y=positive_values_df['CO(GT)'], mode='markers', marker=dict(color='orange')))
        fig.update_layout(title='Autocorrelation Plot', xaxis_title='Lag', yaxis_title='Autocorrelation')
    elif selected_value == 'scatter':
        fig.add_trace(go.Scatter(x=train.index, y=train, mode='markers', name='Train', marker=dict(color='blue', opacity=0.5)))
        fig.add_trace(go.Scatter(x=test.index, y=test, mode='markers', name='Test', marker=dict(color='green', opacity=0.5)))
        fig.add_trace(go.Scatter(x=test.index, y=forecast, mode='markers', name='ARIMA Forecast', marker=dict(color='red', opacity=0.5)))
        fig.update_layout(title='Scatter Plot with ARIMA Forecast', xaxis_title='Time', yaxis_title='CO(GT)')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
