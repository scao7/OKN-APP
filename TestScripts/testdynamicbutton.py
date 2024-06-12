import dash
from dash import html
from dash.dependencies import Input, Output, State, ALL
import re

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(id='output-container'),
    html.Button('Button 1', id={'type': 'dynamic-button', 'index': 0}),
    html.Button('Button 2', id={'type': 'dynamic-button', 'index': 1}),
    html.Button('Button 3', id={'type': 'dynamic-button', 'index': 2}),
])

@app.callback(
    Output('output-container', 'children'),
    [Input({'type': 'dynamic-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'dynamic-button', 'index': ALL}, 'id'),
     State({'type': 'dynamic-button', 'index': ALL}, 'children')]
)
def handle_button_clicks(n_clicks, button_ids, button_labels):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "No button clicked yet."

    button_id_clicked_str = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Extract the index from the clicked button ID string using regular expression
    button_index = int(re.search(r'\d+', button_id_clicked_str).group())
    clicked_button_name = button_labels[button_index]
    
    return f"Clicked button name: {clicked_button_name}"

if __name__ == '__main__':
    app.run_server(debug=True)
