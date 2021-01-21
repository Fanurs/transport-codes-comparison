import dash
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies as dependencies
import plotly.graph_objects as go
import numpy as np
import pandas as pd

x = np.linspace(0, 2, 100)
y = x**2
curve = go.Scatter(x=x, y=y)
fig = go.Figure(data=[curve])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H2('Nuclear reaction: transport codes comparison'),
    html.Div([
        'Input: ',
        dcc.Slider(
            id='slider', value=2,
            updatemode='drag',
            min=0, max=3, step=0.01,
            marks={round(x, 1): {'label': f'{x:.1f}'} for x in np.arange(0, 3.1, 0.5)},
        ),
    ]),
    html.Br(),
    dcc.Graph(id='curve', figure=fig),
    html.Button(id='save-button', children='save', n_clicks=0),
    html.Br(),
    html.Div(id='save-msg', children=None),
])

@app.callback(
    dependencies.Output('curve', 'figure'),
    dependencies.Input('slider', 'value'),
)
def update_figure(value):
    global curve, fig
    fig.update_traces(dict(y=x**float(value)), selector=0)
    fig.update_layout(title=f'{value:3.1f}')
    return fig

@app.callback(
    dependencies.Output('save-msg', 'children'),
    dependencies.Input('save-button', 'n_clicks'),
    dependencies.State('slider', 'value'),
)
def update_database(n_clicks, value):
    if n_clicks == 0:
        return ''

    with open('./data.txt', 'w') as f:
        f.write(f'>> {value:3.2f}\n')
    return 'Input has been saved to "./data.txt".'

if __name__ == '__main__':
    app.run_server(
        host='127.0.0.1', port=9595,
        debug=True,
        dev_tools_ui=False, 
        dev_tools_props_check=False,
    )

