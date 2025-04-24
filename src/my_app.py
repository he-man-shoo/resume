from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from PIL import Image
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go


def section_title(title):
    return html.H2(title, className="mt-5 mb-3", style={"textAlign": "center"})

profile_pic = Image.open("profile.png") #Profile picture path

# Experience Dataframe
experience_df = pd.read_excel("work_ex.xlsx", header=0) # Excel file path
# Add your experience data here

# Convert "Start_Date" and "End_Date" columns to datetime
experience_df['Start_Date'] = pd.to_datetime(experience_df['Start_Date'], errors='coerce')
experience_df['End_Date'] = pd.to_datetime(experience_df['End_Date'], errors='coerce')

experience_df.loc[experience_df['Company'] == 'Prevalon Energy LLC', 'End_Date'] = datetime.datetime.today()

experience_df['Company | Role'] = experience_df['Company'] + " | " + experience_df['Position']

custom_colors = {
            'Work Experience': 'rgb(252,215,87)',
            'Education': 'rgb(99,102,106)',
            }
        
fig = px.timeline(experience_df, x_start="Start_Date", x_end="End_Date", y="Company | Role", color='Category', color_discrete_map=custom_colors)


fig.update_layout(
    yaxis_title=""  # Set y-axis title to an empty string
    )

fig.update_yaxes(categoryorder='array', categoryarray=experience_df['Company | Role'])
fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
fig.update_xaxes(autorange="reversed") # otherwise tasks are listed from the bottom up

fig.update_traces(customdata=experience_df[['Location', 'Point 1', 'Point 2', 'Point 3']].values)

fig.update_traces(
    hovertemplate="<b>%{y}</b><br>" \
    "Location: %{customdata[0]}<br>" \
    " • %{customdata[1]}<br>" \
    " • %{customdata[2]}<br>" \
    " • %{customdata[3]}<br>" \
    "<extra></extra>"

)

        
fig.update_layout(
    plot_bgcolor='rgb(255, 255, 255)', # Light grey background 
    paper_bgcolor='rgb(255, 255, 255)', # Very light grey paper background                       

    xaxis=dict(showgrid=False, # Show gridlines 
                gridcolor='rgb(200, 200, 200)', # Gridline color 
                gridwidth=1, # Gridline width
                zeroline=False, # Remove zero line
                ),
    yaxis=dict( showgrid=True, # Show gridlines 
                gridcolor='rgb(200, 200, 200)', # Gridline color 
                gridwidth=0.5, # Gridline width 
                zeroline=False, # Remove zero line
                automargin=True,
                ),

    legend=dict(
        x=1,
        y=1,
        traceorder="reversed",
        title_font_family="Helvetica",
        font=dict(
            family="Helvetica",
            size=12,
            color="black"
        ),
    )
)

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP], 
            meta_tags=[{'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'}])

server = app.server


app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col(html.Img(src=profile_pic, style={"width": "100%"})
                , xs=6, sm=6, md=6, lg=6, xl=6),
        
        dbc.Col([
            html.H1("Himanshu Deshpande", className="text-center"),
            html.H4("Engineering | Energy Storage | Renewable Energy", className="text-center text-muted"),
            ], xs=6, sm=6, md=6, lg=6, xl=6, align="center"),
    ],justify="around"),  

    dbc.Row([
        dbc.Col(section_title("Experience")
                , xs=12, sm=12, md=12, lg=12, xl=12, align="center"),
    ],justify="center"),

    dbc.Row([
        dbc.Col([
            dbc.Spinner(dcc.Graph(id = "work_ex_gantt", figure = fig, style = {"height":"90vh", "width":"100%"}))
        ], xs=12, sm=12, md=12, lg=12, xl=12),
    ],justify="center"),

    html.Br(), html.Br(),
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)