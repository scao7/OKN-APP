import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

# Define namespaces
ex = Namespace("http://example.org/ontology#")

# Load the ontology template
g = Graph()
g.parse('ontology_template.ttl', format='turtle')

# Read data from Excel file
xls_file = r'D:\OKN_Front_End\Datasets\ruralurbancodes2013.xls'
df = pd.read_excel(xls_file)

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
        g.add((state_uri, RDF.type, ex.State))
        g.add((state_uri, ex.Description, Literal(state_name, datatype=XSD.string)))
    else:
        state_uri = states[state_name]

    # Create or retrieve the RUCC instance
    if rucc_code not in rucc_codes:
        rucc_uri = URIRef(f"http://example.org/rucc/{rucc_code}")
        rucc_codes[rucc_code] = rucc_uri
        g.add((rucc_uri, RDF.type, ex.RUCC))
        g.add((rucc_uri, ex.RUCCCode, Literal(rucc_code, datatype=XSD.integer)))
    else:
        rucc_uri = rucc_codes[rucc_code]

    # Add triples for each property using the ontology template
    g.add((county_uri, RDF.type, ex.County))
    g.add((county_uri, ex.FIPS, Literal(row['FIPS'], datatype=XSD.string)))
    g.add((county_uri, ex.hasState, state_uri))
    g.add((county_uri, ex.CountyName, Literal(row['County_Name'], datatype=XSD.string)))
    g.add((county_uri, ex.Population2010, Literal(int(row['Population_2010']), datatype=XSD.integer)))
    g.add((county_uri, ex.hasRUCC, rucc_uri))
    g.add((county_uri, ex.Description, Literal(row['Description'], datatype=XSD.string)))

# Serialize the RDF graph to a TTL file with UTF-8 encoding
output_file = 'county_instances.ttl'
g.serialize(destination=output_file, format='turtle', encoding='utf-8')

print(f"Instances added and saved to {output_file}.")
