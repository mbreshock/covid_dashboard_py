import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from shiny import App, ui, render, reactive

# Load data
covid_data = pd.read_csv("https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv")

# get date of the last update
last_row = covid_data.iloc[-1]
last_update = f"Last Update: {last_row['date']}"

# refactor date column
covid_data['date'] = pd.to_datetime(covid_data['date'])

# Filter and select data
countries = ["United States", "United Kingdom", "India", "Japan", "China", 
             "Brazil", "Germany", "Canada", "Mexico", "Italy"]

count_data = covid_data[covid_data['country'].isin(countries)]
count_data = count_data[['country', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

world_data = covid_data[covid_data['country'] == "World"]
world_data = world_data[['country', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

# Create plots
def create_country_graphs(dtype):
    if dtype == '1':
        y_col = 'total_cases'
        title = 'Number of Total Cases Over Time per Country'
        y_lab = 'Cases (Total)'
    elif dtype == '2':
        y_col = 'new_cases'
        title = 'Number of New Cases Over Time per Country'
        y_lab = 'Cases (New)'
    elif dtype == '3':
        y_col = 'total_deaths'
        title = 'Number of Total Deaths Over Time per Country'
        y_lab = 'Deaths (Total)'
    else:
        y_col = 'new_deaths'
        title = 'Number of New Deaths Over Time per Country'
        y_lab = 'Deaths (New)'

    # Create the Figure and Axes objects
    fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axes

    # Create the Seaborn line plot on the Axes object
    sns.lineplot(data=count_data, x='date', y=y_col, hue='country', ax=ax)

    # Set the title and labels
    ax.set_title(title)
    ax.set_ylabel(y_lab) 

     # Format the x-axis ticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()

    # Format the y-axis ticks to include commas
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f'{int(x):,}'))

    # Hide the legend
    # ax.legend([],[], frameon=False)
    return fig

def create_world_graphs(dtype):
    if dtype == '1':
        y_col = 'total_cases'
        title = 'Number of Total Cases in the World Over Time'
        y_lab = 'Cases (Total)'
    elif dtype == '2':
        y_col = 'new_cases'
        title = 'Number of New Cases in the World Over Time'
        y_lab = 'Cases (New)'
    elif dtype == '3':
        y_col = 'total_deaths'
        title = 'Number of Total Deaths in the World Over Time'
        y_lab = 'Deaths (Total)'
    else:
        y_col = 'new_deaths'
        title = 'Number of New Deaths in the World Over Time'
        y_lab = 'Deaths (New)'

    # Create the Figure and Axes objects
    fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axes

    # Create the Seaborn line plot on the Axes object
    sns.lineplot(data=world_data, x='date', y=y_col, ax=ax)

    # Set the title and labels
    ax.set_title(title)
    ax.set_ylabel(y_lab) 

    # Format the x-axis ticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()

    # Format the y-axis ticks to include commas
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f'{int(x):,}'))

    # Hide the legend
    # ax.legend([],[], frameon=False)
    return fig

# UI layout
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h1("COVID-19 Dashboard"),
            ui.input_radio_buttons('dtype', 'Metric', 
                                   choices={1:'Total Cases', 2:'New Cases', 3:'Total Deaths', 4:'New Deaths'}),
            ui.output_text('disclaimer'), 
            ui.output_ui("source"),
            ui.output_text('update'),
            ui.output_ui("author")
        ),
        ui.h2("Country Data"),
        ui.output_plot('plot1'),
        ui.h2("World Data"),
        ui.output_plot('plot2')
    )
)

# Server logic
def server(input, output, session):

    @output
    @render.text
    def update():
        return last_update

    @output
    @render.text
    def disclaimer():
        return ('This dashboard was made as a practice exercise for learning Shiny for Python. This is not official health '
                'information and should not be used as such.')
    
    @reactive.calc
    def source_url():
        return ui.tags.a("Our World in Data", href='https://docs.owid.io/projects/etl/api/covid/', target='_blank')
    
    @render.ui
    def source(): 
        return ui.div("Data comes from: ", source_url())
    
    @reactive.calc
    def author_url():
        return ui.tags.a("Michael Breshock", href='https://mbreshock.github.io/index.html', target='_blank')
    
    @render.ui
    def author(): 
        return ui.div("Created by ", author_url())

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
