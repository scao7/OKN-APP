from dash import html
from dash import dcc
from dash.dependencies import Input, Output
# from app import app

layout = html.Div([
    html.H1('Resource Page'),
    html.P("some description about the data"),
	html.P('''
        Childersburg VA Clinic		151 9th Avenue NW		Childersburg	AL	35044
        Clanton MI Outpatient		110 Medical Center Drive		Clanton	AL	35045
        WellStone Inc		1909 Commerce Avenue NW		Cullman	AL	35055
        Health Connect America		801 Church Street NE 	Suite 6	Decatur	AL	35601
        MHCNCA Inc	Decatur/Morgan Counseling Center	4110 U.S. Highway 31 South		Decatur	AL	35603
        MHCNCA Inc	The Albany Clinic for Children	1315 13th Avenue SE		Decatur	AL	35601
        West Alabama Mental Health Center		1215 South Walnut Avenue		Demopolis	AL	36732
        West Alabama Mental Health Center		1401 U.S. Highway 80 East		Demopolis	AL	36732
        West Alabama Mental Health Center	Springhill Home	1304 Old Springhill Road		Demopolis	AL	36732
        Whitfield Regional Hospital IPF	Gerpsych/Adult Psych	105 Highway 80 East		Demopolis	AL	36732

        ''')
])

