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


def csv_owl_final(subclass, domain_axiom, range_axiom, instances, subproperty, inverse, allvaluesfrom, somevaluesfrom,maxcardinality, owlclass, firstrest, g):
    global iri_dict
    
    g = Graph()

    # CLASS
    class1 = owlclass.iloc[:, 0].values
    for c1 in class1:
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing
        
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

    for (c1, p1) in zip(classs, parent):

        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=p1.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

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
    for (o1, d1) in zip(object, domain):

        s=o1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=d1.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        if (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] == 'http:'):
            obj = URIRef(a)
            dom = URIRef(b)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.domain, dom))
        elif (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] != 'http:'):
            obj = URIRef(b)
            dom = BNode(a)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.domain, dom))
        elif (b.rsplit('/')[0] != 'http:') and (a.rsplit('/')[0] == 'http:'):
            obj = URIRef(a)
            dom = BNode(b)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.domain, dom))
        else:
            obj = BNode(a)
            dom = BNode(b)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.domain, dom))
        # url1="http://example.org/ontology/"+a
        # obj = URIRef(a)
        # # url2="http://example.org/ontology/"+b
        # dom = URIRef(b)
        # g.add((obj, RDF.type, OWL.ObjectProperty))
        # g.add((obj, RDFS.domain, dom))

    # RANGE
    col1 = range_axiom.iloc[:, 0].values
    col2 = range_axiom.iloc[:, 1].values
    for (c1, c2) in zip(col1, col2):
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        if (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] == 'http:'):
            obj = URIRef(a)
            range = URIRef(b)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.range, range))
        elif (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] != 'http:'):
            obj = URIRef(b)
            range = BNode(a)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.range, range))
        elif (b.rsplit('/')[0] != 'http:') and (a.rsplit('/')[0] == 'http:'):
            obj = URIRef(a)
            range = BNode(b)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.range, range))
        else:
            obj = BNode(a)
            range = BNode(b)
            g.add((obj, RDF.type, OWL.ObjectProperty))
            g.add((obj, RDFS.range, range))
        # url1 = "http://example.org/ontology/"+a
        # obj = URIRef(a)
        # # url2 = "http://example.org/ontology/"+b
        # range = URIRef(b)
        # g.add((obj, RDF.type, OWL.ObjectProperty))
        # g.add((obj, RDFS.range, range))

    # INSTANCES
    col1 = instances.iloc[:, 0].values
    col2 = instances.iloc[:, 1].values
    for (c1, c2) in zip(col1, col2):

        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        if (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] == 'http:'):
            object = URIRef(a)
            classs = URIRef(b)
            g.add((object, RDF.type, classs))
            g.add((object, RDF.type, OWL.NamedIndividual))
        elif (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] != 'http:'):
            object = URIRef(b)
            classs = BNode(a)
            g.add((object, RDF.type, classs))
            g.add((object, RDF.type, OWL.NamedIndividual))
        elif (b.rsplit('/')[0] != 'http:') and (a.rsplit('/')[0] == 'http:'):
            object = URIRef(a)
            classs = BNode(b)
            g.add((object, RDF.type, classs))
            g.add((object, RDF.type, OWL.NamedIndividual))
        else:
            object = BNode(a)
            classs = BNode(b)
            g.add((object, RDF.type, classs))
            g.add((object, RDF.type, OWL.NamedIndividual))

        # url1 = "http://example.org/ontology/"+a
        # object = URIRef(a)
        # url2 = "http://example.org/ontology/"+b
        # classs = URIRef(b)
        # g.add((object, RDF.type, classs))

    # SUBPROPERTY
    col1 = subproperty.iloc[:, 0].values
    col2 = subproperty.iloc[:, 1].values
    for (c1, c2) in zip(col1, col2):

        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        if (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] == 'http:'):
            subprop = URIRef(a)
            object = URIRef(b)
            g.add((subprop, RDFS.subPropertyOf, object))
        elif (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] != 'http:'):
            subprop = URIRef(b)
            object = BNode(a)
            g.add((subprop, RDFS.subPropertyOf, object))
        elif (b.rsplit('/')[0] != 'http:') and (a.rsplit('/')[0] == 'http:'):
            subprop = URIRef(a)
            object = BNode(b)
            g.add((subprop, RDFS.subPropertyOf, object))
        else:
            subprop = BNode(a)
            object= BNode(b)
            g.add((subprop, RDFS.subPropertyOf, object))

        # uri1 = "http://example.org/ontology/"+a
        # subprop = URIRef(a)
        # uri2 = "http://example.org/ontology/"+b
        # object = URIRef(b)
        # g.add((subprop, RDFS.subPropertyOf, object))

    # INVERSE
    col1 = inverse.iloc[:, 0].values
    col2 = inverse.iloc[:, 1].values
    for (c1, c2) in zip(col1, col2):
        
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        if (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] == 'http:'):
            subprop = URIRef(a)
            object = URIRef(b)
            g.add((subprop, OWL.inverseOf, object))
        elif (b.rsplit('/')[0] == 'http:') and (a.rsplit('/')[0] != 'http:'):
            subprop = URIRef(b)
            object = BNode(a)
            g.add((subprop, OWL.inverseOf, object))
        elif (b.rsplit('/')[0] != 'http:') and (a.rsplit('/')[0] == 'http:'):
            subprop = URIRef(a)
            object = BNode(b)
            g.add((subprop, OWL.inverseOf, object))
        else:
            subprop = BNode(a)
            object= BNode(b)
            g.add((subprop, OWL.inverseOf, object))


        # uri1 = "http://example.org/ontology/"+a
        # subprop = URIRef(a)
        # uri2 = "http://example.org/ontology/"+b
        # object = URIRef(b)
        # g.add((subprop, OWL.inverseOf, object))

    # # OnProperty
    # col1 = onproperty.iloc[:, 0].values
    # col2 = onproperty.iloc[:, 1].values
    # for (a, b) in zip(col1, col2):
    #     if (a.rsplit('/')[0] == 'http:'):
    #         classs = URIRef(a)
    #         property = URIRef(b)
    #         g.add((classs, OWL.onProperty, property))
    #     else:
    #         print(a)
    #         nodeid = BNode(a)
    #         property = URIRef(b)
    #         g.add((nodeid, OWL.onProperty, property))

    # someValuesFrom
    col1 = somevaluesfrom.iloc[:, 0].values
    col2 = somevaluesfrom.iloc[:, 1].values
    col3 = somevaluesfrom.iloc[:, 2].values
    for (c1, c2, c3) in zip(col1, col2, col3):
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        s=c3.split(':')
        if len(s)==1:
            c=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            c=s[1]
        else:
            pre=s[0]
            thing=s[1]
            c=iri_dict[pre]+thing

        if (a.rsplit('/')[0] == 'http:') and (c.split('/')[0]=='http:'):
            classs = URIRef(a)
            onproperty = URIRef(b)
            somevaluesfrom=URIRef(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.someValuesFrom, somevaluesfrom))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]=='http:'):
            classs=BNode(a)
            onproperty = URIRef(b)
            somevaluesfrom=URIRef(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.someValuesFrom, somevaluesfrom))
        elif (a.split('/')[0]=='http:') and (c.split('/')[0]!='http'):
            classs=URIRef(a)
            onproperty=URIRef(b)
            somevaluesfrom= BNode(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.someValuesFrom, somevaluesfrom))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]!='http'):
            classs=BNode(a)
            onproperty=URIRef(b)
            somevaluesfrom=BNode(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.someValuesFrom, somevaluesfrom))

    
    #allvaluesfrom
    col1 = allvaluesfrom.iloc[:, 0].values
    col2 = allvaluesfrom.iloc[:, 1].values
    col3 = allvaluesfrom.iloc[:, 2].values
    for (c1, c2, c3) in zip(col1, col2, col3):
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        s=c3.split(':')
        if len(s)==1:
            c=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            c=s[1]
        else:
            pre=s[0]
            thing=s[1]
            c=iri_dict[pre]+thing
            

        if (a.rsplit('/')[0] == 'http:') and (c.split('/')[0]=='http:'):
            classs = URIRef(a)
            onproperty = URIRef(b)
            allvaluesfrom=URIRef(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.allValuesFrom, allvaluesfrom))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]=='http:'):
            classs=BNode(a)
            onproperty = URIRef(b)
            allvaluesfrom=URIRef(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.allValuesFrom, allvaluesfrom))
        elif (a.split('/')[0]=='http:') and (c.split('/')[0]!='http'):
            classs=URIRef(a)
            onproperty=URIRef(b)
            allvaluesfrom= BNode(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.allValuesFrom, allvaluesfrom))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]!='http'):
            classs=BNode(a)
            onproperty=URIRef(b)
            allvaluesfrom=BNode(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.allValuesFrom, allvaluesfrom))
    
    #maxcardinality
    col1 = maxcardinality.iloc[:, 0].values
    col2 = maxcardinality.iloc[:, 1].values
    col3 = maxcardinality.iloc[:, 2].values
    for (c1, c2, c3) in zip(col1, col2, col3):
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        s=c3.split(':')
        if len(s)==1:
            c=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            c=s[1]
        else:
            pre=s[0]
            thing=s[1]
            c=iri_dict[pre]+thing
            

        if (a.rsplit('/')[0] == 'http:') and (c.split('/')[0]=='http:'):
            classs = URIRef(a)
            onproperty = URIRef(b)
            maxcardinality=URIRef(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.maxCardinality, maxcardinality))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]=='http:'):
            classs=BNode(a)
            onproperty = URIRef(b)
            maxcardinality=URIRef(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.maxCardinality, maxcardinality))
        elif (a.split('/')[0]=='http:') and (c.split('/')[0]!='http'):
            classs=URIRef(a)
            onproperty=URIRef(b)
            maxcardinality= BNode(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.maxCardinality, maxcardinality))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]!='http'):
            classs=BNode(a)
            onproperty=URIRef(b)
            maxcardinality=BNode(c)
            g.add((classs, OWL.onProperty, onproperty))
            g.add((classs, OWL.maxCardinality, maxCardinality))



    #firstrest
    col1 = firstrest.iloc[:, 0].values
    col2 = firstrest.iloc[:, 1].values
    col3 = firstrest.iloc[:, 2].values
    for (c1, c2, c3) in zip(col1, col2, col3):
        s=c1.split(':')
        if len(s)==1:
            a=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            a=s[1]
        else:
            pre=s[0]
            thing=s[1]
            a=iri_dict[pre]+thing

        s=c2.split(':')
        if len(s)==1:
            b=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            b=s[1]
        else:
            pre=s[0]
            thing=s[1]
            b=iri_dict[pre]+thing

        s=c3.split(':')
        if len(s)==1:
            c=iri_dict['ns1']+s[0]
        elif s[0]=='_':
            c=s[1]
        else:
            pre=s[0]
            thing=s[1]
            c=iri_dict[pre]+thing
            
        if (a.rsplit('/')[0] == 'http:') and (c.split('/')[0]=='http:'):
            classs = URIRef(a)
            first = URIRef(b)
            rest=URIRef(c)
            g.add((classs, RDF.first, first))
            g.add((classs, RDF.rest, rest))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]=='http:'):
            classs=BNode(a)
            first = URIRef(b)
            rest=URIRef(c)
            g.add((classs, RDF.first, first))
            g.add((classs, RDF.rest, rest))
        elif (a.split('/')[0]=='http:') and (c.split('/')[0]!='http'):
            classs=URIRef(a)
            first=URIRef(b)
            rest= BNode(c)
            g.add((classs, RDF.first, first))
            g.add((classs, RDF.rest, rest))
        elif (a.split('/')[0]!='http:') and (c.split('/')[0]!='http'):
            classs=BNode(a)
            first=URIRef(b)
            rest=BNode(c)
            g.add((classs, RDF.first, first))
            g.add((classs, RDF.rest, rest))

    g.serialize(destination='output.owl', format='xml', xmlns=iri_dict['ns1'],xml_base=iri_dict['ns1'], )


def main(file):
    g = Graph()
    owlclass = pd.read_excel(file, sheet_name='owlclass')
    subclass = pd.read_excel(file, sheet_name='subclass')
    domain_axiom = pd.read_excel(file, sheet_name='domain')
    range_axiom = pd.read_excel(file, sheet_name='range')
    instances = pd.read_excel(file, sheet_name='instances')
    subproperty = pd.read_excel(file, sheet_name='subproperty')
    inverse = pd.read_excel(file, sheet_name='inverseOf')
    # onproperty = pd.read_excel(file, sheet_name='onproperty')
    somevaluesfrom = pd.read_excel(file, sheet_name='somevaluesfrom')
    allvaluesfrom = pd.read_excel(file, sheet_name='allvaluesfrom')
    maxcardinality = pd.read_excel(file, sheet_name='maxcardinality')
    firstrest = pd.read_excel(file, sheet_name='firstrest')

    
    iri=pd.read_excel(file, sheet_name='prefixiri')
    if iri.empty:
        print('There is no default namespace for the ontology\n The default namespace for the ontology is taken as : http://www.semanticweb.org/rohitbhatia/ontologies/2023/3/ontology#')
        namespace='http://www.semanticweb.org/rohitbhatia/ontologies/2023/3/ontology#'
        row={'Prefix': 'ns1', 'Namespace': namespace}
        iri=iri.append(row, ignore_index=True)
    
    c1=iri.iloc[:,0].values
    print(c1)
    c2=iri.iloc[:,1].values
    print(c2)
    global iri_dict
    iri_dict={}
    for (a,b) in zip(c1,c2):
        iri_dict[a]=b

    print(iri_dict['ns1'])

    csv_owl_final(subclass, domain_axiom, range_axiom, instances,
                  subproperty, inverse, allvaluesfrom, somevaluesfrom,maxcardinality, owlclass,firstrest, g)
