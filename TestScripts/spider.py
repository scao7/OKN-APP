import dash
from dash import dcc, html
import plotly.graph_objects as go

# 创建一个 Dash 应用程序
app = dash.Dash(__name__)

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
app.layout = html.Div(children=[
    html.H1(children='角色战力图'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)
