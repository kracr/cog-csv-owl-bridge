# import pandas as pd
# from owlready2 import *
#
#
# def resolve_uri(value, iri_dict, onto):
#     """Resolves a prefixed URI or blank node to a full URI or Ontology entity."""
#     if ':' in value:
#         prefix, local_name = value.split(':', 1)
#         if prefix in iri_dict:
#             return iri_dict[prefix] + local_name
#     return iri_dict.get('ns1', '') + value
#
#
# def process_owl_class(owlclass, onto, iri_dict):
#     for class_name in owlclass.iloc[:, 0].values:
#         if "https" not in class_name:
#             continue
#         class_uri = resolve_uri(class_name, iri_dict, onto)
#         with onto:
#             types.new_class(class_uri.split('#')[-1], (Thing,))
#
#
# def process_subclass(subclass, onto, iri_dict):
#     for class_name, parent_name in zip(subclass.iloc[:, 0].values, subclass.iloc[:, 1].values):
#         class_uri = resolve_uri(class_name, iri_dict, onto)
#         parent_uri = resolve_uri(parent_name, iri_dict, onto)
#         with onto:
#             child_cls = types.new_class(class_uri.split('#')[-1], (Thing,))
#             parent_cls = types.new_class(parent_uri.split('#')[-1], (Thing,))
#             child_cls.is_a.append(parent_cls)
#
#
# def process_domain(domain_axiom, onto, iri_dict):
#     for obj_name, domain_name in zip(domain_axiom.iloc[:, 0].values, domain_axiom.iloc[:, 1].values):
#         obj_uri = resolve_uri(obj_name, iri_dict, onto)
#         domain_uri = resolve_uri(domain_name, iri_dict, onto)
#         with onto:
#             prop = types.new_class(obj_uri.split('#')[-1], (ObjectProperty,))
#             domain_cls = types.new_class(domain_uri.split('#')[-1], (Thing,))
#             prop.domain.append(domain_cls)
#
#
# def process_range(range_axiom, onto, iri_dict):
#     for obj_name, range_name in zip(range_axiom.iloc[:, 0].values, range_axiom.iloc[:, 1].values):
#         obj_uri = resolve_uri(obj_name, iri_dict, onto)
#         range_uri = resolve_uri(range_name, iri_dict, onto)
#         with onto:
#             prop = types.new_class(obj_uri.split('#')[-1], (ObjectProperty,))
#             range_cls = types.new_class(range_uri.split('#')[-1], (Thing,))
#             prop.range.append(range_cls)
#
#
# def process_instances(instances, onto, iri_dict):
#     for instance_name, class_name in zip(instances.iloc[:, 0].values, instances.iloc[:, 1].values):
#         instance_uri = resolve_uri(instance_name, iri_dict, onto)
#         class_uri = resolve_uri(class_name, iri_dict, onto)
#         with onto:
#             instance_cls = types.new_class(class_uri.split('#')[-1], (Thing,))
#             instance_cls(instance_uri.split('#')[-1])
#
#
# def csv_owl_final(subclass, domain_axiom, range_axiom, instances, owlclass, onto):
#     process_owl_class(owlclass, onto, iri_dict)
#     process_subclass(subclass, onto, iri_dict)
#     process_domain(domain_axiom, onto, iri_dict)
#     process_range(range_axiom, onto, iri_dict)
#     process_instances(instances, onto, iri_dict)
#     onto.save(file="output_3.owl", format="rdfxml")
#
#
# def main(file):
#     onto = get_ontology("http://www.semanticweb.org/ontology#")
#
#     owlclass = pd.read_excel(file, sheet_name='owlclass')
#     subclass = pd.read_excel(file, sheet_name='subclass')
#     domain_axiom = pd.read_excel(file, sheet_name='domain')
#     range_axiom = pd.read_excel(file, sheet_name='range')
#     instances = pd.read_excel(file, sheet_name='instances')
#
#     iri = pd.read_excel(file, sheet_name='prefixiri')
#     global iri_dict
#     iri_dict = {row[0]: row[1] for _, row in iri.iterrows()}
#
#     with onto:
#         csv_owl_final(subclass, domain_axiom, range_axiom, instances, owlclass, onto)
#
#     print("Ontology saved to output.owl")
#
# main('go.xlsx')


import pandas as pd
from owlready2 import *


def resolve_uri(value, iri_dict, onto):
    """Resolves a prefixed URI or blank node to a full URI or Ontology entity."""
    if ':' in value:
        prefix, local_name = value.split(':', 1)
        if prefix in iri_dict:
            return iri_dict[prefix] + local_name
    return iri_dict.get('ns1', '') + value


def process_owl_class(owlclass, onto, iri_dict):
    for class_name in owlclass.iloc[:, 0].values:
        if class_name is not pd.NA and "https" not in class_name:
            continue
        class_uri = resolve_uri(class_name, iri_dict, onto)
        with onto:
            # Create class using the part after the '#' as a name
            types.new_class(class_uri.split('#')[-1], (Thing,))


def process_subclass(subclass, onto, iri_dict):
    for class_name, parent_name in zip(subclass.iloc[:, 0].values, subclass.iloc[:, 1].values):
        class_uri = resolve_uri(class_name, iri_dict, onto)
        parent_uri = resolve_uri(parent_name, iri_dict, onto)
        with onto:
            child_cls = types.new_class(class_uri.split('#')[-1], (Thing,))
            parent_cls = types.new_class(parent_uri.split('#')[-1], (Thing,))
            child_cls.is_a.append(parent_cls)


def process_domain(domain_axiom, onto, iri_dict):
    for obj_name, domain_name in zip(domain_axiom.iloc[:, 0].values, domain_axiom.iloc[:, 1].values):
        obj_uri = resolve_uri(obj_name, iri_dict, onto)
        domain_uri = resolve_uri(domain_name, iri_dict, onto)
        with onto:
            prop = types.new_class(obj_uri.split('#')[-1], (ObjectProperty,))
            domain_cls = types.new_class(domain_uri.split('#')[-1], (Thing,))
            prop.domain.append(domain_cls)


def process_range(range_axiom, onto, iri_dict):
    for obj_name, range_name in zip(range_axiom.iloc[:, 0].values, range_axiom.iloc[:, 1].values):
        obj_uri = resolve_uri(obj_name, iri_dict, onto)
        range_uri = resolve_uri(range_name, iri_dict, onto)
        with onto:
            prop = types.new_class(obj_uri.split('#')[-1], (ObjectProperty,))
            range_cls = types.new_class(range_uri.split('#')[-1], (Thing,))
            prop.range.append(range_cls)


def process_instances(instances, onto, iri_dict):
    for instance_name, class_name in zip(instances.iloc[:, 0].values, instances.iloc[:, 1].values):
        instance_uri = resolve_uri(instance_name, iri_dict, onto)
        class_uri = resolve_uri(class_name, iri_dict, onto)
        with onto:
            instance_cls = types.new_class(class_uri.split('#')[-1], (Thing,))
            # Create an individual (instance) of the given class.
            instance_cls(instance_uri.split('#')[-1])


def process_subproperty(subproperty_axiom, onto, iri_dict):
    """Process subproperty axioms. Expects two columns: subproperty and its superproperty."""
    for prop_name, super_prop in zip(subproperty_axiom.iloc[:, 0].values, subproperty_axiom.iloc[:, 1].values):
        prop_uri = resolve_uri(prop_name, iri_dict, onto)
        sup_uri = resolve_uri(super_prop, iri_dict, onto)
        with onto:
            sub_prop = types.new_class(prop_uri.split('#')[-1], (ObjectProperty,))
            sup_prop = types.new_class(sup_uri.split('#')[-1], (ObjectProperty,))
            sub_prop.is_a.append(sup_prop)


def process_inverseof(inverse_axiom, onto, iri_dict):
    """Process inverseOf axioms. Expects two columns: a property and its inverse."""
    for prop1, prop2 in zip(inverse_axiom.iloc[:, 0].values, inverse_axiom.iloc[:, 1].values):
        uri1 = resolve_uri(prop1, iri_dict, onto)
        uri2 = resolve_uri(prop2, iri_dict, onto)
        with onto:
            p1 = types.new_class(uri1.split('#')[-1], (ObjectProperty,))
            p2 = types.new_class(uri2.split('#')[-1], (ObjectProperty,))
            p1.inverse_property = p2


def process_allvaluesfrom(allvaluesfrom_axiom, onto, iri_dict):
    """
    Process allValuesFrom axioms.
    Expects three columns: subject class, property, and filler class.
    Creates a universal (only) restriction on the subject class.
    """
    for subject, prop, filler in zip(allvaluesfrom_axiom.iloc[:, 0].values,
                                      allvaluesfrom_axiom.iloc[:, 1].values,
                                      allvaluesfrom_axiom.iloc[:, 2].values):
        subject_uri = resolve_uri(subject, iri_dict, onto)
        prop_uri = resolve_uri(prop, iri_dict, onto)
        filler_uri = resolve_uri(filler, iri_dict, onto)
        with onto:
            subj_cls = types.new_class(subject_uri.split('#')[-1], (Thing,))
            prop_obj = types.new_class(prop_uri.split('#')[-1], (ObjectProperty,))
            filler_cls = types.new_class(filler_uri.split('#')[-1], (Thing,))
            restriction = prop_obj.only(filler_cls)
            subj_cls.is_a.append(restriction)


def process_somevaluesfrom(somevaluesfrom_axiom, onto, iri_dict):
    """
    Process someValuesFrom axioms.
    Expects three columns: subject class, property, and filler class.
    Creates an existential (some) restriction on the subject class.
    """
    for subject, prop, filler in zip(somevaluesfrom_axiom.iloc[:, 0].values,
                                      somevaluesfrom_axiom.iloc[:, 1].values,
                                      somevaluesfrom_axiom.iloc[:, 2].values):
        subject_uri = resolve_uri(subject, iri_dict, onto)
        prop_uri = resolve_uri(prop, iri_dict, onto)
        filler_uri = resolve_uri(filler, iri_dict, onto)
        with onto:
            subj_cls = types.new_class(subject_uri.split('#')[-1], (Thing,))
            prop_obj = types.new_class(prop_uri.split('#')[-1], (ObjectProperty,))
            filler_cls = types.new_class(filler_uri.split('#')[-1], (Thing,))
            restriction = prop_obj.some(filler_cls)
            subj_cls.is_a.append(restriction)


def process_maxcardinality(maxcardinality_axiom, onto, iri_dict):
    """
    Process maxCardinality axioms.
    Expects four columns: subject class, property, cardinality (number), and filler class.
    Adds a max cardinality restriction to the subject class.
    """
    for subject, prop, card, filler in zip(maxcardinality_axiom.iloc[:, 0].values,
                                            maxcardinality_axiom.iloc[:, 1].values,
                                            maxcardinality_axiom.iloc[:, 2].values,
                                            maxcardinality_axiom.iloc[:, 3].values):
        subject_uri = resolve_uri(subject, iri_dict, onto)
        prop_uri = resolve_uri(prop, iri_dict, onto)
        filler_uri = resolve_uri(filler, iri_dict, onto)
        with onto:
            subj_cls = types.new_class(subject_uri.split('#')[-1], (Thing,))
            prop_obj = types.new_class(prop_uri.split('#')[-1], (ObjectProperty,))
            filler_cls = types.new_class(filler_uri.split('#')[-1], (Thing,))
            try:
                card_int = int(card)
            except ValueError:
                continue  # skip or handle error if cardinality is not numeric
            restriction = prop_obj.max(card_int, filler_cls)
            subj_cls.is_a.append(restriction)




def csv_owl_final(subclass, domain_axiom, range_axiom, owlclass,
                  subproperty_axiom, inverse_axiom, allvaluesfrom_axiom, somevaluesfrom_axiom,
                   onto):
    process_owl_class(owlclass, onto, iri_dict)
    process_subclass(subclass, onto, iri_dict)
    process_domain(domain_axiom, onto, iri_dict)
    process_range(range_axiom, onto, iri_dict)
    # process_instances(instances, onto, iri_dict)
    process_subproperty(subproperty_axiom, onto, iri_dict)
    process_inverseof(inverse_axiom, onto, iri_dict)
    process_allvaluesfrom(allvaluesfrom_axiom, onto, iri_dict)
    process_somevaluesfrom(somevaluesfrom_axiom, onto, iri_dict)
    # process_maxcardinality(maxcardinality_axiom, onto, iri_dict)
    print("here")
    onto.save(file="output_3.owl", format="rdfxml")


def main(file):
    onto = get_ontology(f"https://raw.githubusercontent.com/{file}.owl#")

    # Read required sheets
    owlclass = pd.read_excel(file, sheet_name='owlclass').dropna()
    subclass = pd.read_excel(file, sheet_name='subclass').dropna()
    domain_axiom = pd.read_excel(file, sheet_name='domain').dropna()
    range_axiom = pd.read_excel(file, sheet_name='range').dropna()
    # instances = pd.read_excel(file, sheet_name='instances')

    # Read sheets for additional axioms
    subproperty_axiom = pd.read_excel(file, sheet_name='subproperty').dropna()
    inverse_axiom = pd.read_excel(file, sheet_name='inverseOf').dropna()
    allvaluesfrom_axiom = pd.read_excel(file, sheet_name='allvaluesfrom').dropna()
    somevaluesfrom_axiom = pd.read_excel(file, sheet_name='somevaluesfrom').dropna()
    # # maxcardinality_axiom = pd.read_excel(file, sheet_name='maxcardinality')
    # # firstrest_axiom = pd.read_excel(file, sheet_name='firstrest')
    # #
    iri = pd.read_excel(file, sheet_name='prefixiri')
    global iri_dict
    iri_dict = {row[0]: row[1] for _, row in iri.iterrows()}

    with onto:
        csv_owl_final(subclass, domain_axiom, range_axiom, owlclass,
                      subproperty_axiom, inverse_axiom, allvaluesfrom_axiom, somevaluesfrom_axiom,
                      onto)

    print("Ontology saved to output_3.owl")


if __name__ == "__main__":
    main('go.xlsx')
