import pandas as pd
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, OWL
import re
import os

def load_ontology(owl_file):
    """Load the OWL ontology into an RDF graph"""
    g = Graph()
    # Convert Windows path to file:// URL format
    if owl_file.startswith('C:\\'):
        owl_file = owl_file.replace('\\', '/')
        owl_file = 'file:///' + owl_file
    g.parse(owl_file)
    return g

def get_namespace_mapping(csv_dir):
    """Load namespace mappings from prefixiri.csv"""
    prefix_mapping = {}
    try:
        df = pd.read_csv(f"{csv_dir}/prefixiri.csv")
        for _, row in df.iterrows():
            prefix_mapping[row['Prefix']] = row['Namespace']
    except FileNotFoundError:
        print("Warning: prefixiri.csv not found - using empty namespace mapping")
    return prefix_mapping

def expand_qname(qname, prefix_mapping):
    """Convert prefixed name (prefix:local) to full URI with better error handling"""
    if pd.isna(qname) or not qname or str(qname).lower() == 'none':
        return None
        
    qname = str(qname).strip()
    
    # Skip complex expressions
    if '+' in qname or 'Restriction(' in qname:
        return None
        
    if qname.startswith('http://') or qname.startswith('https://'):
        return qname
        
    if ':' not in qname:
        return None
        
    try:
        prefix, local = qname.split(':', 1)
        if prefix in prefix_mapping:
            return prefix_mapping[prefix] + local
        return None
    except:
        return None

'''
def validate_subclasses(g, csv_dir, prefix_mapping):
    """Validate subclass relationships with better restriction handling"""
    print("\nValidating subclass relationships...")
    df = pd.read_csv(f"{csv_dir}/subclass.csv")
    errors = 0
    
    for _, row in df.iterrows():
        subclass = expand_qname(row['Subclass'], prefix_mapping)
        superclass = row['Superclass']
        
        # Skip obviously malformed entries
        if not superclass or superclass.lower() == 'none':
            continue
            
        # Handle restriction patterns
        if 'Restriction' in superclass and '+' in superclass:
            parts = [p.strip() for p in superclass.split('+')]
            if len(parts) >= 3 and 'part_of' in superclass:
                # This is likely a restriction - skip as we'll handle differently
                continue
                
        superclass_uri = expand_qname(superclass, prefix_mapping)
        
        # Check direct subclass relationship
        if not (URIRef(subclass), RDFS.subClassOf, URIRef(superclass_uri)) in g:
            # Check for restriction-based subclass
            restriction_found = False
            for s in g.subjects(RDF.type, OWL.Restriction):
                if (URIRef(subclass), RDFS.subClassOf, s) in g:
                    restriction_found = True
                    break
                    
            if not restriction_found:
                print(f"Error: Missing subclass relationship {subclass} -> {superclass}")
                errors += 1
    
    print(f"Found {errors} errors in subclass relationships")
'''

def validate_subclasses(g, csv_dir, prefix_mapping):
    """Validate subclass relationships with proper restriction handling"""
    print("\nValidating subclass relationships...")
    df = pd.read_csv(f"{csv_dir}/subclass.csv")
    errors = 0
    
    for _, row in df.iterrows():
        subclass = expand_qname(row['Subclass'], prefix_mapping)
        superclass = row['Superclass']
        
        # Skip empty or invalid entries
        if not superclass or superclass.lower() == 'none':
            continue
            
        # Handle complex expressions (unions, intersections, restrictions)
        if '+' in superclass:
            # This is a complex expression - skip detailed validation
            # Just verify the subclass exists in the ontology
            if not (URIRef(subclass), RDF.type, OWL.Class) in g:
                print(f"Error: Subclass {subclass} not declared as a class")
                errors += 1
            continue
            
        # Handle simple URIs
        try:
            superclass_uri = expand_qname(superclass, prefix_mapping)
            
            # Check direct subclass relationship
            if not (URIRef(subclass), RDFS.subClassOf, URIRef(superclass_uri)) in g:
                print(f"Error: Missing subclass relationship {subclass} -> {superclass_uri}")
                errors += 1
        except Exception as e:
            print(f"Skipping complex superclass expression: {superclass}")
            continue
    
    print(f"Found {errors} errors in subclass relationships")
def validate_classes(g, csv_dir, prefix_mapping):
    """Validate class declarations"""
    print("\nValidating class declarations...")
    df = pd.read_csv(f"{csv_dir}/owlclass.csv")
    errors = 0
    
    for _, row in df.iterrows():
        class_uri = expand_qname(row['OWL Class'], prefix_mapping)
        if not (URIRef(class_uri), RDF.type, OWL.Class) in g:
            print(f"Error: Missing class declaration for {class_uri}")
            errors += 1
    
    print(f"Found {errors} errors in class declarations")

def validate_domain_ranges(g, csv_dir, prefix_mapping, relation_type):
    """Validate domain or range relationships"""
    filename = 'domain.csv' if relation_type == 'domain' else 'range.csv'
    print(f"\nValidating {relation_type} relationships...")
    df = pd.read_csv(f"{csv_dir}/{filename}")
    errors = 0
    predicate = RDFS.domain if relation_type == 'domain' else RDFS.range
    
    for _, row in df.iterrows():
        property_uri = expand_qname(row['Object'], prefix_mapping)
        class_uri = expand_qname(row[relation_type.capitalize()], prefix_mapping)
        
        if not (URIRef(property_uri), predicate, URIRef(class_uri)) in g:
            print(f"Error: Missing {relation_type} relationship {property_uri} -> {class_uri}")
            errors += 1
    
    print(f"Found {errors} errors in {relation_type} relationships")

def validate_instances(g, csv_dir, prefix_mapping):
    """Validate instance declarations"""
    print("\nValidating instances...")
    df = pd.read_csv(f"{csv_dir}/instances.csv")
    errors = 0
    
    for _, row in df.iterrows():
        instance_uri = expand_qname(row['Instances'], prefix_mapping)
        class_uri = expand_qname(row['Class'], prefix_mapping)
        
        if not (URIRef(instance_uri), RDF.type, URIRef(class_uri)) in g:
            print(f"Error: Missing instance relationship {instance_uri} -> {class_uri}")
            errors += 1
    
    print(f"Found {errors} errors in instance declarations")

def validate_subproperties(g, csv_dir, prefix_mapping):
    """Validate subproperty relationships"""
    print("\nValidating subproperty relationships...")
    df = pd.read_csv(f"{csv_dir}/subproperty.csv")
    errors = 0
    
    for _, row in df.iterrows():
        subprop = expand_qname(row['subproperty'], prefix_mapping)
        superprop = expand_qname(row['Object'], prefix_mapping)
        
        if not (URIRef(subprop), RDFS.subPropertyOf, URIRef(superprop)) in g:
            print(f"Error: Missing subproperty relationship {subprop} -> {superprop}")
            errors += 1
    
    print(f"Found {errors} errors in subproperty relationships")

def validate_inverse_properties(g, csv_dir, prefix_mapping):
    """Validate inverse property relationships"""
    print("\nValidating inverse properties...")
    df = pd.read_csv(f"{csv_dir}/inverseOf.csv")
    errors = 0
    
    for _, row in df.iterrows():
        prop1 = expand_qname(row['inverseOf'], prefix_mapping)
        prop2 = expand_qname(row['Object'], prefix_mapping)
        
        found = False
        # Check both directions since OWL.inverseOf is symmetric
        if (URIRef(prop1), OWL.inverseOf, URIRef(prop2)) in g:
            found = True
        if (URIRef(prop2), OWL.inverseOf, URIRef(prop1)) in g:
            found = True
            
        if not found:
            print(f"Error: Missing inverse relationship between {prop1} and {prop2}")
            errors += 1
    
    print(f"Found {errors} errors in inverse property relationships")

def validate_all_values_from(g, csv_dir, prefix_mapping):
    """Validate allValuesFrom restrictions"""
    print("\nValidating allValuesFrom restrictions...")
    df = pd.read_csv(f"{csv_dir}/allvaluesfrom.csv")
    errors = 0
    
    for _, row in df.iterrows():
        class_uri = expand_qname(row['Class'], prefix_mapping)
        prop_uri = expand_qname(row['OnProperty'], prefix_mapping)
        value_uri = expand_qname(row['allValuesFrom'], prefix_mapping)
        
        # Find the restriction node
        found = False
        for s, p, o in g.triples((None, RDF.type, OWL.Restriction)):
            if (s, OWL.onProperty, URIRef(prop_uri)) in g:
                if (s, OWL.allValuesFrom, URIRef(value_uri)) in g:
                    if (URIRef(class_uri), RDFS.subClassOf, s) in g:
                        found = True
                        break
        
        if not found:
            print(f"Error: Missing allValuesFrom restriction for {class_uri} on {prop_uri} with {value_uri}")
            errors += 1
    
    print(f"Found {errors} errors in allValuesFrom restrictions")

def validate_some_values_from(g, csv_dir, prefix_mapping):
    """Validate someValuesFrom restrictions"""
    print("\nValidating someValuesFrom restrictions...")
    df = pd.read_csv(f"{csv_dir}/somevaluesfrom.csv")
    errors = 0
    
    for _, row in df.iterrows():
        prop_uri = expand_qname(row['OnProperty'], prefix_mapping)
        value_uri = expand_qname(row['SomeValuesFrom'], prefix_mapping)
        
        # Find any restriction using this property and value
        found = False
        for s, p, o in g.triples((None, OWL.onProperty, URIRef(prop_uri))):
            if (s, OWL.someValuesFrom, URIRef(value_uri)) in g:
                found = True
                break
        
        if not found:
            print(f"Error: Missing someValuesFrom restriction on {prop_uri} with {value_uri}")
            errors += 1
    
    print(f"Found {errors} errors in someValuesFrom restrictions")

def validate_max_cardinality(g, csv_dir, prefix_mapping):
    """Validate maxCardinality restrictions"""
    print("\nValidating maxCardinality restrictions...")
    df = pd.read_csv(f"{csv_dir}/maxcardinality.csv")
    errors = 0
    
    for _, row in df.iterrows():
        class_uri = expand_qname(row['Class'], prefix_mapping)
        prop_uri = expand_qname(row['OnProperty'], prefix_mapping)
        cardinality = row['maxCardinality']
        
        # Find the restriction node
        found = False
        for s, p, o in g.triples((None, RDF.type, OWL.Restriction)):
            if (s, OWL.onProperty, URIRef(prop_uri)) in g:
                if (s, OWL.maxCardinality, Literal(cardinality)) in g:
                    if (URIRef(class_uri), RDFS.subClassOf, s) in g:
                        found = True
                        break
        
        if not found:
            print(f"Error: Missing maxCardinality restriction for {class_uri} on {prop_uri} with {cardinality}")
            errors += 1
    
    print(f"Found {errors} errors in maxCardinality restrictions")

def validate_first_rest(g, csv_dir, prefix_mapping):
    """Validate first/rest relationships (for lists)"""
    print("\nValidating first/rest relationships...")
    df = pd.read_csv(f"{csv_dir}/firstrest.csv")
    errors = 0
    
    for _, row in df.iterrows():
        list_uri = expand_qname(row['Class'], prefix_mapping)
        first_uri = expand_qname(row['First'], prefix_mapping)
        rest_uri = expand_qname(row['Rest'], prefix_mapping)
        
        if not (URIRef(list_uri), RDF.first, URIRef(first_uri)) in g:
            print(f"Error: Missing first relationship {list_uri} -> {first_uri}")
            errors += 1
        
        if not (URIRef(list_uri), RDF.rest, URIRef(rest_uri)) in g:
            print(f"Error: Missing rest relationship {list_uri} -> {rest_uri}")
            errors += 1
    
    print(f"Found {errors} errors in first/rest relationships")

def validate_property_declarations(g, csv_dir, prefix_mapping):
    """Validate property declarations"""
    print("\nValidating property declarations...")
    df = pd.read_csv(f"{csv_dir}/onproperty.csv")
    errors = 0
    
    for _, row in df.iterrows():
        prop_uri = expand_qname(row['ObjectProperty'], prefix_mapping)
        
        # Check if it's declared as either ObjectProperty or Property
        if not ((URIRef(prop_uri), RDF.type, OWL.ObjectProperty) in g or 
                (URIRef(prop_uri), RDF.type, RDF.Property) in g):
            print(f"Error: Missing property declaration for {prop_uri}")
            errors += 1
    
    print(f"Found {errors} errors in property declarations")

def validate_all(owl_file, csv_dir):
    """Run all validation checks with better error handling"""
    try:
        g = load_ontology(owl_file)
        prefix_mapping = get_namespace_mapping(csv_dir)
        
        print("\n=== Starting Validation ===")
        validate_classes(g, csv_dir, prefix_mapping)
        validate_subclasses(g, csv_dir, prefix_mapping)
        validate_domain_ranges(g, csv_dir, prefix_mapping, 'domain')
        validate_domain_ranges(g, csv_dir, prefix_mapping, 'range')
        validate_instances(g, csv_dir, prefix_mapping)
        validate_subproperties(g, csv_dir, prefix_mapping)
        validate_inverse_properties(g, csv_dir, prefix_mapping)
        validate_all_values_from(g, csv_dir, prefix_mapping)
        validate_some_values_from(g, csv_dir, prefix_mapping)
        validate_max_cardinality(g, csv_dir, prefix_mapping)
        validate_first_rest(g, csv_dir, prefix_mapping)
        validate_property_declarations(g, csv_dir, prefix_mapping)
        
        print("\n=== Validation Complete ===")
    except Exception as e:
        print(f"\nError during validation: {str(e)}")

if __name__ == "__main__":
    owl_file = "endocarditis.owl"
    csv_dir = "endocarditis.xlsx"

    # Verify files exist
    if not os.path.isfile(owl_file):
        print(f"Error: OWL file not found at {owl_file}")
    elif not os.path.isdir(csv_dir):
        print(f"Error: CSV directory not found at {csv_dir}")
    else:
        validate_all(owl_file, csv_dir)