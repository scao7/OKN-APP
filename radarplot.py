import dash
from dash import dcc, html
import plotly.graph_objects as go
def create_radarplot():

	# 示例数据
	categories = ['力量', '速度', '智力', '耐力', '技巧']
	values = [80, 70, 85, 90, 75]

	# 创建雷达图
	fig = go.Figure()

	fig.add_trace(go.Scatterpolar(
		r=values,
		theta=categories,
		fill='toself',
		name='角色能力值'
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
