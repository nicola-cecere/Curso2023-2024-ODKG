
import requests
import rdflib
from rdflib import Graph

def execute_query(wikidata_id):
    query = f"""
    SELECT ?population ?image ?coordinateLocation
    WHERE {{
      wd:{wikidata_id} wdt:P1082 ?population.
      wd:{wikidata_id} wdt:P18 ?image.
      wd:{wikidata_id} wdt:P625 ?coordinateLocation.
    }}
    """
    # Send the query to the Wikidata SPARQL endpoint and retrieve the results
    endpoint_url = 'https://query.wikidata.org/sparql'
    response = requests.get(endpoint_url, params={'query': query, 'format': 'json'})
    
    if response.status_code == 200:
        population_data = response.json()
        return population_data
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")


def execute_local_query(district_name):
    """
    Given an dsitrict name it generates th waste amount for each type of waste for each month
    :param district_name:
    :return:
    """
    graph = rdflib.Graph()
    graph.parse(
        #replace this with your path to the rdf graph
        "/home/meril/Documents/UPM/Curso2023-2024-ODKG/HandsOn/Group01/waste_management_dashboard/data/rdf-with-links.ttl",
        format="turtle")
    query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX nso: <http://madridwastemanagement.org/group01/ontology/>
        PREFIX wst: <http://www.disit.org/km4city/schema#>
        PREFIX time: <http://www.w3.org/2006/time#>

        SELECT ?wasteName ?wikidataLink ?m (SUM(?val) AS ?totalAmount)
        WHERE {{
          ?districtInstance a dbo:District ;
                            dbo:districtName "{district_name}";
                            wst:hasResidue ?wasteinstance.
          ?wasteinstance rdfs:label ?wasteName;
                         owl:sameAs ?wikidataLink;
                         nso:hasTotal ?totalinstance.
          ?totalinstance nso:value ?val;
                         time:month ?m.
        }}
        GROUP BY ?wasteName ?wikidataLink ?m
        ORDER BY ?m ?wasteName
        """
    results = graph.query(query)
    output = []
    for row in results:
        output_dict = {
            'wasteName': str(row[0]),
            'wikidataLink': str(row[1]),
            'month': str(row[2]),
            'totalAmount': str(row[3])
        }
        output.append(output_dict)
    return output