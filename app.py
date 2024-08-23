import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, ui, render, reactive

# Load data
covid_data = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

# Filter and select data
countries = ["United States", "United Kingdom", "India", "Japan", "China", 
             "Brazil", "Germany", "Canada", "Mexico", "Italy"]

count_data = covid_data[covid_data['location'].isin(countries)]
count_data = count_data[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

world_data = covid_data[covid_data['location'] == "World"]
world_data = world_data[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

last_row = world_data.iloc[-1]
last_update = f"Last Update: {last_row['date']}"

# Create plots
def create_country_graphs(dtype):
    if dtype == 1:
        y_col = 'total_cases'
        title = 'Number of Total Cases Over Time per Country'
    elif dtype == 2:
        y_col = 'new_cases'
        title = 'Number of New Cases Over Time per Country'
    elif dtype == 3:
        y_col = 'total_deaths'
        title = 'Number of Total Deaths Over Time per Country'
    else:
        y_col = 'new_deaths'
        title = 'Number of New Deaths Over Time per Country'

    fig = px.line(count_data, x='date', y=y_col, color='location', facet_col='location', facet_col_wrap=5,
                  title=title, labels={y_col: ''})
    fig.update_yaxes(tickformat=",")
    fig.update_layout(showlegend=False)
    return fig

def create_world_graphs(dtype):
    if dtype == 1:
        y_col = 'total_cases'
        title = 'Number of Total Cases in the World Over Time'
    elif dtype == 2:
        y_col = 'new_cases'
        title = 'Number of New Cases in the World Over Time'
    elif dtype == 3:
        y_col = 'total_deaths'
        title = 'Number of Total Deaths in the World Over Time'
    else:
        y_col = 'new_deaths'
        title = 'Number of New Deaths in the World Over Time'

    fig = px.line(world_data, x='date', y=y_col, title=title, labels={y_col: ''})
    fig.update_yaxes(tickformat=",")
    return fig

# UI layout
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_radio_buttons('dtype', 'Type:', 
                                   choices={'Total Cases': 1, 'New Cases': 2, 'Total Deaths': 3, 'New Deaths': 4}),
            ui.output_text('interact'),
            ui.output_text('update'),
            ui.output_text('disclaimer')
        ),
        ui.panel_main(
            ui.h2("Country Data"),
            ui.output_plot('plot1'),
            ui.h2("World Data"),
            ui.output_plot('plot2')
        )
    )
)

# Server logic
def server(input, output, session):
    @output
    @render.text
    def interact():
        return 'The plots are interactive. You can use the tools at the top right of the figure to manipulate the graphs! :)'

    @output
    @render.text
    def update():
        return last_update

    @output
    @render.text
    def disclaimer():
        return ('This dashboard was made as a practice exercise for learning Python shiny. This is not official health '
                'information and should not be used as such.')

    @output
    @render.plot
    def plot1():
        dtype = input.dtype()
        return create_country_graphs(dtype)

    @output
    @render.plot
    def plot2():
        dtype = input.dtype()
        return create_world_graphs(dtype)

# Create the app
app = App(app_ui, server)
