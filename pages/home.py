
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html,MATCH, ALL
from openai import OpenAI
from textwrap import dedent
import plotly.graph_objs as go
import networkx as nx
import os
from interactivemap import create_map,query_clinic,get_coordinates,get_place_id,get_website,query_clinic_google
from getfacilities import get_facility_website
from dash.exceptions import PreventUpdate
import re
import json
# from dash.dependencies import Input, Output, State, MATCH, ALL
# place_holder = html.Div(
#     [
#         dbc.Placeholder(color="primary", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="secondary", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="success", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="warning", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="danger", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="info", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="light", className="me-1 mt-1 w-100",button=True),
#         dbc.Placeholder(color="dark", className="me-1 mt-1 w-100",button=True),
#     ]
# )
google_api_key=os.environ.get("GoogleMAP_API")
openmapbox = create_map()
data_scatter = {}
services=None 


# G = nx.Graph()

# # Add nodes and edges
# G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])


# def generate_graph():
#     pos = nx.spring_layout(G)  # Positioning the nodes

#     edge_trace = go.Scatter(
#         x=[],
#         y=[],
#         line=dict(width=1, color='#888'),
#         hoverinfo='none',
#         mode='lines')

#     for edge in G.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_trace['x'] += (x0, x1, None)
#         edge_trace['y'] += (y0, y1, None)

#     node_trace = go.Scatter(
#         x=[],
#         y=[],
#         text=[],
#         mode='markers+text',
#         hoverinfo='text',
#         marker=dict(
#             showscale=True,
#             colorscale='YlGnBu',
#             size=10,
#             colorbar=dict(
#                 thickness=15,
#                 title='Node Connections',
#                 xanchor='left',
#                 titleside='right'
#             )))

#     for node in G.nodes():
#         x, y = pos[node]
#         node_trace['x'] += (x,)
#         node_trace['y'] += (y,)
#         node_trace['text'] += (str(node),)
    


#     return html.Div([
#                 dcc.Graph(
#                     id='network-graph',
#                     figure={
#                         'data': [edge_trace, node_trace],
#                         'layout': go.Layout(
#                             title='Network Graph',
#                             showlegend=False,
#                             hovermode='closest',
#                             margin=dict(b=20, l=5, r=5, t=40),
#                             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
#                         )
#                     }
#                 )
#             ])

# graph = generate_graph()

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
            "height": "calc(55vh - 132px)",
            "flex-direction": "column-reverse",
        },
    )

    controls = dbc.InputGroup(
        children=[  
            dbc.Input(id="user-input", placeholder="Write to the chatbox...", type="text"),
            dbc.Button("Ask AI", id="submit"),
        ]
    )
    controls_query =dbc.InputGroup(
        children=[
            dbc.Input(id="query-input", placeholder="Write to the qeury...", type="text"),
            dbc.Button("Query",id = "submit_query",color="secondary"),
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
                controls_query,
                dbc.Spinner(html.Div(id="loading-component")),
            ],
        )
        
    )

    treatment_agency = html.Div(
        dbc.Container(
            fluid= True,
            children=[
                html.H3("Treatmemt Agency",className='h3'),
                dcc.Loading(
                    id="agency",
                    type="circle",
                    children=[
                        services,
                    ],
                    overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"},
                    custom_spinner=html.H2(["Loading", dbc.Spinner(color="danger")]), 
                )   

            ]
             
        )
    )

    agency_info = html.Div(
        dcc.Loading(
            id="output-container",
            # children=[
            #     'test'
            # ]
        )
    )

    home = html.Div(
		[
			dbc.Row(
				[
					dbc.Col(
						[
							html.Div([
								html.H3("MAP",className="h3"),
                                dcc.Loading(
                                    id="openmap_render",
                                    type="circle",
                                    children=[
                                        openmapbox,
                                    ],
                                    overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"},
                                    custom_spinner=html.H2(["Loading", dbc.Spinner(color="danger")]), 
                                ),
                                
							],
                            className="border rounded")
						],
						# md=7,
                        style={"marginLeft": "10px"}
					),

					dbc.Col(
						[
						chatbox
						],
						# md=5,
						className="border rounded"
					) 
				]
			),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col([
                            treatment_agency
                            ],
                           
                            style={"marginLeft": "10px"},
                            className="border rounded",
                            ),

                    dbc.Col([html.H3("Angency Info",className='h3'),
                            agency_info,
                            ],
                          
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
        [Output("user-input", "value"), Output("query-input", "value")],
        [Input("submit", "n_clicks"), Input("user-input", "n_submit"),Input("submit_query", "n_clicks"),Input("query-input", "n_submit")],
        
    )
    def clear_input(n_clicks1, n_submit,n_clicks_query,n_submit_query):
        return "",""

    @dash.callback(
        [Output("store-conversation", "data"), Output("loading-component", "children"), Output("openmap_render","children"),Output("agency","children")],
        [Input("submit", "n_clicks"), Input("user-input", "n_submit"),Input("submit_query", "n_clicks"),Input("query-input", "n_submit")],
        [State("user-input", "value"),State("query-input", "value"), State("store-conversation", "data")],
    )
    def dialog(n_clicks, n_submit,n_clicks2,n_submit2,user_input, query_input,chat_history):
        ctx = dash.callback_context
        button_id = None
        if ctx.triggered:
            print("ctx",ctx.triggered[0]['prop_id'])
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        result = "",None,openmapbox,services
        if button_id == 'submit':
            result= run_chatbot(n_clicks, n_submit,user_input, chat_history)
        elif button_id == 'submit_query':
            result= run_query(n_clicks2, n_submit2,query_input, chat_history)
        return result
        # return 'Unexpected button clicked',None

    def run_chatbot(n_clicks, n_submit,user_input, chat_history):
        if n_clicks == 0 and n_submit is None:
            return "", None, openmapbox, services

        if user_input is None or user_input == "":
            return chat_history, None,openmapbox,services

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

        return chat_history, None,openmapbox,services

    def run_query(n_clicks, n_submit,user_input, chat_history):
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

        
        data_scatter = query_clinic(user_input)


        print(data_scatter)
        model_output = f"the query is {user_input}:{data_scatter} "

        if data_scatter:
            openmapbox = create_map(data_scatter)
        else:
            openmapbox = create_map()
        # print(data_scatter)
        button_styles = ["primary","secondary","success","warning","danger","info","light","dark"]
        services =  html.Div(
            [dbc.Button(button['name']+" " +button['info'] , color=button_styles[idx % 8], className="me-1",id={'type': 'dynamic-button', 'index': idx},style={"width":"100%"}) for idx, button in enumerate(data_scatter)],
            id='button-container'
        )
        chat_history += f"{model_output}<split>"


        return chat_history, None,openmapbox,services


        # Callback to handle button clicks
    @dash.callback(
        Output('output-container', 'children'),
        [Input({'type': 'dynamic-button', 'index': ALL}, 'n_clicks')],
        [State({'type': 'dynamic-button', 'index': ALL}, 'id'),
        State({'type': 'dynamic-button', 'index': ALL}, 'children')]
    )

    def dynamic_button_logic(n_clicks, button_ids,button_labels):
        ctx = dash.callback_context
        if not ctx.triggered:
            return "No agency selected yet."

        button_id_clicked_str = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Extract the index from the clicked button ID string using regular expression
        button_index = int(re.search(r'\d+', button_id_clicked_str).group())
        clicked_button_name = button_labels[button_index]
        address= clicked_button_name
        print(address)
        
        web_info  =get_facility_website(google_api_key,address)
        json_string = json.dumps(web_info, indent=4)
        data_dict = json.loads(json_string)
        print(data_dict)
        # lat, lng = get_coordinates(address, google_api_key)
        # place_id = get_place_id(lat, lng, google_api_key)
        # web_info = get_website(place_id,google_api_key)

        out_layout = html.Div(
            [html.H3(data_dict['result']['name']),
            html.P(data_dict['result']['rating']),
            html.P(data_dict['result']['formatted_address']),
            html.P(data_dict['result']['formatted_phone_number']),
            html.P(data_dict['result']['website']),
            # html.P(data_dict['result']['opening_hours']),
            ]
        )
        return out_layout
        


        
        


    return home
    