import logging
import numpy as np
import pandas as pd
import re
from base64 import encode
from token import ENCODING
import csv
import rdflib
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib import BNode
from rdflib.namespace import split_uri
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD
import pprint
import os


def custom_split_uri(uri):
    """Custom URI splitting that handles various URI formats"""
    uri = str(uri)
    if '#' in uri:
        return uri.split('#', 1)
    if '/' in uri:
        return uri.rsplit('/', 1)
    return uri, ''

def owl_csv_subclass(g, uri, output_file="subclass.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Subclass", "Restriction (onProperty)", "Restriction (quantifier)", "Superclass"])
        results_found = False

        for class_uri, _, parent in g.triples((None, RDFS.subClassOf, None)):
            if isinstance(class_uri, BNode):
                continue

            if isinstance(class_uri, URIRef):
                ns, local = custom_split_uri(str(class_uri))
                prefix = uri.get(ns, f"ns{len(uri)}")
                uri[ns] = prefix
                subclass_name = f"{prefix}:{local}"
            else:
                continue

            if isinstance(parent, BNode):
                on_property = None
                quantifier = None
                superclass = None

                for p, q, r in g.triples((parent, None, None)):
                    if q == OWL.onProperty and isinstance(r, URIRef):
                        ns, local = custom_split_uri(str(r))
                        prefix = uri.get(ns, f"ns{len(uri)}")
                        uri[ns] = prefix
                        on_property = f"{prefix}:{local}"
                    elif q in (OWL.someValuesFrom, OWL.allValuesFrom) and isinstance(r, URIRef):
                        ns, local = custom_split_uri(str(r))
                        prefix = uri.get(ns, f"ns{len(uri)}")
                        uri[ns] = prefix
                        superclass = f"{prefix}:{local}"
                        quantifier = "some" if q == OWL.someValuesFrom else "all"

                if on_property and quantifier and superclass:
                    writer.writerow([subclass_name, on_property, quantifier, superclass])
                    results_found = True
                continue

            elif isinstance(parent, URIRef):
                ns, local = custom_split_uri(str(parent))
                prefix = uri.get(ns, f"ns{len(uri)}")
                uri[ns] = prefix
                if prefix == 'ns1' and local == 'Class':
                    continue
                parent_name = f"{prefix}:{local}"
                writer.writerow([subclass_name, "", "", parent_name])
                results_found = True

        return output_file if results_found else None

def owl_csv_class(g, uri):
    fields = ['OWL Class']
    with open('owlclass.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for subject, predicate, obj in g:
            if predicate == RDF.type and obj == OWL.Class:
                if not isinstance(subject, BNode):
                    ns, local = custom_split_uri(str(subject))
                    prefix = uri.get(ns, f"ns{len(uri)}")
                    uri[ns] = prefix
                    writer.writerow([f"{prefix}:{local}"])
    return 'owlclass.csv'


def owl_csv_domain(g, uri):
    global count
    fields = ['Object', 'Domain']
    f = open('domain.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:

        if predicate == rdflib.RDFS.domain:
            object_prop = (str)(subject).rsplit('/')[-1]
            if (subject.rsplit('/')[0] == 'http:'):
                name = URIRef(subject)
                namespace, local_name = split_uri(str(name))
                # a=local_name
                if namespace in uri:
                    a = uri[namespace]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace] = prefix
                    a = uri[namespace]+":"+local_name
            else:
                a = '_:'+subject

            domain = (str)(obj).rsplit('/')[-1]
            if (obj.rsplit('/')[0] == 'http:'):
                name = URIRef(obj)
                namespace, local_name = split_uri(str(name))
                # b=local_name
                if namespace in uri:
                    b = uri[namespace]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace] = prefix
                    b = uri[namespace]+":"+local_name
            else:
                b = '_:'+obj

            rows = [a, b]
            writer.writerow(rows)

    f.close()
    return 'domain.csv'


def owl_csv_range(g, uri):
    global count
    fields = ['Object', 'Range']
    f = open('range.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:

        if predicate == rdflib.RDFS.range:
            object_prop = (str)(subject).rsplit('/')[-1]
            if (subject.rsplit('/')[0] == 'http:'):
                name = URIRef(subject)
                namespace, local_name = split_uri(str(name))
                # a=local_name
                if namespace in uri:
                    a = uri[namespace]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace] = prefix
                    a = uri[namespace]+":"+local_name
            else:
                a = '_:'+subject

            range = (str)(obj).rsplit('/')[-1]
            if (obj.rsplit('/')[0] == 'http:'):
                name = URIRef(obj)
                namespace, local_name = split_uri(str(name))
                # b=local_name
                if namespace in uri:
                    b = uri[namespace]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace] = prefix
                    b = uri[namespace]+":"+local_name
            else:
                b = '_:'+obj

            rows = [a, b]
            writer.writerow(rows)

    f.close()
    return 'range.csv'


def owl_csv_instances(g, uri):
    global count
    prop = []
    fields = ['Instances', 'Class']
    f = open('instances.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)

    for s, p, o in g:
        if p == rdflib.RDF.type and o == rdflib.OWL.NamedIndividual:
            for subject, predicate, obj in g:
                if str(subject) == str(s) and str(p) == str(predicate) and obj != rdflib.OWL.NamedIndividual:

                    subj = (str)(subject).rsplit('/')[-1]
                    if (subject.rsplit('/')[0] == 'http:'):
                        name = URIRef(subject)
                        namespace, local_name = split_uri(str(name))
                        # a=local_name
                        if namespace in uri:
                            a = uri[namespace]+":" + local_name
                        else:
                            prefix = 'ns'+str(count)
                            count += 1
                            uri[namespace] = prefix
                            a = uri[namespace]+":"+local_name
                    else:
                        a = '_:'+subject

                    objj = (str)(obj).rsplit('/')[-1]
                    if (obj.rsplit('/')[0] == 'http:'):
                        name = URIRef(obj)
                        namespace, local_name = split_uri(str(name))
                        # b=local_name
                        if namespace in uri:
                            b = uri[namespace]+":" + local_name
                        else:
                            prefix = 'ns'+str(count)
                            count += 1
                            uri[namespace] = prefix
                            b = uri[namespace]+":"+local_name
                    else:
                        b = '_:'+obj

                    rows = [a, b]
                    writer.writerow(rows)
    f.close()
    return 'instances.csv'

def owl_csv_subproperty(g, uri):
    global count
    fields = ['subproperty', 'role1', 'role2', 'superproperty']
    f = open('subproperty.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)

    for subject, predicate, obj in g:
        if predicate == rdflib.RDFS.subPropertyOf:
            if isinstance(subject, URIRef):
                ns1, local1 = split_uri(str(subject))
                subproperty = f"{uri.get(ns1, 'ns0')}:{local1}"
            else:
                subproperty = f"_:{subject}"

            role1 = ""
            role2 = ""

            if isinstance(obj, BNode):
                for s, p, o in g.triples((obj, None, None)):
                    if p == OWL.propertyChainAxiom:
                        chain_items = list(g.items(o))
                        if len(chain_items) == 2:
                            role1_uri = chain_items[0]
                            role2_uri = chain_items[1]

                            if isinstance(role1_uri, URIRef):
                                ns_r1, local_r1 = split_uri(str(role1_uri))
                                role1 = f"{uri.get(ns_r1, 'ns0')}:{local_r1}"

                            if isinstance(role2_uri, URIRef):
                                ns_r2, local_r2 = split_uri(str(role2_uri))
                                role2 = f"{uri.get(ns_r2, 'ns0')}:{local_r2}"

                        for s2, p2, o2 in g.triples((obj, RDF.type, None)):
                            if isinstance(o2, URIRef):
                                ns2, local2 = split_uri(str(s))
                                superproperty = f"{uri.get(ns2, 'ns0')}:{local2}"
                                writer.writerow([subproperty, role1, role2, superproperty])
                continue  # Skip rest of loop

            if isinstance(obj, URIRef):
                ns2, local2 = split_uri(str(obj))
                superproperty = f"{uri.get(ns2, 'ns0')}:{local2}"
            else:
                superproperty = f"_:{obj}"

            writer.writerow([subproperty, role1, role2, superproperty])

    f.close()
    return 'subproperty.csv'


def owl_csv_inverseof(g, uri):
    global count
    fields = ['inverseOf', 'Object']
    seen_pairs = set()  # Track seen inverse pairs
    
    with open('inverseOf.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        
        for subject, predicate, obj in g:
            if predicate == rdflib.OWL.inverseOf:
                # Sort URIs to treat A-B and B-A as same pair
                pair = tuple(sorted([str(subject), str(obj)]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    
                    # Process subject
                    if (str(subject).startswith('http:')):
                        name = URIRef(subject)
                        namespace, local_name = split_uri(str(name))
                        if namespace in uri:
                            a = f"{uri[namespace]}:{local_name}"
                        else:
                            prefix = f"ns{count}"
                            count += 1
                            uri[namespace] = prefix
                            a = f"{prefix}:{local_name}"
                    else:
                        a = f"_:{subject}"
                    
                    # Process object
                    if (str(obj).startswith('http:')):
                        name = URIRef(obj)
                        namespace, local_name = split_uri(str(name))
                        if namespace in uri:
                            b = f"{uri[namespace]}:{local_name}"
                        else:
                            prefix = f"ns{count}"
                            count += 1
                            uri[namespace] = prefix
                            b = f"{prefix}:{local_name}"
                    else:
                        b = f"_:{obj}"
                    
                    writer.writerow([a, b])
    
    return 'inverseOf.csv'

def owl_csv_maxcardinality(g, onproperty_dict, uri):
    global count
    maxcardinality_dict = {}
    fields = ['Class', 'Property']
    f2 = open('maxcardinality1.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.maxCardinality:
            rows = [subject, obj]
            maxcardinality_dict[subject] = obj
            writer.writerow(rows)

    f2.close()

    f3 = open('maxcardinality_temp.csv', 'w')
    writer1 = csv.writer(f3, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'maxCardinality']
    writer1.writerow(fields)

    for i in maxcardinality_dict:
        if i in onproperty_dict:
            rows = [i, onproperty_dict[i], maxcardinality_dict[i]]
            writer1.writerow(rows)
    f3.close()

    temp = pd.read_csv('maxcardinality_temp.csv')
    classs = temp.iloc[:, 0].values
    onproperty = temp.iloc[:, 1].values
    maxcardinality = temp.iloc[:, 2].values

    f4 = open('maxcardinality.csv', 'w')
    writer4 = csv.writer(f4, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'maxCardinality']
    writer4.writerow(fields)

    for (subject, predicate, obj) in zip(classs, onproperty, maxcardinality):
        if (str(subject).rsplit('/')[0] == 'http:'):
            name = URIRef(subject)
            namespace, local_name = split_uri(str(name))
            if namespace in uri:
                a1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                a1 = uri[namespace]+":"+local_name
        else:
            a1 = '_:'+ str(subject)

        if (str(predicate).rsplit('/')[0] == 'http:'):
            name = URIRef(predicate)
            namespace, local_name = split_uri(str(name))
            if namespace in uri:
                b1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                b1 = uri[namespace]+":"+local_name
        else:
            b1 = '_:'+ str(predicate)

        if isinstance(obj, (int, float, np.integer)):  # Numeric cardinality
            c1 = str(obj)
        elif str(obj).startswith('http:'):  # URI
            name = URIRef(obj)
            namespace, local_name = split_uri(str(name))
            if namespace in uri:
                c1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                c1 = uri[namespace]+":"+local_name
        else:
            c1 = '_:'+ str(obj)

        rows = [a1, b1, c1]
        writer4.writerow(rows)

    f4.close()
    return 'maxcardinality.csv'

def not_processing(g, uri):
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    for subject, predicate, obj in g:
        if not ((predicate==RDFS.subClassOf) or (predicate == rdflib.RDF.type and obj == rdflib.OWL.Class) or (predicate == rdflib.RDFS.domain) or (predicate == rdflib.RDFS.range) or (predicate == rdflib.RDF.type and obj == rdflib.OWL.NamedIndividual) or (predicate == rdflib.RDFS.subPropertyOf) or (predicate == rdflib.OWL.inverseOf) or (predicate == rdflib.OWL.onProperty) or (predicate == rdflib.RDF.rest) or (predicate == rdflib.RDF.first)):
            logging.error(subject)
            logging.error(predicate)
            logging.error(obj+'\n')
def func():
    return 'prefixiri.csv'

def main(file, output_filename):
    g = Graph()
    g.parse(file)  # Use correct format if needed

    global count
    count = 1
    uri = {}
    onproperty_dict = {}
    unique_properties = set()

    for s, p, o in g:
        for node in [s, p, o]:
            if isinstance(node, URIRef):
                try:
                    ns, _ = custom_split_uri(str(node))
                    if ns not in uri:
                        uri[ns] = f"ns{count}"
                        count += 1
                except Exception as e:
                    print(f"Error processing URI {node}: {e}")
                    continue

        if (p == RDF.type and o == OWL.ObjectProperty) or \
           (p == RDF.type and o == RDF.Property) or \
           (p == RDFS.domain and isinstance(s, URIRef)) or \
           (p == RDFS.range and isinstance(s, URIRef)):
            if isinstance(s, URIRef):
                ns, local = custom_split_uri(str(s))
                prop_name = f"{uri.get(ns, 'ns0')}:{local}"
                unique_properties.add(prop_name)

    with open('onproperty.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ObjectProperty'])
        for prop in sorted(unique_properties):
            writer.writerow([prop])

    f9 = owl_csv_class(g, uri)
    f1 = owl_csv_domain(g, uri)
    f2 = owl_csv_subclass(g, uri)
    f3 = owl_csv_range(g, uri)
    f4 = owl_csv_instances(g, uri)
    f5 = owl_csv_subproperty(g, uri)
    f6 = owl_csv_inverseof(g, uri)
    f11 = owl_csv_maxcardinality(g, onproperty_dict, uri)

    with open('prefixiri.csv', 'w', newline='', encoding='utf-8') as furi:
        writer = csv.writer(furi)
        writer.writerow(['Prefix', 'Namespace'])
        for namespace, prefix in uri.items():
            writer.writerow([prefix, namespace])

    name = output_filename + '.xlsx'

    generated_files = [f9, f1, f2, f3, f4, f5, f6, f11, 'prefixiri.csv', 'onproperty.csv']
    valid_files = [f for f in generated_files if f is not None]

    with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
        for filename in valid_files:
            try:
                df = pd.read_csv(filename)
                sheet_name = os.path.splitext(os.path.basename(filename))[0]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    print('The default namespace for the ontology is ' + str(uri.get('ns1')))
    not_processing(g, uri)