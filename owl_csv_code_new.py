import logging
import pandas as pd
import csv
import rdflib
from rdflib import Graph, URIRef, BNode, RDF, RDFS, OWL
from rdflib.namespace import split_uri
import os

# Configure logging
logging.basicConfig(filename='dumm/logfile.log', level=logging.DEBUG)

def get_prefixed_uri(value, uri, count):
    """Resolves a prefixed URI or blank node to a full URI or BNode."""
    if value.startswith('http:'):
        namespace, local_name = split_uri(str(URIRef(value)))
        if namespace not in uri:
            uri[namespace] = f'ns{count[0]}'
            count[0] += 1
        return f'{uri[namespace]}:{local_name}'
    return f'_:{value}'

def write_csv(filename, fields, rows):
    """Writes data to a CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)
        writer.writerows(rows)
    return filename

def extract_axioms(g, predicate, fields, uri, count):
    """Extracts axioms from RDF graph based on predicate."""
    rows = []
    for subj, obj in g.subject_objects(predicate=predicate):
        a = get_prefixed_uri(str(subj), uri, count)
        b = get_prefixed_uri(str(obj), uri, count)
        rows.append([a, b])
    return write_csv(f'{fields[0].lower()}.csv', fields, rows)

def extract_triples(g, predicate, fields, uri, count):
    """Extracts triples from RDF graph based on predicate."""
    rows = []
    for subj, pred, obj in g:
        if pred == predicate:
            a = get_prefixed_uri(str(subj), uri, count)
            b = get_prefixed_uri(str(obj), uri, count)
            rows.append([a, b])
    return write_csv(f'{fields[0].lower()}.csv', fields, rows)

def extract_complex_axioms(g, predicate, onproperty_dict, fields, uri, count):
    """Extracts complex axioms like allValuesFrom, someValuesFrom, etc."""
    axiom_dict = {}
    for subj, pred, obj in g:
        if pred == predicate:
            axiom_dict[subj] = obj

    temp_file = write_csv('temp.csv', fields, [[k, onproperty_dict[k], v] for k, v in axiom_dict.items() if k in onproperty_dict])

    temp_df = pd.read_csv(temp_file)
    classs = temp_df.iloc[:, 0].values
    onproperty = temp_df.iloc[:, 1].values
    values = temp_df.iloc[:, 2].values

    rows = []
    for subject, predicate, obj in zip(classs, onproperty, values):
        a = get_prefixed_uri(subject, uri, count)
        b = get_prefixed_uri(predicate, uri, count)
        c = get_prefixed_uri(obj, uri, count)
        rows.append([a, b, c])

    return write_csv(f'{fields[0].lower()}.csv', fields, rows)

def not_processing(g, uri):
    """Logs unprocessed triples."""
    for subject, predicate, obj in g:
        if not ((predicate == RDFS.subClassOf) or 
                (predicate == RDF.type and obj == OWL.Class) or 
                (predicate == RDFS.domain) or 
                (predicate == RDFS.range) or 
                (predicate == RDF.type and obj == OWL.NamedIndividual) or 
                (predicate == RDFS.subPropertyOf) or 
                (predicate == OWL.inverseOf) or 
                (predicate == OWL.onProperty) or 
                (predicate == RDF.rest) or 
                (predicate == RDF.first)):
            logging.error(f"Unprocessed triple: {subject} {predicate} {obj}")

def main(file):
    """Main function to process the RDF file and generate CSV files."""
    g = Graph()
    g.parse(file)

    count = [1]
    uri = {}

    # Extract onProperty relationships
    onproperty_dict = {subj: obj for subj, pred, obj in g if pred == OWL.onProperty}
    write_csv('dumm/onproperty.csv', ['Class', 'OnProperty'], [[k, v] for k, v in onproperty_dict.items()])

    # Extract first relationships
    first_dict = {subj: obj for subj, pred, obj in g if pred == RDF.first}
    write_csv('dumm/first.csv', ['Class', 'First'], [[k, v] for k, v in first_dict.items()])

    # Extract various axioms
    csv_files = [
        extract_axioms(g, RDFS.subClassOf, ['Class', 'Parent'], uri, count),
        extract_axioms(g, RDFS.domain, ['Object', 'Domain'], uri, count),
        extract_axioms(g, RDFS.range, ['Object', 'Range'], uri, count),
        extract_axioms(g, RDFS.subPropertyOf, ['Subproperty', 'Object'], uri, count),
        extract_axioms(g, OWL.inverseOf, ['InverseOf', 'Object'], uri, count),
        extract_triples(g, RDF.type, ['Instances', 'Class'], uri, count),
        extract_complex_axioms(g, OWL.allValuesFrom, onproperty_dict, ['Class', 'OnProperty', 'AllValuesFrom'], uri, count),
        extract_complex_axioms(g, OWL.someValuesFrom, onproperty_dict, ['Class', 'OnProperty', 'SomeValuesFrom'], uri, count),
        extract_complex_axioms(g, OWL.maxCardinality, onproperty_dict, ['Class', 'OnProperty', 'MaxCardinality'], uri, count),
        extract_complex_axioms(g, RDF.rest, first_dict, ['Class', 'First', 'Rest'], uri, count),
    ]

    # Write prefix mappings to CSV
    write_csv('prefixiri.csv', ['Prefix', 'Namespace'], [[v, k] for k, v in uri.items()])

    # Combine all CSV files into an Excel file
    name = input('Output file name: ') + '.xlsx'
    with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f'The default namespace for the ontology is {uri.get("ns1")}')
    not_processing(g, uri)


main("pizza.owl")