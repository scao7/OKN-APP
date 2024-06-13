from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

# Define namespaces
ONT = Namespace("http://example.com/ontology#")  # Replace with your ontology URI
GEO = Namespace("http://www.geonames.org/ontology#")  # Example namespace, adjust as per your ontology

def verify_ontology(ttl_file):
    # Load the ontology from TTL file
    g = Graph()
    g.parse(ttl_file, format='turtle')

    # Perform ontology verification checks
    print("Ontology Verification Results:")
    
    # Example checks:
    
    # Check if all cities have a population value
    query = """
    SELECT DISTINCT ?city WHERE {
        ?city rdf:type geo:City .
        FILTER NOT EXISTS {
            ?city ont:hasPopulation ?population .
        }
    }
    """
    results = g.query(query, initNs={"rdf": RDF, "geo": GEO, "ont": ONT})
    if len(results) > 0:
        print("Cities without population:")
        for row in results:
            print(row.city)

    # Check for inconsistent data or missing relationships
    # Example: Check if there are any cities without a state assigned
    query = """
    SELECT DISTINCT ?city WHERE {
        ?city rdf:type geo:City .
        FILTER NOT EXISTS {
            ?city ont:hasState ?state .
        }
    }
    """
    results = g.query(query, initNs={"rdf": RDF, "geo": GEO, "ont": ONT})
    if len(results) > 0:
        print("Cities without state assignment:")
        for row in results:
            print(row.city)

    # Add more checks as per your ontology's structure and requirements

if __name__ == "__main__":
    ttl_file = 'ontology.ttl'  # Replace with your TTL file path
    verify_ontology(ttl_file)
