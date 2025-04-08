# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All sites', 'value': 'All'}, 
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, 
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    placeholder='Select a Launch Site here',
                                    searchable=True,
                                    value='All'
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, 
                                    max=10000, 
                                    step=1000,
                                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000'},
                                    value=[0, 10000]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def update_pie_chart(selected_site):
    # If-Else logic based on whether "ALL" or a specific site is selected
    if selected_site == 'All':
        # Use all rows in spacex_df to calculate total success launches
        total_counts = spacex_df['class'].value_counts()
        fig = px.pie(
            names=['Failed (0)', 'Success (1)'],
            values=[total_counts.get(0, 0), total_counts.get(1, 0)],
            title='Total Success vs Failed Launches (All Sites)'
        )
    else:
        # Filter the DataFrame for the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Calculate success and failed counts for the selected site
        site_counts = filtered_df['class'].value_counts()
        fig = px.pie(
            names=['Failed (0)', 'Success (1)'],
            values=[site_counts.get(0, 0), site_counts.get(1, 0)],
            title=f'Success vs Failed Launches for {selected_site}'
        )
    
    # Return the pie chart figure
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)

def update_scatter_chart(selected_site, payload_range):
    # Filter by payload range (applies to both ALL and specific site cases)
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= min_payload) & 
        (spacex_df['Payload Mass (kg)'] <= max_payload)
    ]

    # If-Else logic based on whether "ALL" or a specific site is selected
    if selected_site == 'All':
        # Use all rows within the payload range
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload Mass vs Success/Failure (All Sites)',
            labels={'class': 'Launch Outcome (0=Failed, 1=Success)'}
        )
    else:
        # Further filter by the selected launch site
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            site_filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload Mass vs Success/Failure for {selected_site}',
            labels={'class': 'Launch Outcome (0=Failed, 1=Success)'}
        )
    
    # Customize the scatter plot (optional)
    fig.update_layout(
        yaxis=dict(tickvals=[0, 1], ticktext=['Failed', 'Success']),
        xaxis_title='Payload Mass (kg)',
        yaxis_title='Launch Outcome'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
