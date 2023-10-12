# -*- coding: utf-8 -*-
"""Task08.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z-ma2cpKDi55SGNpcTyUdQcAYbH3nBsE

**Task 08: Completing missing data**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal, URIRef
g1 = Graph()
g2 = Graph()
g1.parse(github_storage+"/rdf/data01.rdf", format="xml")
g2.parse(github_storage+"/rdf/data02.rdf", format="xml")

"""Tarea: lista todos los elementos de la clase Person en el primer grafo (data01.rdf) y completa los campos (given name, family name y email) que puedan faltar con los datos del segundo grafo (data02.rdf). Puedes usar consultas SPARQL o iterar el grafo, o ambas cosas."""

from rdflib.plugins.sparql import prepareQuery
from rdflib import FOAF
from rdflib.namespace import RDF, RDFS
ns = Namespace("http://data.org#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

count = 0

print ("INITIAL G1")
for s, p, o in g1.triples((None, RDF.type, ns.Person)):
    for a, b, c in g1.triples((s, None, None)):
        count = count + 1;
        print(a, b, c)

print("Number of instances:", count)
count = 0

print ("INITIAL G2")
for s, p, o in g2.triples((None, RDF.type, ns.Person)):
    for a, b, c in g2.triples((s, None, None)):
        count = count + 1;
        print(a, b, c)
print("Number of instances:", count)
count = 0

for s,p,o in g1.triples((None, RDF.type, ns.Person)):
  for a,b,c in g2.triples((s, vcard.Given, None)):
    g1.add((s, b, c))
  for d,e,f in g2.triples((s, vcard.Family, None)):
    g1.add((s, e, f))
  for h,i,l in g2.triples((s, vcard.EMAIL, None)):
     g1.add((s, i, l))

print ("FINAL G1")
for s, p, o in g1.triples((None, RDF.type, ns.Person)):
    for a, b, c in g1.triples((s, None, None)):
        count = count + 1;
        print(a, b, c)

print("Number of instances:", count)