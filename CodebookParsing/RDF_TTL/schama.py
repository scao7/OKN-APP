import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

# Load the Excel file
file_path = r'D:\OKN_Front_End\Datasets\ruralurbancodes2013.xls'  # Update this with the actual file path
df = pd.read_excel(file_path)

# Define the schema.org namespace
SCHEMA = Namespace("http://schema.org/")

# Create a new RDF graph
g = Graph()

# Bind the schema.org namespace to a prefix
g.bind("schema", SCHEMA)

# Process each row to match the schema.org ontology
for index, row in df.iterrows():
    place = URIRef(f"http://example.org/place/{row['FIPS']}")

    # Add triples to the graph
    g.add((place, RDF.type, SCHEMA.Place))
    g.add((place, SCHEMA.identifier, Literal(row["FIPS"], datatype=XSD.string)))
    g.add((place, SCHEMA.address, URIRef(f"http://example.org/address/{row['FIPS']}")))
    
    address = URIRef(f"http://example.org/address/{row['FIPS']}")
    g.add((address, RDF.type, SCHEMA.PostalAddress))
    g.add((address, SCHEMA.addressRegion, Literal(row["State"], datatype=XSD.string)))
    g.add((address, SCHEMA.addressLocality, Literal(row["County_Name"], datatype=XSD.string)))
    
    g.add((place, SCHEMA.population, Literal(row["Population_2010"], datatype=XSD.integer)))
    g.add((place, SCHEMA.category, Literal(row["RUCC_2013"], datatype=XSD.string)))
    g.add((place, SCHEMA.description, Literal(row["Description"], datatype=XSD.string)))

# Serialize the graph to a TTL file
output_file = 'ontology_data.ttl'
g.serialize(destination=output_file, format='turtle')

print(f"Ontology data has been written to {output_file}")
