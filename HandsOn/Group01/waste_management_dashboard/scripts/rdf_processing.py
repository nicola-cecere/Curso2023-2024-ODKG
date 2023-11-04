# Script for RDF data processing
sparql_query_template = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX nso: <http://madridwastemanagement.org/group01/ontology/>

SELECT ?wasteName ?m (SUM(?val) AS ?totalAmount)
WHERE {
  ?districtInstance a nso:District ;
                    nso:districtName "{district_name}"^^xsd:string;
                    nso:hasResidue ?wasteinstance.
  ?wasteinstance rdfs:label ?wasteName;
                 nso:hasTotal ?totalinstance.
  ?totalinstance nso:value ?val;
                 nso:month ?m.
}
GROUP BY ?wasteName ?m
ORDER BY ?m ?wasteName
"""

# Function to create a SPARQL query for a specific district name
def create_query_for_district(district_name):
    return sparql_query_template.format(district_name=district_name)
