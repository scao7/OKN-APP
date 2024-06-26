import psycopg2
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD

# Function to connect to PostgreSQL and fetch schema information
def fetch_postgres_schema(db_params):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute("SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'public';")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# Function to construct ontology template
def construct_ontology_template(rows):
    g = Graph()
    onto = Namespace("http://example.org/ontology#")

    for row in rows:
        table_name, column_name, data_type = row

        class_uri = onto[table_name]
        g.add((class_uri, RDF.type, OWL.Class))

        property_uri = onto[column_name]
        g.add((property_uri, RDF.type, OWL.DatatypeProperty))
        g.add((property_uri, RDFS.domain, class_uri))

        # Define range based on PostgreSQL data types
        if data_type == 'integer':
            g.add((property_uri, RDFS.range, XSD.int))
        elif data_type == 'text':
            g.add((property_uri, RDFS.range, XSD.string))
        # Add more conditions for other data types as needed

    return g

# Database connection parameters
db_params = {
    'host': '127.0.0.1',
    'database': 'onto',
    'user': 'postgres',
    'password': 'Cst1995!',
    'port':'5432'
}

# Fetch PostgreSQL schema
schema_rows = fetch_postgres_schema(db_params)

# Construct ontology template
ontology_graph = construct_ontology_template(schema_rows)

# Serialize RDF graph to TTL format
ttl_output = ontology_graph.serialize(format='turtle')

# Print or save TTL output
print(ttl_output)

# Optionally, save TTL output to a file
with open('ontology_template_from_db.ttl', 'w') as f:
    f.write(ttl_output)
