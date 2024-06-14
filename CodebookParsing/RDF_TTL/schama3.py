import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Define namespaces
schema = Namespace("http://schema.org/")
example = Namespace("http://saillab.ua.edu/")

# Read data from Excel file
df = pd.read_excel(r'D:\OKN_Front_End\Datasets\ruralurbancodes2013.xls')

# Initialize RDF Graph
g = Graph()

# Iterate over rows and add instances to the RDF graph
for index, row in df.iterrows():
    county_id = f"county_{index}"  # Generate a unique identifier for each county instance
    county_uri = example[county_id]

    # Add triples for each property using schema.org terms
    g.add((county_uri, RDF.type, schema.AdministrativeArea))
    g.add((county_uri, schema.identifier, Literal(row['FIPS'], datatype=XSD.string)))
    g.add((county_uri, schema.identifier, Literal(row['State'], datatype=XSD.string)))
    g.add((county_uri, schema.name, Literal(row['County_Name'], datatype=XSD.string)))
    g.add((county_uri, schema.population, Literal(int(row['Population_2010']), datatype=XSD.integer)))
    g.add((county_uri, schema.description, Literal(row['Description'], datatype=XSD.string)))
    # Assuming there's no direct equivalent for RUCC_2013 in schema.org, you may use a custom property:
    try:
        g.add((county_uri, example.hasRUCC_2013, Literal(int(row['RUCC_2013']), datatype=XSD.integer)))
    except:
        print("wrong")

# Serialize the RDF graph to a TTL file
output_file = 'county_ontology.ttl'
with open(output_file, 'w') as f:
    f.write(g.serialize(format='turtle'))

print(f"Instances added and saved to {output_file}.")
