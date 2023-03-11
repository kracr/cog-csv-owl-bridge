#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from base64 import encode
from msilib.schema import Class
from token import ENCODING
import rdflib
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF,XSD
from rdflib import BNode
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
import pandas as pd
import pprint

def csv_owl_final(subclass,domain_axiom, range_axiom, instances,subproperty,inverse, g):
    g=Graph()
    
    #SUBCLASS
    parent=subclass.iloc[:,1].values
    classs=subclass.iloc[:,0].values
    import math
    for a in classs:
        url="http://example.org/ontology/"+a
        class1=URIRef(url)
        g.add((class1,RDF.type, RDFS.Class))
    
    for (a,b) in zip(classs, parent):
        if b==b:
            url1="http://example.org/ontology/"+a
            class1=URIRef(url1)
            url2="http://example.org/ontology/"+b
            class2=URIRef(url2)
            g.add((class1, RDFS.subClassOf, class2))
        else:
            url1="http://example.org/ontology/"+a
            class1=URIRef(url1)
            g.add((class1,RDF.type, RDFS.Class))
        
    #DOMAIN
    object=domain_axiom.iloc[:,0].values
    domain=domain_axiom.iloc[:,1].values
    for (a,b) in zip(object, domain):
        url1="http://example.org/ontology/"+a
        obj=URIRef(url1)
        url2="http://example.org/ontology/"+b
        dom=URIRef(url2)
        g.add((obj,RDF.type,OWL.ObjectProperty))
        g.add((obj,RDFS.domain,dom))


    #RANGE 
    col1=range_axiom.iloc[:,0].values
    col2=range_axiom.iloc[:,1].values
    for (a,b) in zip(col1, col2):
        url1="http://example.org/ontology/"+a
        obj=URIRef(url1)
        url2="http://example.org/ontology/"+b
        range=URIRef(url2)
        g.add((obj,RDF.type,OWL.ObjectProperty))
        g.add((obj,RDFS.range,range))


    #INSTANCES
    col1=instances.iloc[:,0].values
    col2=instances.iloc[:,1].values
    for (a,b) in zip(col1, col2):
        url1="http://example.org/ontology/"+a
        object=URIRef(url1)
        url2="http://example.org/ontology/"+b
        classs=URIRef(url2)
        g.add((object, RDF.type, classs))

    #SUBPROPERTY
    col1=subproperty.iloc[:,0].values
    col2=subproperty.iloc[:,1].values
    for (a,b) in zip(col1,col2):
        uri1="http://example.org/ontology/"+a
        subprop=URIRef(uri1)
        uri2="http://example.org/ontology/"+b
        object=URIRef(uri2)
        g.add((subprop, RDFS.subPropertyOf, object))

    #INVERSE
    col1=inverse.iloc[:,0].values
    col2=inverse.iloc[:,1].values
    for (a,b) in zip(col1,col2):
        uri1="http://example.org/ontology/"+a
        subprop=URIRef(uri1)
        uri2="http://example.org/ontology/"+b
        object=URIRef(uri2)
        g.add((subprop, OWL.inverseOf, object))

    
    g.serialize(destination='output.owl', format='pretty-xml')

def main(file):
    g = Graph()
    subclass = pd.read_excel(file, sheet_name='subclass')
    domain_axiom=pd.read_excel(file, sheet_name='domain')
    range_axiom=pd.read_excel(file, sheet_name='range')
    instances=pd.read_excel(file, sheet_name='instances')
    subproperty=pd.read_excel(file, sheet_name='subproperty')
    inverse=pd.read_excel(file, sheet_name='inverseOf')
    csv_owl_final(subclass,domain_axiom, range_axiom, instances, subproperty,inverse, g)
