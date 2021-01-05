import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from builders import make_table
from data import countries_df, totals_df, dropdown_options
from dash.dependencies import Input, Output

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    size="Confirmed",
    projection="equirectangular",
    hover_name="Country_Region",
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    size_max=40,
    title="Confirmed By Country",
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    hover_data={
        "Confirmed": ":,",
        "Deaths": ":,",
        "Recovered": ":,",
        "Country_Region": False,
    },
)
bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                         coloraxis_colorbar=dict(xanchor="left", x=0))

bars_graph = px.bar(
    totals_df,
    x="condition",
    hover_data={"count": ":,"},
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    labels={
        "condition": "Condition",
        "count": "Count",
        "color": "Condition"
    },
)
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
        "x-scroll": "auto",
    },
    children=[
        html.Header(
            style={
                "textAlign": "center",
                "paddingTop": "50px",
                "marginBottom": 100,
            },
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})]),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(style={
            "display": "grid",
            "gap": 50,
            "gridTemplateColumns": "repeat(4, 1fr)",
        },
                 children=[
                     html.Div(children=[
                         dcc.Graph(figure=bars_graph),
                         html.Div(children=[
                             dcc.Dropdown(id="country",
                                          options=[{
                                              'label': country,
                                              'value': country
                                          } for country in dropdown_options]),
                        html.H1(id="country-output"),
                         ])
                     ]),
                 ])
    ],
)

map_figure = px.scatter_geo(countries_df)
map_figure.show()

if __name__ == "__main__":
    app.run_server(debug=True)


@app.callback(Output("country-output", "children"),
              [Input("country", "value")])
def update_hello(value):
    print(value)