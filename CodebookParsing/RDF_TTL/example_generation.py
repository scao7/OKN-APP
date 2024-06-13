import xlrd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

# Define namespaces
SCHEMA = Namespace("http://schema.org/")
GEO = Namespace("http://www.geonames.org/ontology#")
ONT = Namespace("http://example.com/ontology#")  # Replace with your ontology URI

# Load XLS data
def load_xls(filename):
    data = []
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)  # Read first sheet

    # Read header row
    headers = [cell.value.strip() for cell in sheet.row(0)]

    # Read data rows
    for row_idx in range(1, sheet.nrows):
        row_data = {}
        for col_idx in range(sheet.ncols):
            row_data[headers[col_idx]] = sheet.cell_value(row_idx, col_idx)
        data.append(row_data)

    return data

# Create RDF triples
def create_rdf_from_xls(data):
    g = Graph()
    print(data)
    for entry in data:
        # Define subjects and objects
        city_name = entry['County_Name']
        population_literal = Literal(entry['Population_2010'], datatype=XSD.integer)
        rucc_code_literal = Literal(entry['RUCC_2013'], datatype=XSD.string)
        rucc_desc_literal = Literal(entry['Description'], datatype=XSD.string)
        state_literal = Literal(entry['State'], datatype=XSD.string)
        fips_literal = Literal(entry['FIPS'], datatype=XSD.string)

        # Create URI for the city
        city_uri = URIRef(GEO + f"{city_name.replace(' ', '_')}")

        # Add triples
        g.add((city_uri, RDF.type, GEO.City))
        g.add((city_uri, RDFS.label, Literal(city_name, datatype=XSD.string)))
        g.add((city_uri, ONT.hasPopulation, population_literal))
        g.add((city_uri, ONT.hasRucc, rucc_code_literal))
        g.add((city_uri, ONT.hasRuccDescription, rucc_desc_literal))
        g.add((city_uri, ONT.hasState, state_literal))
        g.add((city_uri, ONT.hasFIPS, fips_literal))

    return g

# Save RDF graph to TTL file
def save_ttl(graph, filename):
    with open(filename, 'w') as f:
        f.write(graph.serialize(format='turtle'))

if __name__ == "__main__":
    xls_filename = r'D:\OKN_Front_End\Datasets\ruralurbancodes2013.xls'  # Replace with your XLS file path
    ttl_filename = r'ontology.ttl'  # Output TTL file name

    data = load_xls(xls_filename)
    rdf_graph = create_rdf_from_xls(data)
    save_ttl(rdf_graph, ttl_filename)

    print(f"Ontology generated successfully and saved to {ttl_filename}")
