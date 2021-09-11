# Import required libraries
from logging import PlaceHolder
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout. The layout describes what the app looks like
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                    options = [
                                                    {"label": "All sites", "value": "All sites"},
                                                    {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                                                    {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                                                    {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                                    {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"}],                                                    
                                                    value="All sites",
                                                    placeholder="Select a Launch Site here",
                                                    searchable=True
                                                    )), #continue here
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                                marks={
                                    0: 0,
                                    2500: 2500,
                                    5000: 5000,
                                    7500.65: 7500,
                                    10000: 10000},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
siteList = sorted(list(set(spacex_df['Launch Site']))) # this list will be used later

@app.callback( # callback functions are automatically called by Dash whenever an inpute component's property changes
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

# I want a pie that shows the success rate by launch site
def get_pie(entered_site):
    if entered_site == "All sites":
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Successful Launches by Site')
        return fig
    elif entered_site == siteList[0]:
        launch1 = spacex_df[spacex_df['Launch Site']==siteList[0] ]
        fig = px.pie(launch1, names='class', title=siteList[0])
        return fig
    elif entered_site == siteList[1]:
        mySite = siteList[1]
        launch2 = spacex_df[spacex_df['Launch Site']==mySite]
        fig = px.pie(launch2, names='class', title=mySite)
        return fig
    elif entered_site == siteList[2]:
        mySite = entered_site
        launch2 = spacex_df[spacex_df['Launch Site']==mySite]
        fig = px.pie(launch2, names='class', title=mySite)
        return fig
    else:
        mySite = entered_site
        launch2 = spacex_df[spacex_df['Launch Site']==mySite]
        fig = px.pie(launch2, names='class', title=mySite)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
)

def get_scatter(entered_site, slider):
    if entered_site == "All sites":
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(slider[0], slider[1])], 
            x='Payload Mass (kg)', y='class', color='Booster Version Category', title="Correlation for All Sites")
        return fig
    else:
        filtered = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(filtered[filtered['Payload Mass (kg)'].between(slider[0], slider[1])], x='Payload Mass (kg)', y='class', 
            color='Booster Version Category', title="Correlation for " + entered_site)
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()

# A decorator is a function that takes another function and extends the behavior of the latter function.
# It wraps a function, modifying its behavior
# the @ symbol is sometimes called the "pie" syntax