#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from base64 import encode
from msilib.schema import Class
from token import ENCODING
import rdflib
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib import BNode
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD
import pandas as pd
import pprint
from rdflib import BNode


def csv_owl_final(subclass, domain_axiom, range_axiom, instances, subproperty, inverse, onproperty, somevaluesfrom, owlclass, g):
    g = Graph()

    # CLASS
    class1 = owlclass.iloc[:, 0].values
    for a in class1:
        if (a.rsplit('/')[0] == 'http:'):
            owl_class = URIRef(a)
            g.add((owl_class, RDF.type, OWL.Class))
        else:
            owl_class = BNode(a)
            g.add((owl_class, RDF.type, OWL.Class))

    # SUBCLASS
    parent = subclass.iloc[:, 1].values
    classs = subclass.iloc[:, 0].values
    import math
    # for a in classs:
    #     # url="http://example.org/ontology/"+a
    #     if (a.rsplit('/')[0]=='http:'):
    #         class1=URIRef(a)
    #         g.add((class1 ,RDF.type, OWL.Class))
    #     else:
    #         class1=BNode(a)
    #         g.add((class1,RDF.type, OWL.Class))

    for (a, b) in zip(classs, parent):

        if (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] == 'http:'):
            class1 = URIRef(a)
            class2 = URIRef(b)
            g.add((class1, RDFS.subClassOf, class2))
        elif (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] != 'http:'):
            class2 = URIRef(b)
            class1 = BNode(a)
            g.add((class1, RDFS.subClassOf, class2))
        elif (b.rsplit('/')[0] != 'http:') and (a.rsplit('/')[0] == 'http:'):
            class1 = URIRef(a)
            class2 = BNode(b)
            g.add((class1, RDFS.subClassOf, class2))
        else:
            class1 = BNode(a)
            class2 = BNode(b)
            g.add((class1, RDFS.subClassOf, class2))
        # # url1="http://example.org/ontology/"+a
        # class1=URIRef(a)
        # # url2="http://example.org/ontology/"+b
        # class2=URIRef(b)
        # g.add((class1, RDFS.subClassOf, class2))
        # else:
        #     # url1="http://example.org/ontology/"+a
        #     class1=URIRef(a)
        #     g.add((class1,RDF.type, OWL.Class))

    # DOMAIN
    object = domain_axiom.iloc[:, 0].values
    domain = domain_axiom.iloc[:, 1].values
    for (a, b) in zip(object, domain):
        # url1="http://example.org/ontology/"+a
        obj = URIRef(a)
        # url2="http://example.org/ontology/"+b
        dom = URIRef(b)
        g.add((obj, RDF.type, OWL.ObjectProperty))
        g.add((obj, RDFS.domain, dom))

    # RANGE
    col1 = range_axiom.iloc[:, 0].values
    col2 = range_axiom.iloc[:, 1].values
    for (a, b) in zip(col1, col2):
        url1 = "http://example.org/ontology/"+a
        obj = URIRef(a)
        url2 = "http://example.org/ontology/"+b
        range = URIRef(b)
        g.add((obj, RDF.type, OWL.ObjectProperty))
        g.add((obj, RDFS.range, range))

    # INSTANCES
    col1 = instances.iloc[:, 0].values
    col2 = instances.iloc[:, 1].values
    for (a, b) in zip(col1, col2):
        url1 = "http://example.org/ontology/"+a
        object = URIRef(a)
        url2 = "http://example.org/ontology/"+b
        classs = URIRef(b)
        g.add((object, RDF.type, classs))

    # SUBPROPERTY
    col1 = subproperty.iloc[:, 0].values
    col2 = subproperty.iloc[:, 1].values
    for (a, b) in zip(col1, col2):
        uri1 = "http://example.org/ontology/"+a
        subprop = URIRef(a)
        uri2 = "http://example.org/ontology/"+b
        object = URIRef(b)
        g.add((subprop, RDFS.subPropertyOf, object))

    # INVERSE
    col1 = inverse.iloc[:, 0].values
    col2 = inverse.iloc[:, 1].values
    for (a, b) in zip(col1, col2):
        uri1 = "http://example.org/ontology/"+a
        subprop = URIRef(a)
        uri2 = "http://example.org/ontology/"+b
        object = URIRef(b)
        g.add((subprop, OWL.inverseOf, object))

    # OnProperty
    col1 = onproperty.iloc[:, 0].values
    col2 = onproperty.iloc[:, 1].values
    for (a, b) in zip(col1, col2):
        if (a.rsplit('/')[0] == 'http:'):
            classs = URIRef(a)
            property = URIRef(b)
            g.add((classs, OWL.onProperty, property))
        else:
            print(a)
            nodeid = BNode(a)
            property = URIRef(b)
            g.add((nodeid, OWL.onProperty, property))

    # someValuesFrom
    col1 = somevaluesfrom.iloc[:, 0].values
    col2 = somevaluesfrom.iloc[:, 1].values
    for (a, b) in zip(col1, col2):
        if (a.rsplit('/')[0] == 'http:'):
            classs = URIRef(a)
            property = URIRef(b)
            g.add((classs, OWL.someValuesFrom, property))
        else:
            print(a)
            nodeid = BNode(a)
            property = URIRef(b)
            g.add((nodeid, OWL.someValuesFrom, property))

    g.serialize(destination='output.owl', format='xml')


def main(file):
    g = Graph()
    owlclass = pd.read_excel(file, sheet_name='owlclass')
    subclass = pd.read_excel(file, sheet_name='subclass')
    domain_axiom = pd.read_excel(file, sheet_name='domain')
    range_axiom = pd.read_excel(file, sheet_name='range')
    instances = pd.read_excel(file, sheet_name='instances')
    subproperty = pd.read_excel(file, sheet_name='subproperty')
    inverse = pd.read_excel(file, sheet_name='inverseOf')
    onproperty = pd.read_excel(file, sheet_name='onproperty')
    somevaluesfrom = pd.read_excel(file, sheet_name='somevaluesfrom')

    csv_owl_final(subclass, domain_axiom, range_axiom, instances,
                  subproperty, inverse, onproperty, somevaluesfrom, owlclass, g)
