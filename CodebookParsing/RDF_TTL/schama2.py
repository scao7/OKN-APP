import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD

# Load the Excel file
file_path = r'D:\OKN_Front_End\Datasets\ruralurbancodes2013.xls'  # Update this with the actual file path
df = pd.read_excel(file_path)

# Define the namespaces
SCHEMA = Namespace("http://schema.org/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
QUDT = Namespace("http://qudt.org/vocab/unit/")

# Create a new RDF graph
g = Graph()

# Bind namespaces to prefixes
g.bind("schema", SCHEMA)
g.bind("geo", GEO)
g.bind("qudt", QUDT)
g.bind("rdf", RDF)

# Function to remove spaces from a string
def remove_spaces(value):
    if isinstance(value, str):
        return value.replace(" ", "")
    return value

# Process each row to match the schema.org ontology
for index, row in df.iterrows():
    fips = remove_spaces(row['FIPS'])
    state = remove_spaces(row['State'])
    county_name = remove_spaces(row['County_Name'])
    
    place_uri = URIRef(f"http://sailab.ua.edu/place/{fips}")
    
    # Add triples to the graph
    g.add((place_uri, RDF.type, SCHEMA.Place))
    g.add((place_uri, SCHEMA.identifier, Literal(fips, datatype=XSD.string)))
    
    address_uri = URIRef(f"http://sailab.ua.edu/address/{fips}")
    g.add((place_uri, SCHEMA.address, address_uri))
    g.add((address_uri, RDF.type, SCHEMA.PostalAddress))
    g.add((address_uri, SCHEMA.addressRegion, Literal(state, datatype=XSD.string)))
    g.add((address_uri, SCHEMA.addressLocality, Literal(county_name, datatype=XSD.string)))
    
    g.add((place_uri, SCHEMA.population, Literal(row["Population_2010"], datatype=XSD.integer)))
    g.add((place_uri, SCHEMA.category, Literal(row["RUCC_2013"], datatype=XSD.string)))
    g.add((place_uri, SCHEMA.description, Literal(row["Description"], datatype=XSD.string)))

# Serialize the graph to a TTL file
output_file = 'ontology_data.ttl'
g.serialize(destination=output_file, format='turtle')

print(f"Ontology data has been written to {output_file}")
