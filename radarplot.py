import dash
from dash import dcc, html
import plotly.graph_objects as go
import dotenv
import os
from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
import pandas as pd
dotenv.load_dotenv()
password = os.environ["okn_database"]
engine = create_engine(f'postgresql+psycopg2://saillab:{password}@127.0.0.1:5432/postgres')
# df = pd.read_sql("SELECT rural_urban.county_fips, rural_urban.rucc FROM public.rural_urban ORDER BY rural_urban_id ASC", engine)

df1 = pd.read_sql("SELECT COUNT(*) AS rural_ratio FROM public.rural_urban",engine)
# print(df1)
df2 = pd.read_sql("SELECT COUNT(*) AS rural_ratio FROM public.rural_urban where rural_urban.rucc >3",engine)
# print(df2['rural_urban_rucc'])
rural_ratio = df2.iloc[0, 0]/df1.iloc[0, 0]
# print(rural_ratio)

df3 = pd.read_sql("SELECT SUM(population) AS rural_pupulation_ratio FROM public.rural_urban",engine)
# print(df3['rural_urban_population'])
df4 = pd.read_sql("SELECT SUM(population) AS rural_pupulation_ratio FROM public.rural_urban WHERE rural_urban.rucc>=3",engine)
# print(df3['rural_urban_population'])
rural_pupulation_ratio = df4.iloc[0, 0]/df3.iloc[0, 0]
# print(rural_pupulation_ratio)

df5 = pd.read_sql("SELECT COUNT(*) AS urban_ratio FROM public.rural_urban where rural_urban.rucc <=3",engine)
urban_ratio = df5.iloc[0, 0]/df1.iloc[0, 0]
# print(urban_ratio)



def create_radarplot():

	# 示例数据
	# categories = ['Rural \n ratio', 'Rural \n population\n ratio', 'Urban\n ratio', '# of\n treatment', 'variaty of\n treatment']

	categories = ['Rural \n ratio', 'Rural \n population\n ratio', 'Urban\n ratio']

	values = [rural_ratio*100, rural_pupulation_ratio*100, urban_ratio*100]

	print(values)
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
