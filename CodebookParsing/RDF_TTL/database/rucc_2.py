import psycopg2
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, XSD

# Define Namespaces
OKN = Namespace("http://sail.ua.edu/okn/")
RUCC = Namespace("http://sail.ua.edu/okn/rucc/")

# postgresql+psycopg2://postgres:{password}@127.0.0.1:5432/dummy
# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host='127.0.0.1',
    dbname='onto',
    user='postgres',
    password='Cst1995!',
    port='5432'
)
cursor = conn.cursor()
cursor1 = conn.cursor()
cursor2 = conn.cursor()
cursor3 = conn.cursor()

# Initialize RDF Graph
g = Graph()

# Fetch and process data
# Fetch States
cursor.execute("SELECT state_id, state_name, state_abbr, fips FROM state")
for state_id, state_name, state_abbr, fips in cursor.fetchall():
    state_uri = RUCC[f"State_{state_abbr}"]
    g.add((state_uri, RDF.type, RUCC.State))
    g.add((state_uri, RUCC.name, Literal(state_name, datatype=XSD.string)))
    g.add((state_uri, RUCC.abbreviation, Literal(state_abbr, datatype=XSD.string)))
    g.add((state_uri, RUCC.fips, Literal(fips, datatype=XSD.string)))

    # Fetch Counties in this State
    cursor1.execute("SELECT county_id, county_name, fips as county_fips FROM county WHERE state_id = %s", (state_id,))
    for county_id, county_name, county_fips in cursor1.fetchall():
        county_uri = RUCC[f"County_{county_fips}"]
        g.add((county_uri, RDF.type, RUCC.County))
        g.add((county_uri, RUCC.name, Literal(county_name, datatype=XSD.string)))
        g.add((county_uri, RUCC.fips, Literal(fips, datatype=XSD.string)))
        g.add((state_uri, RUCC.containsPlace, county_uri))
        
        
        # Fetch RUCC related to this County
        cursor2.execute("SELECT rucc_id, rucc_code, description, year FROM rucc")
        for rucc_id, rucc_code, description, year in cursor2.fetchall():
            rucc_uri = RUCC[f"rucc_{rucc_code}"]
            g.add((rucc_uri, RDF.type, RUCC.RUCC))
            cursor3.execute("SELECT rural_urban_id, rural_urban_code, population, rucc FROM rural_urban WHERE rural_urban_code = %s", (county_fips,))
            for rural_urban_id, rural_urban_code, population, rucc in cursor3.fetchall():
                # if rucc_uri == RUCC[f"{rucc}"]:
                g.add((county_uri,RUCC.hasRUCC,RUCC[f"rucc_{rucc}"]))
                g.add((county_uri,RUCC.population,Literal(population,datatype=XSD.integer)))

            g.add((rucc_uri, RUCC.code, Literal(rucc_code, datatype=XSD.string)))
            g.add((rucc_uri, RUCC.description, Literal(description, datatype=XSD.string)))
            g.add((rucc_uri, RUCC.year, Literal(year, datatype=XSD.integer)))
            
            

        # cursor.execute("SELECT rural_urban_id, rural_urban_code, population, rucc FROM rural_urban WHERE rural_urban_code = %s", (county_fips,))
        # for rural_urban_id, rural_urban_code, population, rucc in cursor.fetchall():
        #     rucc_uri = RUCC[f"RUCC_{rural_urban_id}"]
        #     g.add((county_uri, RUCC.hasRUCC, rucc_uri))
        #     g.add((rucc_uri, RUCC.population, Literal(population, datatype=XSD.integer)))

        #     # Fetch RUCC details
        #     cursor.execute("SELECT rucc_id, rucc_code, description, year FROM rucc WHERE rucc_code = %s", (rucc,))
        #     rucc_id, rucc_code, description, year = cursor.fetchone()
        #     g.add((rucc_uri, RDF.type, RUCC.RUCC_Code))
        #     g.add((rucc_uri, RUCC.code, Literal(rucc_code, datatype=XSD.string)))
        #     g.add((rucc_uri, RUCC.description, Literal(description, datatype=XSD.string)))
        #     g.add((rucc_uri, RUCC.year, Literal(year, datatype=XSD.integer)))

# Close database connection
conn.close()

# Serialize the RDF graph to a TTL file
output_file = 'rucc_ontology2.ttl'
g.serialize(destination=output_file, format='turtle')
print(f"RDF graph serialized and saved to {output_file}.")