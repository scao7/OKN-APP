create environment with 
```
conda create -n OKN python=3.10
```
install dash 
```
pip install dash 
```
install pandas
```
pip install pandas
```

Dash template website: https://dash.gallery/Portal/

Theme documentation
https://hellodash.pythonanywhere.com/theme-explorer/gallery

Project layout:
```
OKN
--assets
--Datasets # for survey data
--pages 
app.py
README.md
```

multipage design 

https://dash.plotly.com/urls

Mapbox map styles change to the following in the fig.update()
```
"open-street-map"
"carto-positron"
"carto-darkmatter"
"stamen-terrain"
"stamen-toner"
"stamen-watercolor"
"white-bg"
"basic"
"streets"
"outdoors"
"light"
"dark"
"satellite"
"satellite-streets"


```
USDA rural 2013 rural
```
https://www.ers.usda.gov/data-products/rural-urban-continuum-codes/
```

usa-state.geojson
```
https://github.com/PublicaMundi/MappingAPI/blob/master/data/geojson/us-states.json
```

usa-county.geojson
```
https://gist.github.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a#file-counties-geojson
```


PostgreSQL setup
```
pip install dash psycopg2 sqlalchemy
```

connecting to database 
```
postgresql+psycopg2://username:password@host:port/database
```

set password in envrionment variable 
```
import os
os.['okn_database'] = "password"
os.[OPENAI_API_KEY] = "password"
```
or in windows open the edit the system environment variable and restart the treminal	


table extracting script in the CodebookParsing 
```
pip install tabula-py
```
install java to run the tabula-py
https://www.oracle.com/java/technologies/downloads/#jdk22-windows

tabula-py need jpype install it using 
```
pip install jpype1
```

previous method requires many dependencis for java 

try to use the following package
```
pip install camelot-py[cv]
pip install 'PyPDF2<3.0' # the PyPDF latest version not working

```
example usage
```
import camelot

# Specify the path to your PDF file
pdf_path = "path/to/your/pdf_file.pdf"

# Extract tables from the PDF
tables = camelot.read_pdf(pdf_path, pages='all')

# Print the tables or save them to CSV files
for i, table in enumerate(tables):
    print(f"Table {i}")
    print(table.df)
    table.to_csv(f"table_{i}.csv")
```
Looks like both package need java


use geopy to get the lantitude and longitude 
https://geopy.readthedocs.io/en/stable/#geopy-is-not-a-service
https://operations.osmfoundation.org/policies/nominatim/
https://planet.openstreetmap.org/
```
pip install geopy
```
example
```
from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

# Define the address
address = "1600 Amphitheatre Parkway, Mountain View, CA"

# Get the location
location = geolocator.geocode(address)

# Print latitude and longitude
if location:
    print(f"Address: {address}")
    print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
else:
    print("Location not found")

```

if use google api use the google geocoding api 
https://developers.google.com/maps/billing-and-pricing/billing#geocoding
