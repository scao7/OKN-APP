
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from openai import OpenAI
from textwrap import dedent
import plotly.graph_objs as go
import networkx as nx
import os
from interactivemap import create_map

openmapbox = create_map()

G = nx.Graph()

# Add nodes and edges
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])


def generate_graph():
    pos = nx.spring_layout(G)  # Positioning the nodes

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (str(node),)
    


    return html.Div([
                dcc.Graph(
                    id='network-graph',
                    figure={
                        'data': [edge_trace, node_trace],
                        'layout': go.Layout(
                            title='Network Graph',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        )
                    }
                )
            ])

graph = generate_graph()

def create_home():
    def Header(name, app):
        title = html.H3(name, className= "h3")
        logo = html.Img(
            src=app.get_asset_url("UALogo.jpg"), style={"float": "right", "height": 60}
        )
        return dbc.Row([dbc.Col(title), dbc.Col(logo)])

    def textbox(text, box="AI", name="OKN"):
        text = text.replace(f"{name}:", "").replace("You:", "")
        style = {
            "max-width": "80%",
            "width": "100%",
            "padding": "5px 10px",
            "border-radius": 25,
            "margin-bottom": 20,
        }

        if box == "user":
            style["margin-left"] = "auto"
            style["margin-right"] = 0

            return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

        elif box == "AI":
            style["margin-left"] = 0
            style["margin-right"] = "auto"

            thumbnail = html.Img(
                src=dash.get_asset_url("UALogo.jpg"),
                style={
                    "border-radius": 50,
                    "height": 36,
                    "margin-right": 5,
                    "float": "left",
                },
            )
            textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

            return html.Div([thumbnail, textbox])

        else:
            raise ValueError("Incorrect option for `box`.")


    description = """
    OKN is a open knowlege graph building team in University of Alabama. Could You help analysis medical and rural health data?
    """

    # Authentication
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY")

    )
    # Load images
    IMAGES = {"OKN": dash.get_asset_url("UALogo.jpg")}


    # Define Layout
    conversation = html.Div(
        html.Div(id="display-conversation"),
        style={
            "overflow-y": "auto",
            "display": "flex",
            "height": "calc(50vh - 132px)",
            "flex-direction": "column-reverse",
        },
    )

    controls = dbc.InputGroup(
        children=[
            dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text"),
            dbc.Button("Submit", id="submit")
        ]
    )

    raw_query_box = dbc.InputGroup(
        children=[
            dbc.Input(id="user-input", placeholder="Write raw query input...", type="text"),
            dbc.Button("Submit", id="submit")
        ]
    )

    chatbox = html.Div(
        dbc.Container(
            fluid=True,
            children=[
                Header("Chatbot", dash),
                html.Hr(),
                dcc.Store(id="store-conversation", data=""),
                conversation,
                controls,
                dbc.Spinner(html.Div(id="loading-component")),
            ],
        )
        
    )
    



    place_holder = html.Div(
        [
            dbc.Placeholder(color="primary", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="secondary", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="success", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="warning", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="danger", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="info", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="light", className="me-1 mt-1 w-100",button=True),
            dbc.Placeholder(color="dark", className="me-1 mt-1 w-100",button=True),
        ]
    )
    home = html.Div(
		[
			dbc.Row(
				[
					dbc.Col(
						[
							html.Div([
								html.H3("Open street map",className='mt-auto'),
								# html.Iframe(
								# 	src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d497695.0212663337!2d-74.25986413519108!3d40.697589547260245!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c24fa5d33f083b%3A0xc80b8f06e177fe62!2sNew%20York%2C%20NY!5e0!3m2!1sen!2sus!4v1621073910982!5m2!1sen!2sus",
								# 	width="100%",
								# 	height="500"
								# )
                                openmapbox
							],className="border rounded")
					
						],
						md=7,
                        className="mt-auto"
					),
					dbc.Col(
						[
                        raw_query_box,
                        html.Hr(),
						chatbox
						],
						md=5,
						className="border rounded"
			
					)
				]
			),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col([html.H3("Service provided by selected treatment agency",className='h3'),
                             place_holder
                            ],
                            md=7,
                            className="border rounded",
                            ),

                    dbc.Col([html.H3("Client satisfaction & Peer Review",className='h3'),
                            place_holder,
                            ],
                            md=5,
                            
                            className="border rounded"),
                ],
            
            )
            ]
	)



    # chatbox
    @dash.callback(
        Output("display-conversation", "children"), [Input("store-conversation", "data")]
    )
    def update_display(chat_history):
        return [
            textbox(x, box="user") if i % 2 == 0 else textbox(x, box="AI")
            for i, x in enumerate(chat_history.split("<split>")[:-1])
        ]


    @dash.callback(
        Output("user-input", "value"),
        [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    )
    def clear_input(n_clicks, n_submit):
        return ""


    @dash.callback(
        [Output("store-conversation", "data"), Output("loading-component", "children")],
        [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
        [State("user-input", "value"), State("store-conversation", "data")],
    )
    def run_chatbot(n_clicks, n_submit, user_input, chat_history):
        if n_clicks == 0 and n_submit is None:
            return "", None

        if user_input is None or user_input == "":
            return chat_history, None

        name = "OKN"

        prompt = dedent(
            f"""
        {description}

        You: Hello {name}!
        {name}: Hello! Glad to be talking to you today.
        """
        )

        # First add the user input to the chat history
        chat_history += f"You: {user_input}<split>{name}:"

        model_input = prompt + chat_history.replace("<split>", "\n")

        response = client.chat.completions.create(
            messages=[
            {
                "role": "user",
                "content": model_input,
            }
            ],
            model="gpt-3.5-turbo",
        )
        model_output = response.choices[0].message.content.strip()

        chat_history += f"{model_output}<split>"

        return chat_history, None

    return home
    