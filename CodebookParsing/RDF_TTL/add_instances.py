import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

# Define namespaces
example = Namespace("http://example.org/ontology#")

# Load the ontology template
g = Graph()
g.parse('ontology_template.ttl', format='turtle')

# Read data from CSV file with the correct encoding
df = pd.read_excel(r'D:\OKN_Front_End\Datasets\ruralurbancodes2013.xls')

# Cache State and RUCC instances
states = {}
rucc_codes = {}

# Iterate over rows and add instances to the RDF graph
for index, row in df.iterrows():
    county_id = f"county_{row['FIPS']}"
    county_uri = URIRef(f"http://example.org/county/{county_id}")
    state_name = row['State']
    rucc_code = row['RUCC_2013']

    # Create or retrieve the State instance
    if state_name not in states:
        state_uri = URIRef(f"http://example.org/state/{state_name.replace(' ', '_')}")
        states[state_name] = state_uri
        g.add((state_uri, RDF.type, example.State))
        g.add((state_uri, example.Description, Literal(state_name, datatype=XSD.string)))
    else:
        state_uri = states[state_name]

    # Create or retrieve the RUCC instance
    if rucc_code not in rucc_codes:
        rucc_uri = URIRef(f"http://example.org/rucc/{rucc_code}")
        rucc_codes[rucc_code] = rucc_uri
        g.add((rucc_uri, RDF.type, example.RUCC))
        g.add((rucc_uri, example.RUCCCode, Literal(rucc_code, datatype=XSD.integer)))
    else:
        rucc_uri = rucc_codes[rucc_code]

    # Add triples for each property using the ontology template
    g.add((county_uri, RDF.type, example.County))
    g.add((county_uri, example.FIPS, Literal(row['FIPS'], datatype=XSD.string)))
    g.add((county_uri, example.hasState, state_uri))
    g.add((county_uri, example.CountyName, Literal(row['County_Name'], datatype=XSD.string)))
    g.add((county_uri, example.Population2010, Literal(int(row['Population_2010']), datatype=XSD.integer)))
    g.add((county_uri, example.hasRUCC, rucc_uri))
    g.add((county_uri, example.Description, Literal(row['Description'], datatype=XSD.string)))

# Serialize the RDF graph to a TTL file
output_file = 'county_instances.ttl'
with open(output_file, 'w') as f:
    f.write(g.serialize(format='turtle'))

print(f"Instances added and saved to {output_file}.")
