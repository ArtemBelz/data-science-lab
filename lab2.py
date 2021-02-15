import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

provinces = {
    "Черкаси": 25,
    "Чернігів": 27,
    "Чернівці": 26,
    "Крим": 12,
    "Дніпропетровськ": 3,
    "Донецьк": 4,
    "Івано-Франківськ": 8,
    "Харків": 22,
    "Херсон": 23,
    "Хмельницький": 24,
    "Київ область": 10,
    "Київ": 9,
    "Кіровоград": 11,
    "Луганськ": 13,
    "Львів": 14,
    "Миколаїв": 15,
    "Одеса": 16,
    "Полтава": 17,
    "Рівне": 18,
    "Севастополь": 19,
    "Суми": 20,
    "Тернопіль": 21,
    "Закарпаття": 6,
    "Вінниця": 1,
    "Волинь": 2,
    "Запоріжжя": 7,
    "Житомир": 5
}

df = pd.read_csv('all_data.csv')


def filter_df(provinces, years, weeks):
    if provinces is None:
        provinces = [1]
    return df[(df.province.isin(provinces)) & (df.year.isin(range(years[0], years[1] + 1))) & (
        df.week.isin(range(weeks[0], weeks[1] + 1)))]


def create_graph(df, type):
    return px.bar(df, x="week", y=type, color="province", barmode="group", facet_row="year", facet_col="week")


def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label('Выберите города'),
    dcc.Dropdown(
        id='provinces-dropdown',
        options=[
            {'label': i, 'value': provinces[i]} for i in provinces
        ],
        multi=True
    ),
    html.Div(id='dd-output-container'),
    html.Label('Выберите года'),
    dcc.RangeSlider(
        id='years-slider',
        min=1982,
        max=2020,
        step=1,
        value=[2019, 2020]
    ),
    html.Div(id='output-container-years-slider'),
    html.Label('Выберите недели'),
    dcc.RangeSlider(
        id='weeks-slider',
        min=1,
        max=52,
        step=1,
        value=[1, 3]
    ),
    html.Div(id='output-container-weeks-slider'),
    dcc.Graph(
        id='VCI-graph'
    ),
    dcc.Graph(
        id='TCI-graph'
    ),
    dcc.Graph(
        id='VHI-graph'
    ),
    html.Table(id='data-container')
])


@app.callback(
    dash.dependencies.Output('VCI-graph', 'figure'),
    dash.dependencies.Output('TCI-graph', 'figure'),
    dash.dependencies.Output('VHI-graph', 'figure'),
    dash.dependencies.Output('data-container', 'children'),

    [dash.dependencies.Input('provinces-dropdown', 'value'),
     dash.dependencies.Input('years-slider', 'value'),
     dash.dependencies.Input('weeks-slider', 'value')])
def update_output(provinces, years, weeks):
    dff = filter_df(provinces, years, weeks)
    return create_graph(dff, "VCI"), create_graph(dff, "TCI"), create_graph(dff, "VHI"), generate_table(dff)


@app.callback(
    dash.dependencies.Output('output-container-years-slider', 'children'),
    [dash.dependencies.Input('years-slider', 'value')])
def update_output(value):
    return f'Вы выбрали: "{value}"'


@app.callback(
    dash.dependencies.Output('output-container-weeks-slider', 'children'),
    [dash.dependencies.Input('weeks-slider', 'value')])
def update_output(value):
    return f'Вы выбрали: "{value}"'


if __name__ == '__main__':
    app.run_server(debug=True)
