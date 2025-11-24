# import logging
# import numpy as np
# import pandas as pd
# import re
# from base64 import encode
# from token import ENCODING
# import csv
# import rdflib
# from rdflib import Graph, Literal, RDF, URIRef
# from rdflib.namespace import FOAF, XSD
# from rdflib import BNode
# from rdflib.namespace import split_uri
# from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
#     PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
#     VOID, XMLNS, XSD
# import pprint
# import os
# from owlready2 import get_ontology


# def custom_split_uri(uri):
#     """Custom URI splitting that handles various URI formats"""
#     uri = str(uri)
#     if '#' in uri:
#         return uri.split('#', 1)
#     if '/' in uri:
#         return uri.rsplit('/', 1)
#     return uri, ''

# from rdflib.collection import Collection

# def owl_csv_subclass(g, uri, output_file="subclass.csv"):
#     with open(output_file, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(["Subclass", "Restriction (onProperty)", "Restriction (quantifier)", "Superclass"])
#         results_found = False

#         for subclass, _, superclass in g.triples((None, RDFS.subClassOf, None)):

#             # --- Subclass formatting ---
#             if isinstance(subclass, URIRef):
#                 ns, local = custom_split_uri(str(subclass))
#                 prefix = uri.get(ns, f"ns{len(uri)}")
#                 uri[ns] = prefix
#                 subclass_str = f"{prefix}:{local}"
#             elif isinstance(subclass, BNode):
#                 if (subclass, OWL.intersectionOf, None) in g:
#                     collection = Collection(g, g.value(subclass, OWL.intersectionOf))
#                     subclass_parts = []
#                     for item in collection:
#                         if isinstance(item, URIRef):
#                             ns, local = custom_split_uri(str(item))
#                             prefix = uri.get(ns, f"ns{len(uri)}")
#                             uri[ns] = prefix
#                             subclass_parts.append(f"{prefix}:{local}")
#                     subclass_str = " & ".join(subclass_parts)
#                 elif (subclass, RDF.type, OWL.Restriction) in g:
#                     on_property = g.value(subclass, OWL.onProperty)
#                     for qtype in (OWL.someValuesFrom, OWL.allValuesFrom):
#                         val = g.value(subclass, qtype)
#                         if val:
#                             quant = "some" if qtype == OWL.someValuesFrom else "all"
#                             ns_p, local_p = custom_split_uri(str(on_property))
#                             prefix_p = uri.get(ns_p, f"ns{len(uri)}")
#                             uri[ns_p] = prefix_p
#                             prop_str = f"{prefix_p}:{local_p}"

#                             ns_c, local_c = custom_split_uri(str(val))
#                             prefix_c = uri.get(ns_c, f"ns{len(uri)}")
#                             uri[ns_c] = prefix_c
#                             class_str = f"{prefix_c}:{local_c}"

#                             writer.writerow(["", prop_str, quant, class_str])
#                             results_found = True
#                     continue
#                 else:
#                     continue  # Unhandled bnode subclass
#             else:
#                 continue  # Skip unknown subclass type

#             # --- Superclass formatting ---
#             if isinstance(superclass, URIRef):
#                 ns, local = custom_split_uri(str(superclass))
#                 prefix = uri.get(ns, f"ns{len(uri)}")
#                 uri[ns] = prefix
#                 superclass_str = f"{prefix}:{local}"
#                 writer.writerow([subclass_str, "", "", superclass_str])
#                 results_found = True

#             elif isinstance(superclass, BNode):
#                 if (superclass, RDF.type, OWL.Restriction) in g:
#                     on_property = g.value(superclass, OWL.onProperty)
#                     for qtype in (OWL.someValuesFrom, OWL.allValuesFrom):
#                         val = g.value(superclass, qtype)
#                         if val:
#                             quant = "some" if qtype == OWL.someValuesFrom else "all"
#                             ns_p, local_p = custom_split_uri(str(on_property))
#                             prefix_p = uri.get(ns_p, f"ns{len(uri)}")
#                             uri[ns_p] = prefix_p
#                             prop_str = f"{prefix_p}:{local_p}"

#                             ns_c, local_c = custom_split_uri(str(val))
#                             prefix_c = uri.get(ns_c, f"ns{len(uri)}")
#                             uri[ns_c] = prefix_c
#                             class_str = f"{prefix_c}:{local_c}"

#                             writer.writerow([subclass_str, prop_str, quant, class_str])
#                             results_found = True
#                     continue

#                 elif (superclass, OWL.intersectionOf, None) in g:
#                     collection = Collection(g, g.value(superclass, OWL.intersectionOf))
#                     parts = []
#                     for item in collection:
#                         if isinstance(item, URIRef):
#                             ns, local = custom_split_uri(str(item))
#                             prefix = uri.get(ns, f"ns{len(uri)}")
#                             uri[ns] = prefix
#                             parts.append(f"{prefix}:{local}")
#                     superclass_str = " & ".join(parts)
#                     writer.writerow([subclass_str, "", "", superclass_str])
#                     results_found = True

#         return output_file if results_found else None

# def owl_csv_class(g, uri):
#     fields = ['OWL Class']
#     with open('owlclass.csv', 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(fields)
#         for subject, predicate, obj in g:
#             if predicate == RDF.type and obj == OWL.Class:
#                 if not isinstance(subject, BNode):
#                     ns, local = custom_split_uri(str(subject))
#                     prefix = uri.get(ns, f"ns{len(uri)}")
#                     uri[ns] = prefix
#                     writer.writerow([f"{prefix}:{local}"])
#     return 'owlclass.csv'


# def owl_csv_domain(g, uri):
#     global count
#     fields = ['Object', 'Domain']
#     f = open('domain.csv', 'w')
#     writer = csv.writer(f, lineterminator='\n')
#     writer.writerow(fields)
#     for subject, predicate, obj in g:

#         if predicate == rdflib.RDFS.domain:
#             object_prop = (str)(subject).rsplit('/')[-1]
#             if (subject.rsplit('/')[0] == 'http:'):
#                 name = URIRef(subject)
#                 namespace, local_name = split_uri(str(name))
#                 # a=local_name
#                 if namespace in uri:
#                     a = uri[namespace]+":" + local_name
#                 else:
#                     prefix = 'ns'+str(count)
#                     count += 1
#                     uri[namespace] = prefix
#                     a = uri[namespace]+":"+local_name
#             else:
#                 a = '_:'+subject

#             domain = (str)(obj).rsplit('/')[-1]
#             if (obj.rsplit('/')[0] == 'http:'):
#                 name = URIRef(obj)
#                 namespace, local_name = split_uri(str(name))
#                 # b=local_name
#                 if namespace in uri:
#                     b = uri[namespace]+":" + local_name
#                 else:
#                     prefix = 'ns'+str(count)
#                     count += 1
#                     uri[namespace] = prefix
#                     b = uri[namespace]+":"+local_name
#             else:
#                 b = '_:'+obj

#             rows = [a, b]
#             writer.writerow(rows)

#     f.close()
#     return 'domain.csv'


# def owl_csv_range(g, uri):
#     global count
#     fields = ['Object', 'Range']
#     f = open('range.csv', 'w')
#     writer = csv.writer(f, lineterminator='\n')
#     writer.writerow(fields)
#     for subject, predicate, obj in g:

#         if predicate == rdflib.RDFS.range:
#             object_prop = (str)(subject).rsplit('/')[-1]
#             if (subject.rsplit('/')[0] == 'http:'):
#                 name = URIRef(subject)
#                 namespace, local_name = split_uri(str(name))
#                 # a=local_name
#                 if namespace in uri:
#                     a = uri[namespace]+":" + local_name
#                 else:
#                     prefix = 'ns'+str(count)
#                     count += 1
#                     uri[namespace] = prefix
#                     a = uri[namespace]+":"+local_name
#             else:
#                 a = '_:'+subject

#             range = (str)(obj).rsplit('/')[-1]
#             if (obj.rsplit('/')[0] == 'http:'):
#                 name = URIRef(obj)
#                 namespace, local_name = split_uri(str(name))
#                 # b=local_name
#                 if namespace in uri:
#                     b = uri[namespace]+":" + local_name
#                 else:
#                     prefix = 'ns'+str(count)
#                     count += 1
#                     uri[namespace] = prefix
#                     b = uri[namespace]+":"+local_name
#             else:
#                 b = '_:'+obj

#             rows = [a, b]
#             writer.writerow(rows)

#     f.close()
#     return 'range.csv'


# def owl_csv_instances(g, uri):
#     global count
#     prop = []
#     fields = ['Instances', 'Class']
#     f = open('instances.csv', 'w')
#     writer = csv.writer(f, lineterminator='\n')
#     writer.writerow(fields)

#     for s, p, o in g:
#         if p == rdflib.RDF.type and o == rdflib.OWL.NamedIndividual:
#             for subject, predicate, obj in g:
#                 if str(subject) == str(s) and str(p) == str(predicate) and obj != rdflib.OWL.NamedIndividual:

#                     subj = (str)(subject).rsplit('/')[-1]
#                     if (subject.rsplit('/')[0] == 'http:'):
#                         name = URIRef(subject)
#                         namespace, local_name = split_uri(str(name))
#                         # a=local_name
#                         if namespace in uri:
#                             a = uri[namespace]+":" + local_name
#                         else:
#                             prefix = 'ns'+str(count)
#                             count += 1
#                             uri[namespace] = prefix
#                             a = uri[namespace]+":"+local_name
#                     else:
#                         a = '_:'+subject

#                     objj = (str)(obj).rsplit('/')[-1]
#                     if (obj.rsplit('/')[0] == 'http:'):
#                         name = URIRef(obj)
#                         namespace, local_name = split_uri(str(name))
#                         # b=local_name
#                         if namespace in uri:
#                             b = uri[namespace]+":" + local_name
#                         else:
#                             prefix = 'ns'+str(count)
#                             count += 1
#                             uri[namespace] = prefix
#                             b = uri[namespace]+":"+local_name
#                     else:
#                         b = '_:'+obj

#                     rows = [a, b]
#                     writer.writerow(rows)
#     f.close()
#     return 'instances.csv'

# def owl_csv_subproperty(g, uri, output_file='subproperty.csv'):
#     """
#     Extracts subProperty and property-chain axioms from an rdflib.Graph `g`.
#     - Writes rows: subproperty, role1, role2, superproperty
#     - Direct subPropertyOf: fills subproperty and superproperty
#     - Property chains (owl:propertyChainAxiom on superproperty): fills role1/role2 and superproperty
#       (for chains >2 the additional roles are joined using ' o ' in role1)
#     """
#     global count
#     from rdflib import URIRef
#     from rdflib.collection import Collection

#     fields = ['subproperty', 'role1', 'role2', 'superproperty']
#     with open(output_file, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(fields)

#         # --- 1) Direct subPropertyOf ---
#         for subj, pred, obj in g.triples((None, RDFS.subPropertyOf, None)):
#             if isinstance(obj, URIRef) and str(obj) != str(OWL.ObjectProperty):
#                 sub_name = f"_:{subj}"
#                 super_name = f"_:{obj}"
                
#                 if isinstance(subj, URIRef):
#                     ns1, local1 = custom_split_uri(str(subj))
#                     if ns1 not in uri:
#                         uri[ns1] = f"ns{count}"
#                         count += 1
#                     sub_name = f"{uri[ns1]}:{local1}"
                
#                 if isinstance(obj, URIRef):
#                     ns2, local2 = custom_split_uri(str(obj))
#                     if ns2 not in uri:
#                         uri[ns2] = f"ns{count}"
#                         count += 1
#                     super_name = f"{uri[ns2]}:{local2}"
                
#                 writer.writerow([sub_name, "", "", super_name])

#         # --- 2) Property chains ---
#         for superprop, _, listnode in g.triples((None, OWL.propertyChainAxiom, None)):
#             # superproperty name
#             super_name = f"_:{superprop}"
#             if isinstance(superprop, URIRef):
#                 ns_s, local_s = custom_split_uri(str(superprop))
#                 if ns_s not in uri:
#                     uri[ns_s] = f"ns{count}"
#                     count += 1
#                 super_name = f"{uri[ns_s]}:{local_s}"

#             # expand RDF list
#             try:
#                 coll = Collection(g, listnode)
#                 items = list(coll)
#             except Exception:
#                 continue  # skip malformed chains

#             # convert to prefixed strings
#             def elem_pref(x):
#                 if isinstance(x, URIRef):
#                     ns, local = custom_split_uri(str(x))
#                     if ns not in uri:
#                         uri[ns] = f"ns{count}"
#                         globals()['count'] += 1
#                     return f"{uri[ns]}:{local}"
#                 else:
#                     return f"_:{x}"

#             # write CSV based on chain length
#             if len(items) == 0:
#                 continue
#             elif len(items) == 1:
#                 r1 = elem_pref(items[0])
#                 writer.writerow(["chain", r1, "", super_name])
#             elif len(items) == 2:
#                 r1 = elem_pref(items[0])
#                 r2 = elem_pref(items[1])
#                 writer.writerow(["chain", r1, r2, super_name])
#             else:
#                 r1 = elem_pref(items[0])
#                 r2 = elem_pref(items[1])
#                 remaining = " o ".join(elem_pref(x) for x in items[2:])
#                 # include remaining in role1 along with r1 for clarity
#                 r1_full = f"{r1} o {remaining}" if remaining else r1
#                 writer.writerow(["chain", r1_full, r2, super_name])

#     return output_file

# '''
# def owl_csv_subproperty(g, uri):
#     global count
#     fields = ['subproperty', 'role1', 'role2', 'superproperty']
#     f = open('subproperty.csv', 'w')
#     writer = csv.writer(f, lineterminator='\n')
#     writer.writerow(fields)

#     for subject, predicate, obj in g:
#         if predicate == rdflib.RDFS.subPropertyOf:
#             # Resolve subproperty
#             if isinstance(subject, URIRef):
#                 ns1, local1 = split_uri(str(subject))
#                 if ns1 not in uri:
#                     uri[ns1] = f"ns{count}"
#                     count += 1
#                 subproperty = f"{uri[ns1]}:{local1}"
#             else:
#                 subproperty = f"_:{subject}"

#             role1 = ""
#             role2 = ""

#             # Handle property chain (optional, if exists)
#             if isinstance(obj, BNode):
#                 for s, p, o in g.triples((obj, None, None)):
#                     if p == OWL.propertyChainAxiom:
#                         chain_items = list(g.items(o))
#                         if len(chain_items) == 2:
#                             role1_uri, role2_uri = chain_items
#                             if isinstance(role1_uri, URIRef):
#                                 ns_r1, local_r1 = split_uri(str(role1_uri))
#                                 if ns_r1 not in uri:
#                                     uri[ns_r1] = f"ns{count}"
#                                     count += 1
#                                 role1 = f"{uri[ns_r1]}:{local_r1}"
#                             if isinstance(role2_uri, URIRef):
#                                 ns_r2, local_r2 = split_uri(str(role2_uri))
#                                 if ns_r2 not in uri:
#                                     uri[ns_r2] = f"ns{count}"
#                                     count += 1
#                                 role2 = f"{uri[ns_r2]}:{local_r2}"

#                         for s2, p2, o2 in g.triples((obj, RDF.type, None)):
#                             if isinstance(o2, URIRef):
#                                 ns2, local2 = split_uri(str(s))
#                                 if ns2 not in uri:
#                                     uri[ns2] = f"ns{count}"
#                                     count += 1
#                                 superproperty = f"{uri[ns2]}:{local2}"
#                                 writer.writerow([subproperty, role1, role2, superproperty])
#                 continue  # Done with bnode case

#             # Resolve superproperty
#             if isinstance(obj, URIRef):
#                 ns2, local2 = split_uri(str(obj))
#                 if ns2 not in uri:
#                     uri[ns2] = f"ns{count}"
#                     count += 1
#                 superproperty = f"{uri[ns2]}:{local2}"
#             else:
#                 superproperty = f"_:{obj}"

#             writer.writerow([subproperty, role1, role2, superproperty])

#     f.close()
#     return 'subproperty.csv'
# '''

# def export_subproperties(owl_file, csv_file):
#     # Load ontology
#     onto = get_ontology(owl_file).load()

#     with open(csv_file, "w", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f)
#         writer.writerow(["type", "role1", "role2", "superproperty"])

#         # 1. Direct subproperty axioms
#         for prop in onto.object_properties():
#             for superprop in prop.is_a:
#                 # Filter out trivial "is-a owl:ObjectProperty"
#                 if hasattr(superprop, "iri") and superprop.iri != "http://www.w3.org/2002/07/owl#ObjectProperty":
#                     writer.writerow(["subproperty", prop.iri, "", superprop.iri])

#         # 2. Property chain axioms
#         for prop in onto.object_properties():
#             if hasattr(prop, "subpropertychains") and prop.subpropertychains:
#                 for chain in prop.subpropertychains:
#                     if len(chain) == 2:
#                         # Binary chain
#                         writer.writerow(["chain", chain[0].iri, chain[1].iri, prop.iri])
#                     else:
#                         # Longer chains (keep as joined string)
#                         chain_str = " o ".join(p.iri for p in chain)
#                         writer.writerow([f"chain+{len(chain)}", chain_str, "", prop.iri])


# def owl_csv_inverseof(g, uri):
#     global count
#     fields = ['inverseOf', 'Object']
#     seen_pairs = set()  # Track seen inverse pairs
    
#     with open('inverseOf.csv', 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(fields)
        
#         for subject, predicate, obj in g:
#             if predicate == rdflib.OWL.inverseOf:
#                 # Sort URIs to treat A-B and B-A as same pair
#                 pair = tuple(sorted([str(subject), str(obj)]))
#                 if pair not in seen_pairs:
#                     seen_pairs.add(pair)
                    
#                     # Process subject
#                     if (str(subject).startswith('http:')):
#                         name = URIRef(subject)
#                         namespace, local_name = split_uri(str(name))
#                         if namespace in uri:
#                             a = f"{uri[namespace]}:{local_name}"
#                         else:
#                             prefix = f"ns{count}"
#                             count += 1
#                             uri[namespace] = prefix
#                             a = f"{prefix}:{local_name}"
#                     else:
#                         a = f"_:{subject}"
                    
#                     # Process object
#                     if (str(obj).startswith('http:')):
#                         name = URIRef(obj)
#                         namespace, local_name = split_uri(str(name))
#                         if namespace in uri:
#                             b = f"{uri[namespace]}:{local_name}"
#                         else:
#                             prefix = f"ns{count}"
#                             count += 1
#                             uri[namespace] = prefix
#                             b = f"{prefix}:{local_name}"
#                     else:
#                         b = f"_:{obj}"
                    
#                     writer.writerow([a, b])
    
#     return 'inverseOf.csv'

# def owl_csv_maxcardinality(g, onproperty_dict, uri):
#     global count
#     maxcardinality_dict = {}
#     fields = ['Class', 'Property']
#     f2 = open('maxcardinality1.csv', 'w')
#     writer = csv.writer(f2, lineterminator='\n')
#     writer.writerow(fields)
#     for subject, predicate, obj in g:
#         if predicate == rdflib.OWL.maxCardinality:
#             rows = [subject, obj]
#             maxcardinality_dict[subject] = obj
#             writer.writerow(rows)

#     f2.close()

#     f3 = open('maxcardinality_temp.csv', 'w')
#     writer1 = csv.writer(f3, lineterminator='\n')
#     fields = ['Class', 'OnProperty', 'maxCardinality']
#     writer1.writerow(fields)

#     for i in maxcardinality_dict:
#         if i in onproperty_dict:
#             rows = [i, onproperty_dict[i], maxcardinality_dict[i]]
#             writer1.writerow(rows)
#     f3.close()

#     temp = pd.read_csv('maxcardinality_temp.csv')
#     classs = temp.iloc[:, 0].values
#     onproperty = temp.iloc[:, 1].values
#     maxcardinality = temp.iloc[:, 2].values

#     f4 = open('maxcardinality.csv', 'w')
#     writer4 = csv.writer(f4, lineterminator='\n')
#     fields = ['Class', 'OnProperty', 'maxCardinality']
#     writer4.writerow(fields)

#     for (subject, predicate, obj) in zip(classs, onproperty, maxcardinality):
#         if (str(subject).rsplit('/')[0] == 'http:'):
#             name = URIRef(subject)
#             namespace, local_name = split_uri(str(name))
#             if namespace in uri:
#                 a1 = uri[namespace]+":" + local_name
#             else:
#                 prefix = 'ns'+str(count)
#                 count += 1
#                 uri[namespace] = prefix
#                 a1 = uri[namespace]+":"+local_name
#         else:
#             a1 = '_:'+ str(subject)

#         if (str(predicate).rsplit('/')[0] == 'http:'):
#             name = URIRef(predicate)
#             namespace, local_name = split_uri(str(name))
#             if namespace in uri:
#                 b1 = uri[namespace]+":" + local_name
#             else:
#                 prefix = 'ns'+str(count)
#                 count += 1
#                 uri[namespace] = prefix
#                 b1 = uri[namespace]+":"+local_name
#         else:
#             b1 = '_:'+ str(predicate)

#         if isinstance(obj, (int, float, np.integer)):  # Numeric cardinality
#             c1 = str(obj)
#         elif str(obj).startswith('http:'):  # URI
#             name = URIRef(obj)
#             namespace, local_name = split_uri(str(name))
#             if namespace in uri:
#                 c1 = uri[namespace]+":" + local_name
#             else:
#                 prefix = 'ns'+str(count)
#                 count += 1
#                 uri[namespace] = prefix
#                 c1 = uri[namespace]+":"+local_name
#         else:
#             c1 = '_:'+ str(obj)

#         rows = [a1, b1, c1]
#         writer4.writerow(rows)

#     f4.close()
#     return 'maxcardinality.csv'

# def not_processing(g, uri):
#     logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
#     for subject, predicate, obj in g:
#         if not ((predicate==RDFS.subClassOf) or (predicate == rdflib.RDF.type and obj == rdflib.OWL.Class) or (predicate == rdflib.RDFS.domain) or (predicate == rdflib.RDFS.range) or (predicate == rdflib.RDF.type and obj == rdflib.OWL.NamedIndividual) or (predicate == rdflib.RDFS.subPropertyOf) or (predicate == rdflib.OWL.inverseOf) or (predicate == rdflib.OWL.onProperty) or (predicate == rdflib.RDF.rest) or (predicate == rdflib.RDF.first)):
#             logging.error(subject)
#             logging.error(predicate)
#             logging.error(obj+'\n')
# def func():
#     return 'prefixiri.csv'

# def main(file, output_filename):
#     g = Graph()
#     g.parse(file)  

#     global count
#     count = 1
    
#     uri = {}
#     onproperty_dict = {}
#     unique_properties = set()

#     for s, p, o in g:
#         for node in [s, p, o]:
#             if isinstance(node, URIRef):
#                 try:
#                     ns, _ = custom_split_uri(str(node))
#                     if ns not in uri:
#                         uri[ns] = f"ns{count}"
#                         count += 1
#                 except Exception as e:
#                     print(f"Error processing URI {node}: {e}")
#                     continue

#         if (p == RDF.type and o == OWL.ObjectProperty) or \
#            (p == RDF.type and o == RDF.Property) or \
#            (p == RDFS.domain and isinstance(s, URIRef)) or \
#            (p == RDFS.range and isinstance(s, URIRef)):
#             if isinstance(s, URIRef):
#                 ns, local = custom_split_uri(str(s))
#                 prop_name = f"{uri.get(ns, 'ns0')}:{local}"
#                 unique_properties.add(prop_name)

#     with open('onproperty.csv', 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(['ObjectProperty'])
#         for prop in sorted(unique_properties):
#             writer.writerow([prop])

#     f9 = owl_csv_class(g, uri)
#     f1 = owl_csv_domain(g, uri)
#     f2 = owl_csv_subclass(g, uri)
#     f3 = owl_csv_range(g, uri)
#     f4 = owl_csv_instances(g, uri)
#     f5 = owl_csv_subproperty(g, uri)
#     f6 = owl_csv_inverseof(g, uri)
#     f11 = owl_csv_maxcardinality(g, onproperty_dict, uri)
#     # f12 = owl_csv_annotation_properties(g, uri)

#     with open('prefixiri.csv', 'w', newline='', encoding='utf-8') as furi:
#         writer = csv.writer(furi)
#         writer.writerow(['Prefix', 'Namespace'])
#         for namespace, prefix in uri.items():
#             if prefix == "":
#                 writer.writerow([":", namespace])
#             else:
#                 writer.writerow([prefix, namespace])

        
#     name = output_filename + '.xlsx'
#     generated_files = [f9, f1, f2, f3, f4, f5, f6, f11, 'prefixiri.csv', 'onproperty.csv']
#     valid_files = [f for f in generated_files if f is not None]

#     with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
#         for filename in valid_files:
#             try:
#                 df = pd.read_csv(filename)
#                 sheet_name = os.path.splitext(os.path.basename(filename))[0]
#                 df.to_excel(writer, sheet_name=sheet_name, index=False)
#             except Exception as e:
#                 print(f"Error processing {filename}: {str(e)}")

#     print('The default namespace for the ontology is ' + str(uri.get('ns1')))
#     not_processing(g, uri)

# owl_csv_code.py  (updated prefix handling)
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
from owlready2 import get_ontology

# --- Helper: custom split and normalization ---
def custom_split_uri(uri):
    """Custom URI splitting that handles various URI formats.
       Returns (namespace, local) where namespace does NOT include trailing '#' or '/'."""
    uri = str(uri)
    if '#' in uri:
        parts = uri.split('#', 1)
        return parts[0], parts[1]
    if '/' in uri:
        parts = uri.rsplit('/', 1)
        return parts[0], parts[1]
    return uri, ''


def normalize_ns_uri(uri):
    """Normalize namespace URIs for stable dictionary keys:
       strip whitespace and trailing '#' or '/' characters."""
    if uri is None:
        return ''
    s = str(uri).strip()
    while s.endswith('#') or s.endswith('/'):
        s = s[:-1]
    return s

# Keep Collection import
from rdflib.collection import Collection

# ----------------- CSV writers (unchanged logic mostly) -----------------
def owl_csv_subclass(g, uri, output_file="subclass.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Subclass", "Restriction (onProperty)", "Restriction (quantifier)", "Superclass"])
        results_found = False

        for subclass, _, superclass in g.triples((None, RDFS.subClassOf, None)):

            # --- Subclass formatting ---
            if isinstance(subclass, URIRef):
                ns, local = custom_split_uri(str(subclass))
                ns_norm = normalize_ns_uri(ns)
                prefix = uri.get(ns_norm, f"ns{len(uri)}")
                # ensure mapping saved for later use (preserve declared mapping if present)
                uri[ns_norm] = prefix
                subclass_str = f"{prefix}:{local}"
            elif isinstance(subclass, BNode):
                if (subclass, OWL.intersectionOf, None) in g:
                    collection = Collection(g, g.value(subclass, OWL.intersectionOf))
                    subclass_parts = []
                    for item in collection:
                        if isinstance(item, URIRef):
                            ns, local = custom_split_uri(str(item))
                            ns_norm = normalize_ns_uri(ns)
                            prefix = uri.get(ns_norm, f"ns{len(uri)}")
                            uri[ns_norm] = prefix
                            subclass_parts.append(f"{prefix}:{local}")
                    subclass_str = " & ".join(subclass_parts)
                elif (subclass, RDF.type, OWL.Restriction) in g:
                    on_property = g.value(subclass, OWL.onProperty)
                    for qtype in (OWL.someValuesFrom, OWL.allValuesFrom):
                        val = g.value(subclass, qtype)
                        if val:
                            quant = "some" if qtype == OWL.someValuesFrom else "all"
                            ns_p, local_p = custom_split_uri(str(on_property))
                            ns_p_norm = normalize_ns_uri(ns_p)
                            prefix_p = uri.get(ns_p_norm, f"ns{len(uri)}")
                            uri[ns_p_norm] = prefix_p
                            prop_str = f"{prefix_p}:{local_p}"

                            ns_c, local_c = custom_split_uri(str(val))
                            ns_c_norm = normalize_ns_uri(ns_c)
                            prefix_c = uri.get(ns_c_norm, f"ns{len(uri)}")
                            uri[ns_c_norm] = prefix_c
                            class_str = f"{prefix_c}:{local_c}"

                            writer.writerow(["", prop_str, quant, class_str])
                            results_found = True
                    continue
                else:
                    continue  # Unhandled bnode subclass
            else:
                continue  # Skip unknown subclass type

            # --- Superclass formatting ---
            if isinstance(superclass, URIRef):
                ns, local = custom_split_uri(str(superclass))
                ns_norm = normalize_ns_uri(ns)
                prefix = uri.get(ns_norm, f"ns{len(uri)}")
                uri[ns_norm] = prefix
                superclass_str = f"{prefix}:{local}"
                writer.writerow([subclass_str, "", "", superclass_str])
                results_found = True

            elif isinstance(superclass, BNode):
                if (superclass, RDF.type, OWL.Restriction) in g:
                    on_property = g.value(superclass, OWL.onProperty)
                    for qtype in (OWL.someValuesFrom, OWL.allValuesFrom):
                        val = g.value(superclass, qtype)
                        if val:
                            quant = "some" if qtype == OWL.someValuesFrom else "all"
                            ns_p, local_p = custom_split_uri(str(on_property))
                            ns_p_norm = normalize_ns_uri(ns_p)
                            prefix_p = uri.get(ns_p_norm, f"ns{len(uri)}")
                            uri[ns_p_norm] = prefix_p
                            prop_str = f"{prefix_p}:{local_p}"

                            ns_c, local_c = custom_split_uri(str(val))
                            ns_c_norm = normalize_ns_uri(ns_c)
                            prefix_c = uri.get(ns_c_norm, f"ns{len(uri)}")
                            uri[ns_c_norm] = prefix_c
                            class_str = f"{prefix_c}:{local_c}"

                            writer.writerow([subclass_str, prop_str, quant, class_str])
                            results_found = True
                    continue

                elif (superclass, OWL.intersectionOf, None) in g:
                    collection = Collection(g, g.value(superclass, OWL.intersectionOf))
                    parts = []
                    for item in collection:
                        if isinstance(item, URIRef):
                            ns, local = custom_split_uri(str(item))
                            ns_norm = normalize_ns_uri(ns)
                            prefix = uri.get(ns_norm, f"ns{len(uri)}")
                            uri[ns_norm] = prefix
                            parts.append(f"{prefix}:{local}")
                    superclass_str = " & ".join(parts)
                    writer.writerow([subclass_str, "", "", superclass_str])
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
                    ns_norm = normalize_ns_uri(ns)
                    prefix = uri.get(ns_norm, f"ns{len(uri)}")
                    uri[ns_norm] = prefix
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
                namespace_norm = normalize_ns_uri(namespace)
                if namespace_norm in uri:
                    a = uri[namespace_norm]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace_norm] = prefix
                    a = uri[namespace_norm]+":"+local_name
            else:
                a = '_:'+subject

            range = (str)(obj).rsplit('/')[-1]
            if (obj.rsplit('/')[0] == 'http:'):
                name = URIRef(obj)
                namespace, local_name = split_uri(str(name))
                namespace_norm = normalize_ns_uri(namespace)
                if namespace_norm in uri:
                    b = uri[namespace_norm]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace_norm] = prefix
                    b = uri[namespace_norm]+":"+local_name
            else:
                b = '_:'+obj

            rows = [a, b]
            writer.writerow(rows)

    f.close()
    return 'domain.csv'

def extract_prefixes(owl_file, output_csv='prefixiri.csv'):
    """
    Extracts xmlns declarations (prefixes) from the first <rdf:RDF> tag of the OWL file
    and saves them in prefixiri.csv as Prefix, Namespace.
    """
    with open(owl_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the rdf:RDF opening tag content only (before first ">")
    match = re.search(r'<rdf:RDF\s+(.*?)>', content, re.DOTALL)
    if not match:
        print("❌ No <rdf:RDF> tag found in the file.")
        return

    rdf_tag = match.group(1)

    # Extract xmlns and xml:base attributes
    pattern = r'xmlns(?::([a-zA-Z0-9_\-]+))?="([^"]+)"|xml:base="([^"]+)"'
    found = re.findall(pattern, rdf_tag)

    prefixes = []
    for pref, ns, base in found:
        if pref:  # e.g. xmlns:rdfs="..."
            prefixes.append((pref, ns))
        elif base:  # xml:base
            prefixes.append(("xml:base", base))
        else:  # default xmlns="..."
            prefixes.append((':', ns))

    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Prefix", "Namespace"])
        writer.writerows(prefixes)

    print(f"✅ Extracted {len(prefixes)} prefixes to {output_csv}")

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
                namespace_norm = normalize_ns_uri(namespace)
                if namespace_norm in uri:
                    a = uri[namespace_norm]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace_norm] = prefix
                    a = uri[namespace_norm]+":"+local_name
            else:
                a = '_:'+subject

            range = (str)(obj).rsplit('/')[-1]
            if (obj.rsplit('/')[0] == 'http:'):
                name = URIRef(obj)
                namespace, local_name = split_uri(str(name))
                namespace_norm = normalize_ns_uri(namespace)
                if namespace_norm in uri:
                    b = uri[namespace_norm]+":" + local_name
                else:
                    prefix = 'ns'+str(count)
                    count += 1
                    uri[namespace_norm] = prefix
                    b = uri[namespace_norm]+":"+local_name
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
                        namespace_norm = normalize_ns_uri(namespace)
                        if namespace_norm in uri:
                            a = uri[namespace_norm]+":" + local_name
                        else:
                            prefix = 'ns'+str(count)
                            count += 1
                            uri[namespace_norm] = prefix
                            a = uri[namespace_norm]+":"+local_name
                    else:
                        a = '_:'+subject

                    objj = (str)(obj).rsplit('/')[-1]
                    if (obj.rsplit('/')[0] == 'http:'):
                        name = URIRef(obj)
                        namespace, local_name = split_uri(str(name))
                        namespace_norm = normalize_ns_uri(namespace)
                        if namespace_norm in uri:
                            b = uri[namespace_norm]+":" + local_name
                        else:
                            prefix = 'ns'+str(count)
                            count += 1
                            uri[namespace_norm] = prefix
                            b = uri[namespace_norm]+":"+local_name
                    else:
                        b = '_:'+obj

                    rows = [a, b]
                    writer.writerow(rows)
    f.close()
    return 'instances.csv'

def owl_csv_subproperty(g, uri, output_file='subproperty.csv'):
    """
    Extracts subProperty and property-chain axioms from an rdflib.Graph `g`.
    - Writes rows: subproperty, role1, role2, superproperty
    """
    global count
    from rdflib import URIRef
    from rdflib.collection import Collection

    fields = ['subproperty', 'role1', 'role2', 'superproperty']
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        # --- 1) Direct subPropertyOf ---
        for subj, pred, obj in g.triples((None, RDFS.subPropertyOf, None)):
            if isinstance(obj, URIRef) and str(obj) != str(OWL.ObjectProperty):
                sub_name = f"_:{subj}"
                super_name = f"_:{obj}"
                
                if isinstance(subj, URIRef):
                    ns1, local1 = custom_split_uri(str(subj))
                    ns1_norm = normalize_ns_uri(ns1)
                    if ns1_norm not in uri:
                        uri[ns1_norm] = f"ns{count}"
                        count += 1
                    sub_name = f"{uri[ns1_norm]}:{local1}"
                
                if isinstance(obj, URIRef):
                    ns2, local2 = custom_split_uri(str(obj))
                    ns2_norm = normalize_ns_uri(ns2)
                    if ns2_norm not in uri:
                        uri[ns2_norm] = f"ns{count}"
                        count += 1
                    super_name = f"{uri[ns2_norm]}:{local2}"
                
                writer.writerow([sub_name, "", "", super_name])

        # --- 2) Property chains ---
        for superprop, _, listnode in g.triples((None, OWL.propertyChainAxiom, None)):
            # superproperty name
            super_name = f"_:{superprop}"
            if isinstance(superprop, URIRef):
                ns_s, local_s = custom_split_uri(str(superprop))
                ns_s_norm = normalize_ns_uri(ns_s)
                if ns_s_norm not in uri:
                    uri[ns_s_norm] = f"ns{count}"
                    count += 1
                super_name = f"{uri[ns_s_norm]}:{local_s}"

            # expand RDF list
            try:
                coll = Collection(g, listnode)
                items = list(coll)
            except Exception:
                continue  # skip malformed chains

            # convert to prefixed strings
            def elem_pref(x):
                if isinstance(x, URIRef):
                    ns, local = custom_split_uri(str(x))
                    ns_norm = normalize_ns_uri(ns)
                    if ns_norm not in uri:
                        uri[ns_norm] = f"ns{count}"
                        globals()['count'] += 1
                    return f"{uri[ns_norm]}:{local}"
                else:
                    return f"_:{x}"

            if len(items) == 0:
                continue
            elif len(items) == 1:
                r1 = elem_pref(items[0])
                writer.writerow(["chain", r1, "", super_name])
            elif len(items) == 2:
                r1 = elem_pref(items[0])
                r2 = elem_pref(items[1])
                writer.writerow(["chain", r1, r2, super_name])
            else:
                r1 = elem_pref(items[0])
                r2 = elem_pref(items[1])
                remaining = " o ".join(elem_pref(x) for x in items[2:])
                r1_full = f"{r1} o {remaining}" if remaining else r1
                writer.writerow(["chain", r1_full, r2, super_name])

    return output_file

def export_subproperties(owl_file, csv_file):
    onto = get_ontology(owl_file).load()

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "role1", "role2", "superproperty"])

        # 1. Direct subproperty axioms
        for prop in onto.object_properties():
            for superprop in prop.is_a:
                if hasattr(superprop, "iri") and superprop.iri != "http://www.w3.org/2002/07/owl#ObjectProperty":
                    writer.writerow(["subproperty", prop.iri, "", superprop.iri])

        # 2. Property chain axioms
        for prop in onto.object_properties():
            if hasattr(prop, "subpropertychains") and prop.subpropertychains:
                for chain in prop.subpropertychains:
                    if len(chain) == 2:
                        writer.writerow(["chain", chain[0].iri, chain[1].iri, prop.iri])
                    else:
                        chain_str = " o ".join(p.iri for p in chain)
                        writer.writerow([f"chain+{len(chain)}", chain_str, "", prop.iri])

def owl_csv_inverseof(g, uri):
    global count
    fields = ['inverseOf', 'Object']
    seen_pairs = set()  # Track seen inverse pairs
    
    with open('inverseOf.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        
        for subject, predicate, obj in g:
            if predicate == rdflib.OWL.inverseOf:
                pair = tuple(sorted([str(subject), str(obj)]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    
                    # Process subject
                    if (str(subject).startswith('http:') or str(subject).startswith('https:')):
                        name = URIRef(subject)
                        namespace, local_name = split_uri(str(name))
                        namespace_norm = normalize_ns_uri(namespace)
                        if namespace_norm in uri:
                            a = f"{uri[namespace_norm]}:{local_name}"
                        else:
                            prefix = f"ns{count}"
                            count += 1
                            uri[namespace_norm] = prefix
                            a = f"{prefix}:{local_name}"
                    else:
                        a = f"_:{subject}"
                    
                    # Process object
                    if (str(obj).startswith('http:') or str(obj).startswith('https:')):
                        name = URIRef(obj)
                        namespace, local_name = split_uri(str(name))
                        namespace_norm = normalize_ns_uri(namespace)
                        if namespace_norm in uri:
                            b = f"{uri[namespace_norm]}:{local_name}"
                        else:
                            prefix = f"ns{count}"
                            count += 1
                            uri[namespace_norm] = prefix
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
            namespace_norm = normalize_ns_uri(namespace)
            if namespace_norm in uri:
                a1 = uri[namespace_norm]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace_norm] = prefix
                a1 = uri[namespace_norm]+":"+local_name
        else:
            a1 = '_:'+ str(subject)

        if (str(predicate).rsplit('/')[0] == 'http:'):
            name = URIRef(predicate)
            namespace, local_name = split_uri(str(name))
            namespace_norm = normalize_ns_uri(namespace)
            if namespace_norm in uri:
                b1 = uri[namespace_norm]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace_norm] = prefix
                b1 = uri[namespace_norm]+":"+local_name
        else:
            b1 = '_:'+ str(predicate)

        if isinstance(obj, (int, float, np.integer)):  # Numeric cardinality
            c1 = str(obj)
        elif str(obj).startswith('http:') or str(obj).startswith('https:'):  # URI
            name = URIRef(obj)
            namespace, local_name = split_uri(str(name))
            namespace_norm = normalize_ns_uri(namespace)
            if namespace_norm in uri:
                c1 = uri[namespace_norm]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace_norm] = prefix
                c1 = uri[namespace_norm]+":"+local_name
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

# Add these imports near top of owl_csv_code.py
from rdflib import RDF, RDFS, OWL, URIRef, BNode, Literal

def extract_annotation_axioms_and_props(g: Graph):
    """
    Scan an rdflib.Graph and extract:
     - reified OWL axiom annotation assertions (owl:Axiom with owl:annotatedSource/Property/Target)
     - explicit annotation property declarations (prop rdf:type owl:AnnotationProperty)
     - heuristic annotation assertions (predicate used with literal objects and lacking a property typing)
    Returns:
      {
        'reified_axioms': [ { 'axiom_node': node, 'source': s, 'property': p, 'target': t, 'annotations_on_axiom': [(k,v), ...] }, ... ],
        'declared_annotation_props': set([URIRef,...]),
        'plain_annotation_assertions': [ (subject, predicate, object), ... ],
        'heuristic_props': set([URIRef,...])
      }
    """
    reified = []
    declared_props = set()
    plain_assertions = []
    heuristic_props = set()

    # 1) find explicit annotation property declarations
    for s, p, o in g.triples((None, RDF.type, OWL.AnnotationProperty)):
        if isinstance(s, URIRef):
            declared_props.add(s)

    # 2) find reified OWL axioms (owl:Axiom nodes)
    for ax_node in set(g.subjects(RDF.type, OWL.Axiom)):
        # collect annotatedSource, annotatedProperty, annotatedTarget
        src = next(g.objects(ax_node, OWL.annotatedSource), None)
        prop = next(g.objects(ax_node, OWL.annotatedProperty), None)
        tgt = next(g.objects(ax_node, OWL.annotatedTarget), None)

        # collect any annotations on the axiom node itself (e.g., rdfs:comment on the axiom)
        annotations_on_axiom = []
        for a_pred, a_obj in g.predicate_objects(ax_node):
            # skip the structural predicates we've already used
            if a_pred in (RDF.type, OWL.annotatedSource, OWL.annotatedProperty, OWL.annotatedTarget):
                continue
            annotations_on_axiom.append((a_pred, a_obj))

        if prop is not None:
            # record declared prop if present on the axiom
            if isinstance(prop, URIRef):
                # sometimes axiom refers to property but there is no explicit declaration; keep this info
                if (prop, RDF.type, OWL.AnnotationProperty) in g:
                    declared_props.add(prop)
                else:
                    # not declared, but used as annotation property in axioms
                    heuristic_props.add(prop)

        reified.append({
            'axiom_node': ax_node,
            'source': src,
            'property': prop,
            'target': tgt,
            'annotations_on_axiom': annotations_on_axiom
        })

    # 3) plain triples that are annotation assertions: 
    #    if predicate is in declared_props OR predicate used with Literal object and predicate not typed as ObjectProperty/DatatypeProperty
    for s, p, o in g:
        if isinstance(p, URIRef):
            # skip structural/triple forms that are obviously not annotation assertions
            if (p, RDF.type, OWL.AnnotationProperty) in g:
                plain_assertions.append((s,p,o))
                declared_props.add(p)
                continue

            # If object is Literal and predicate is not typed as owl:ObjectProperty or owl:DatatypeProperty,
            # then treat it as a heuristic annotation assertion.
            if isinstance(o, Literal):
                if not ((p, RDF.type, OWL.ObjectProperty) in g or (p, RDF.type, OWL.DatatypeProperty) in g):
                    plain_assertions.append((s,p,o))
                    heuristic_props.add(p)

    result = {
        'reified_axioms': reified,
        'declared_annotation_props': declared_props,
        'plain_annotation_assertions': plain_assertions,
        'heuristic_props': heuristic_props
    }
    return result

def main(file, output_filename):
    extract_prefixes(file, output_csv='prefixiri.csv')

    g = Graph()
    g.parse(file, format='xml')  
    ann = extract_annotation_axioms_and_props(g)
    global count
    count = 1
    
    uri = {}  # mapping: normalized_namespace -> prefix_string ('' for default)
    onproperty_dict = {}
    unique_properties = set()

    # --- Pre-populate uri with declared prefixes from the graph's namespace manager ---
    # Also keep an original_ns_map to preserve the exact namespace string (with trailing # or /)
    original_ns_map = {}
    for prefix, ns in g.namespace_manager.namespaces():
        ns_norm = normalize_ns_uri(ns)
        # rdflib may give None or '' for default; normalize to empty prefix string ''
        if prefix is None:
            pref_value = ''
        else:
            pref_value = str(prefix)
        uri[ns_norm] = pref_value
        original_ns_map[ns_norm] = str(ns)  # preserve the exact string for writing later

    # iterate triples to collect any additional namespaces (that weren't declared)
    for s, p, o in g:
        for node in [s, p, o]:
            if isinstance(node, URIRef):
                try:
                    ns, _ = custom_split_uri(str(node))
                    ns_norm = normalize_ns_uri(ns)
                    if ns_norm not in uri:
                        # assign a synthetic prefix only if not already declared
                        uri[ns_norm] = f"ns{count}"
                        count += 1
                        # keep a fallback original string (without trimming) if no declared prefix was present
                        original_ns_map.setdefault(ns_norm, ns)
                except Exception as e:
                    print(f"Error processing URI {node}: {e}")
                    continue

        # Identify object properties etc (existing logic)
        if (p == RDF.type and o == OWL.ObjectProperty) or \
           (p == RDF.type and o == RDF.Property) or \
           (p == RDFS.domain and isinstance(s, URIRef)) or \
           (p == RDFS.range and isinstance(s, URIRef)):
            if isinstance(s, URIRef):
                ns, local = custom_split_uri(str(s))
                ns_norm = normalize_ns_uri(ns)
                prop_name = f"{uri.get(ns_norm, 'ns0')}:{local}"
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

    default_ns = None
    for k, v in uri.items():
        if v == '':
            default_ns = original_ns_map.get(k, k)
            break
    print('The default namespace for the ontology is ' + str(default_ns))
    not_processing(g, uri)