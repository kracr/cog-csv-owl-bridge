#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def csv_owl_final(g):
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
    
    
    g.serialize(destination='output.owl', format='pretty-xml')

