import dash
from dash import dcc, html
import plotly.graph_objects as go
def create_radarplot():

	# 示例数据
	categories = ['Rural \n ratio', 'Rural \n population\n ratio', 'Urban\n ratio', '# of\n treatment', 'variaty of\n treatment']
	values = [80, 70, 85, 90, 75]

	# 创建雷达图
	fig = go.Figure()

	fig.add_trace(go.Scatterpolar(
		r=values,
		theta=categories,
		fill='toself',
		name='State determinants'
	))

	fig.update_layout(
		polar=dict(
			radialaxis=dict(
				visible=True,
				range=[0, 100]
			)),
		showlegend=True
	)

	# 定义应用程序布局
	return html.Div(children=[
		html.H3(children='Rual risk analysis'),

		dcc.Graph(
			id='example-graph',
			figure=fig
		)
	])
