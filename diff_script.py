#!/usr/bin/env python3
"""
owl_diff.py

This script takes two OWL files as input, loads them using Owlready2,
and then compares (“diffs”) various axioms between them.
The axioms compared include:
  - OWL Classes
  - Property Domains
  - Subclass relationships
  - Property Ranges
  - Instances of classes
  - Subproperty relationships
  - Inverse properties
  - Restrictions (allValuesFrom, someValuesFrom, maxCardinality, firstrest)
  - Prefix IRI (base IRI of the ontology)

For each axiom, the script prints out a match (in green) or mismatch (in red)
using colorful ANSI outputs via Colorama.
"""

import argparse
import owlready2
from owlready2 import get_ontology, Restriction
import colorama
from colorama import Fore, Style

# Initialize Colorama for colored output in the terminal.
colorama.init(autoreset=True)

def load_ontology(path):
    """Load an ontology from a given file path."""
    try:
        onto = get_ontology(path)
        onto.load()
        return onto
    except Exception as e:
        print(Fore.RED + f"Error loading ontology from {path}: {e}")
        exit(1)

def diff_classes(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing OWL Classes ===" + Style.RESET_ALL)
    classes1 = list(onto1.classes())
    classes2 = {c.iri.split("#")[1]: c for c in onto2.classes() if ':N' not in c.iri}
    for c in classes1:
        if c.iri.split("#")[1] in classes2:
            print(Fore.GREEN + f"Match: Class '{c.name}' with IRI {c.iri}")
        else:
            print(Fore.RED + f"Mismatch: Class '{c.name}' with IRI {c.iri} not found in second ontology.")

def diff_property_domains(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Property Domains ===" + Style.RESET_ALL)
    # Process all properties (object and data properties)

    prop1 = list(onto1.properties())
    prop2 = {i.iri.split("#")[1] for i in onto2.properties()}
    prop2_domain = []
    for p2 in list(onto2.properties()):
        p2_iri_d=[]
        for p2_d in p2.domain:
            p2_iri_d.append(p2_d.iri.split("#")[1])
        prop2_domain.append(p2_iri_d)
    for prop in prop1:
        if prop.iri.split("#")[1] not in prop2:
            print(Fore.RED + f"Mismatch: Property '{prop.name}' not found in second ontology.")
            continue
        else:
            print(Fore.GREEN + f"Match: Property '{prop.name}' with iri {prop.iri}.")
        prop_domain = {i.iri.split("#")[1]:i.iri for i in prop.domain}
        for k,v in prop_domain.items():
            if [k] in prop2_domain:
                print(Fore.GREEN + f"Match: domain '{k}' with IRI {v}")
            else:
                 print(Fore.RED + f"Mismatch: domain '{k}' with IRI {v} not found in second ontology.")



def diff_subclasses(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Subclass Relationships ===" + Style.RESET_ALL)
    class2 = {i.iri.split("#")[1]:i for i in onto2.classes()}
    for cls in onto1.classes():
        cls2 = None
        if cls.iri.split("#")[1] in class2:
            print(Fore.YELLOW+ "Matching Subclasses for class: ", cls.name, "" + Style.RESET_ALL)
            cls2 = class2[cls.iri.split("#")[1]]
        else:
            print(Fore.RED + "Mismatch Error: Cannot Match Subclasses for class: ", cls.name, ""+ Style.RESET_ALL)
            continue
        subclasses_for_cls = list(cls.subclasses())
        subclasses_for_cls_onto2 = list(cls2.subclasses())
        if len(subclasses_for_cls) == len(subclasses_for_cls_onto2) == 0:
            print(Fore.LIGHTMAGENTA_EX + "No Subclasses for either source or target file" + Style.RESET_ALL)
            continue
        subclasses_for_cls_name = sorted([i.name for i in subclasses_for_cls])
        subclasses_for_cls_onto2_name = sorted([i.name for i in subclasses_for_cls_onto2])
        if subclasses_for_cls_name != subclasses_for_cls_onto2_name:
            print(Fore.RED + "MisMatch found for subclasses. Expected: {} Found: {}".format(', '.join(subclasses_for_cls_name),', '.join(subclasses_for_cls_onto2_name)) + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Subclasses succcessfully match {} !".format(subclasses_for_cls_name))


def diff_property_ranges(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Property Ranges ===" + Style.RESET_ALL)
    onto2_props = {i.name: i for i in onto2.properties()}
    for prop in list(onto1.properties()):
        prop2 = None
        if prop.name not in onto2_props:
            print(Fore.RED + f"Mismatch: Property '{prop.name}' not found in second ontology.")
            continue
        else:
            print(Fore.YELLOW+ "Matching Ranges for Property: ", prop.name, "" + Style.RESET_ALL)
        prop2 = onto2_props[prop.name]
        prop1_range = [i.name for i in prop.range]
        prop2_range = [i.name for i in prop2.range]
        if prop1_range == prop2_range:
             print(Fore.GREEN + f"Match: Range of property '{prop.name}' : {prop1_range}")
        else:
             print(Fore.RED + f"Mismatch: Range of property '{prop.name}'. First: {prop1_range}, Second: {prop2_range}")

def diff_instances(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Class Instances ===" + Style.RESET_ALL)
    onto2_cls = {i.name: i for i in onto2.classes()}
    for cls in list(onto1.classes()):
        cls2 = None
        if cls.name not in onto2_cls:
            print(Fore.RED + f"Mismatch: Class '{cls.name}' not found in second ontology.")
            continue
        else:
            print(Fore.YELLOW + "Matching Instance for class: ", cls.name, "" + Style.RESET_ALL)
        cls2 = onto2_cls[cls.name]
        cls_instance = list(cls.instances())
        cls2_instance = list(cls2.instances())
        if cls_instance == cls2_instance == []:
            print(Fore.LIGHTMAGENTA_EX + "No Instance for either source or target file" + Style.RESET_ALL)
            continue
        if cls_instance != cls2_instance:
            print(Fore.RED + f"MisMatch found for Instances. Expected: {cls_instance} Found: {cls2_instance}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Instances succcessfully match {cls_instance} !")

def diff_subproperties(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Subproperty Relationships ===" + Style.RESET_ALL)
    onto2_props = {i.name: i for i in onto2.properties()}
    for prop in list(onto1.properties()):
        prop2 = None
        if prop.name not in onto2_props:
            print(Fore.RED + f"Mismatch: Property '{prop.name}' not found in second ontology.")
            continue
        else:
            print(Fore.YELLOW + "Matching Subproperties for Property: ", prop.name, "" + Style.RESET_ALL)
        prop2 = onto2_props[prop.name]
        prop_sub = sorted([i.name for i in list(prop.subclasses())])
        prop2_sub = sorted([i.name for i in list(prop2.subclasses())])
        if prop_sub == prop2_sub == []:
            print(Fore.LIGHTMAGENTA_EX + "No Subproperty for either source or target file" + Style.RESET_ALL)
            continue
        if prop_sub != prop2_sub:
            print(Fore.RED + f"MisMatch found for subproperties. Expected: {prop_sub} Found: {prop2_sub}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Subclasses succcessfully match {prop_sub} !")

def diff_inverse_properties(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Inverse Properties ===" + Style.RESET_ALL)
    onto2_props = {i.name: i for i in onto2.properties()}
    for prop in list(onto1.properties()):
        prop2 = None
        if prop.name not in onto2_props:
            print(Fore.RED + f"Mismatch: Property '{prop.name}' not found in second ontology.")
            continue
        else:
            print(Fore.YELLOW + "Matching Inverse Properties for Property: ", prop.name, "" + Style.RESET_ALL)
        prop2 = onto2_props[prop.name]
        inv1 = prop.inverse_property
        inv2 = prop2.inverse_property
        if (inv1 is None and inv2 is None) or (inv1 is not None and inv2 is not None and inv1.name == inv2.name):
            print(Fore.GREEN + f"Match: Inverse property of '{prop.name}'")
        else:
            print(Fore.RED + f"Mismatch: Inverse property of '{prop.name}'. First: {inv1.name if inv1 else None}, Second: {inv2.name if inv2 else None}")

def check_restriction_type(restriction, type_str):
    """Helper function to check the type of a restriction.
    For now, we check the class name.
    Note: owlready2 uses classes like AllValues, SomeValues, and Max.
    'firstrest' is left as a placeholder."""
    cls_name = restriction.__class__.__name__.lower()
    if type_str.lower() == "allvaluesfrom":
        return cls_name == "allvalues"
    elif type_str.lower() == "somevaluesfrom":
        return cls_name == "somevalues"
    elif type_str.lower() == "maxcardinality":
        # Typically the class might be named 'Max' or include a cardinality indicator.
        return "max" in cls_name
    elif type_str.lower() == "firstrest":
        # Placeholder: define the check for 'firstrest' as needed.
        return "firstrest" in cls_name
    return False

def diff_restrictions(onto1, onto2, restriction_type):
    print(Fore.BLUE + f"\n=== Comparing Restrictions: {restriction_type} ===" + Style.RESET_ALL)
    # For each class, inspect its restrictions (in the is_a list)
    onto2_cls = {i.name: i for i in onto2.classes()}
    for cls in list(onto1.classes()):
        cls2 = None
        if cls.name not in onto2_cls:
            print(Fore.RED + f"Mismatch: Class '{cls.name}' not found in second ontology.")
            continue
        else:
            print(Fore.YELLOW + f"Matching Restriction {restriction_type} for class: ", cls.name, "" + Style.RESET_ALL)
        cls2 = onto2_cls[cls.name]

        # Filter restrictions of the given type from the class axioms.
        cls_restrictions = [i.value for i in cls.is_a if isinstance(i,Restriction) if f'.{restriction_type}' in str(i)]
        cls2_restrictions = [i.value for i in cls2.is_a if isinstance(i,Restriction) if f'.{restriction_type}' in str(i)]
        # cls_res_value = [i.value for i in cls_restrictions]
        print(cls_restrictions)
        print(cls2_restrictions)

        # res1 = {str(r) for r in cls.is_a if isinstance(r, Restriction) and check_restriction_type(r, restriction_type)}
        # res2 = {str(r) for r in cls2.is_a if isinstance(r, Restriction) and check_restriction_type(r, restriction_type)}
        # print(res1)
        # print(res2)
        # if res1 == res2 == set():
        #     print(Fore.LIGHTMAGENTA_EX + "No Restriction for either source or target file" + Style.RESET_ALL)
        # if res1 == res2:
        #     print(Fore.GREEN + f"Match: {restriction_type} restrictions for class '{cls.name}'")
        # else:
        #     print(Fore.RED + f"Mismatch: {restriction_type} restrictions for class '{cls.name}'.")
        #     print(Fore.YELLOW + f"  In first: {res1}")
        #     print(Fore.YELLOW + f"  In second: {res2}")

def diff_prefixiri(onto1, onto2):
    print(Fore.BLUE + "\n=== Comparing Ontology Prefix IRI ===" + Style.RESET_ALL)
    prefix1 = onto1.base_iri
    prefix2 = onto2.base_iri
    print(prefix1, prefix2)
    if prefix1 == prefix2:
        print(Fore.GREEN + f"Match: Prefix IRI '{prefix1}'")
    else:
        print(Fore.RED + f"Mismatch: Ontology prefixes differ. First: '{prefix1}', Second: '{prefix2}'")

def main():


    print(Fore.CYAN + "Loading ontologies...")
    onto1 = load_ontology("go.owl")
    onto2 = load_ontology("go_generated.owl")
    # # Compare different aspects of the ontologies.
    # #
    diff_classes(onto1, onto2)
    diff_property_domains(onto1, onto2)
    diff_subclasses(onto1, onto2)
    diff_property_ranges(onto1, onto2)
    diff_instances(onto1, onto2)
    diff_subproperties(onto1, onto2)
    diff_inverse_properties(onto1, onto2)
    # print(list(onto1.classes()))
    # print(list(onto2.classes()))
    # print([i.name for i in list(onto1.classes())])

    # Compare restrictions: allValuesFrom, someValuesFrom, maxCardinality, firstrest.
    # for r_type in ["all", "some", "max", "only"]:
    #     diff_restrictions(onto1, onto2, r_type)

if __name__ == '__main__':
    main()
