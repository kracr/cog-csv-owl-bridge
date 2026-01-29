# #!/usr/bin/env python3
# """
# Compare two OWL files (original normalized ontology vs converted OWL)
# and report:
#  - total axiom counts (by type)
#  - missing axioms (in original but not in converted)
#  - additional axioms (in converted but not in original)

# Usage:
#     python compare_owl_axioms.py original.owl converted.owl
# """

# from rdflib import Graph, URIRef, BNode, RDF, RDFS, OWL, Literal
# from rdflib.collection import Collection
# import sys
# import itertools

# def qname_or_str(node):
#     """Return readable representation of a node (URIRefs as full URI, BNodes labelled)."""
#     if isinstance(node, URIRef):
#         return str(node)
#     if isinstance(node, BNode):
#         return f"_:{str(node)}"
#     if isinstance(node, Literal):
#         return f"\"{str(node)}\"^^{node.datatype}" if node.datatype else f"\"{str(node)}\""
#     return str(node)

# def normalize_restriction(g, bnode):
#     """If bnode is an owl:Restriction, return a normalized textual form: (Restriction on P some/all C)."""
#     if (bnode, RDF.type, OWL.Restriction) not in g:
#         return None
#     onp = g.value(bnode, OWL.onProperty)
#     some = g.value(bnode, OWL.someValuesFrom)
#     allv = g.value(bnode, OWL.allValuesFrom)
#     parts = []
#     if onp is not None:
#         parts.append(f"onProperty={qname_or_str(onp)}")
#     if some is not None:
#         parts.append(f"someValuesFrom={qname_or_str(some)}")
#     if allv is not None:
#         parts.append(f"allValuesFrom={qname_or_str(allv)}")
#     return "Restriction(" + ",".join(parts) + ")"

# def normalize_intersection(g, bnode):
#     """If bnode has owl:intersectionOf, return normalized form listing members."""
#     coll = g.value(bnode, OWL.intersectionOf)
#     if coll is None:
#         return None
#     try:
#         items = list(Collection(g, coll))
#     except Exception:
#         # fallback: try to follow rdf:first / rdf:rest
#         items = []
#         cur = coll
#         while cur and cur != RDF.nil:
#             first = g.value(cur, RDF.first)
#             if first is not None:
#                 items.append(first)
#             cur = g.value(cur, RDF.rest)
#     return "Intersection(" + " & ".join(qname_or_str(i) for i in items) + ")"

# def extract_axioms(g):
#     """
#     Build a set of canonical textual axiom representations from graph g.
#     Returns a dict: { 'all': set(all_axioms), 'by_type': {type:set(...) } }
#     """
#     axioms = set()
#     by_type = {}

#     def add(t, s):
#         axioms.add(s)
#         by_type.setdefault(t, set()).add(s)

#     # Class declarations (named)
#     for s in set(g.subjects(RDF.type, OWL.Class)):
#         if isinstance(s, URIRef):
#             add('Class', f"Class({qname_or_str(s)})")

#     # Named individuals (rdf:type NamedIndividual or type some class)
#     for s in set(g.subjects(RDF.type, OWL.NamedIndividual)):
#         add('NamedIndividual', f"NamedIndividual({qname_or_str(s)})")
#         # also their types (rdf:type A) included below if present

#     # rdf:type triples that are A rdf:type C for individuals
#     for s, o in g.subject_objects(RDF.type):
#         if isinstance(s, URIRef) and isinstance(o, URIRef):
#             # but skip built-in OWL class declarations (we already have those)
#             if o != OWL.Class and o != OWL.ObjectProperty and o != OWL.DatatypeProperty and o != OWL.Ontology:
#                 add('TypeAssertion', f"Type({qname_or_str(s)} , {qname_or_str(o)})")

#     # Subclass axioms: handle both named and anonymous superclasses/restrictions/intersections
#     for s, o in g.subject_objects(RDFS.subClassOf):
#         subj_repr = qname_or_str(s) if not isinstance(s, BNode) else normalize_intersection(g, s) or normalize_restriction(g,s) or qname_or_str(s)
#         # object might be URIRef or BNode (restriction or intersection)
#         if isinstance(o, URIRef):
#             add('SubClassOf', f"SubClassOf({qname_or_str(s)} , {qname_or_str(o)})")
#         elif isinstance(o, BNode):
#             # restriction?
#             restr = normalize_restriction(g, o)
#             if restr:
#                 add('SubClassOf', f"SubClassOf({qname_or_str(s)} , {restr})")
#             else:
#                 inter = normalize_intersection(g, o)
#                 if inter:
#                     add('SubClassOf', f"SubClassOf({qname_or_str(s)} , {inter})")
#                 else:
#                     # generic bnode
#                     add('SubClassOf', f"SubClassOf({qname_or_str(s)} , {qname_or_str(o)})")

#     # Also handle rows where subclass is a BNode (GCI intersection or restriction) like _:x rdf:type owl:Restriction ; rdfs:subClassOf C
#     # These will appear via earlier loop if their (bnode, rdfs:subClassOf, C) triple exists.
#     for s, p, o in g.triples((None, RDFS.subClassOf, None)):
#         # already covered above by subject_objects, so we skip duplicate processing

#         pass

#     # ObjectProperty declarations
#     for s in set(g.subjects(RDF.type, OWL.ObjectProperty)):
#         if isinstance(s, URIRef):
#             add('ObjectProperty', f"ObjectProperty({qname_or_str(s)})")

#     # subPropertyOf
#     for s, o in g.subject_objects(RDFS.subPropertyOf):
#         add('SubPropertyOf', f"SubPropertyOf({qname_or_str(s)} , {qname_or_str(o)})")

#     # propertyChainAxiom (superproperty owl:propertyChainAxiom ( rdf:List ) )
#     for superprop, _, listnode in g.triples((None, OWL.propertyChainAxiom, None)):
#         try:
#             members = list(Collection(g, listnode))
#             chain = " o ".join(qname_or_str(m) for m in members)
#             add('PropertyChain', f"PropertyChain({qname_or_str(superprop)} := {chain})")
#         except Exception:
#             # fallback: attempt to enumerate rdf:first / rest
#             items = []
#             cur = listnode
#             while cur and cur != RDF.nil:
#                 f = g.value(cur, RDF.first)
#                 if f is not None:
#                     items.append(f)
#                 cur = g.value(cur, RDF.rest)
#             chain = " o ".join(qname_or_str(m) for m in items)
#             add('PropertyChain', f"PropertyChain({qname_or_str(superprop)} := {chain})")

#     # domain / range
#     for s, o in g.subject_objects(RDFS.domain):
#         add('Domain', f"Domain({qname_or_str(s)} , {qname_or_str(o)})")
#     for s, o in g.subject_objects(RDFS.range):
#         add('Range', f"Range({qname_or_str(s)} , {qname_or_str(o)})")

#     # inverseOf
#     for s, o in g.subject_objects(OWL.inverseOf):
#         # canonicalize pair ordering so A inverseOf B equals B inverseOf A
#         pair = tuple(sorted([str(s), str(o)]))
#         add('InverseOf', f"InverseOf({pair[0]} , {pair[1]})")

#     # Max cardinality (simple detection: owl:maxCardinality triple on some blank node or class)
#     for s, p, o in g.triples((None, OWL.maxCardinality, None)):
#         # Need to find the class/subject and onProperty for context; best-effort format
#         onp = g.value(s, OWL.onProperty)
#         add('MaxCardinality', f"MaxCardinality(subject={qname_or_str(s)}, onProperty={qname_or_str(onp)}, value={qname_or_str(o)})")

#     return {'all': axioms, 'by_type': by_type}

# def compare_graphs(original_path, converted_path, verbose=True):
#     g1 = Graph()
#     g2 = Graph()
#     g1.parse(original_path, format='xml')
#     g2.parse(converted_path, format='xml')

#     A = extract_axioms(g1)
#     B = extract_axioms(g2)

#     set1 = A['all']
#     set2 = B['all']

#     missing = set1 - set2   # present in original, missing in converted
#     additional = set2 - set1  # present in converted but not original
#     common = set1 & set2

#     # counts per type
#     def counts(by_type):
#         return {k: len(v) for k, v in by_type.items()}

#     print("=== SUMMARY ===")
#     print(f"Original: {len(set1)} extracted axioms; Converted: {len(set2)} extracted axioms; Intersection: {len(common)}")
#     print("\nCounts by axiom type (original):")
#     for t, c in counts(A['by_type']).items():
#         print(f"  {t}: {c}")
#     print("\nCounts by axiom type (converted):")
#     for t, c in counts(B['by_type']).items():
#         print(f"  {t}: {c}")

#     print("\n=== MISSING AXIOMS (in ORIGINAL but NOT in CONVERTED) ===")
#     print(f"Count: {len(missing)}")
#     if missing:
#         for i, ax in enumerate(sorted(missing), 1):
#             print(f"{i}. {ax}")

#     print("\n=== ADDITIONAL AXIOMS (in CONVERTED but NOT in ORIGINAL) ===")
#     print(f"Count: {len(additional)}")
#     if additional:
#         for i, ax in enumerate(sorted(additional), 1):
#             print(f"{i}. {ax}")

#     return {
#         'original_count': len(set1),
#         'converted_count': len(set2),
#         'common_count': len(common),
#         'missing': missing,
#         'additional': additional
#     }

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python compare_owl_axioms.py original.owl converted.owl")
#         sys.exit(1)
#     orig = sys.argv[1]
#     conv = sys.argv[2]
#     res = compare_graphs(orig, conv)


#!/usr/bin/env python3
"""
Compare two OWL files (original normalized ontology vs converted OWL)
and report:

 - total axiom counts (by type)
 - missing axioms (in original but not in converted)
 - additional axioms (in converted but not in original)

Extended to validate correctness of:
  * Domain axioms
  * Range axioms
  * SubPropertyOf axioms
  * InverseOf axioms

Usage:
    python compare_owl_axioms.py original.owl converted.owl
"""

from rdflib import Graph, URIRef, BNode, RDF, RDFS, OWL, Literal
from rdflib.collection import Collection
import sys

def qname_or_str(node):
    if isinstance(node, URIRef):
        return str(node)
    if isinstance(node, BNode):
        return f"_:{str(node)}"
    if isinstance(node, Literal):
        return f"\"{node}\"^^{node.datatype}" if node.datatype else f"\"{node}\""
    return str(node)

def canonical_axiom(s):
    """Normalize whitespace so string comparison is reliable."""
    return " ".join(s.split())

# ========== Extract canonical axioms ==========

def extract_axioms(g):
    axioms = set()
    by_type = {}

    def add(t, s):
        ax = canonical_axiom(s)
        axioms.add(ax)
        by_type.setdefault(t, set()).add(ax)

    # ---- Class declarations ----
    for s in set(g.subjects(RDF.type, OWL.Class)):
        if isinstance(s, URIRef):
            add("Class", f"Class({qname_or_str(s)})")

    # ---- ObjectProperty declarations ----
    for s in set(g.subjects(RDF.type, OWL.ObjectProperty)):
        add("ObjectProperty", f"ObjectProperty({qname_or_str(s)})")

    # ---- SubPropertyOf ----
    for s, o in g.subject_objects(RDFS.subPropertyOf):
        add("SubPropertyOf", f"SubPropertyOf({qname_or_str(s)}, {qname_or_str(o)})")

    # ---- Domain ----
    for s, o in g.subject_objects(RDFS.domain):
        add("Domain", f"Domain({qname_or_str(s)}, {qname_or_str(o)})")

    # ---- Range ----
    for s, o in g.subject_objects(RDFS.range):
        add("Range", f"Range({qname_or_str(s)}, {qname_or_str(o)})")

    # ---- InverseOf ----
    for s, o in g.subject_objects(OWL.inverseOf):
        ordered = tuple(sorted([qname_or_str(s), qname_or_str(o)]))
        add("InverseOf", f"InverseOf({ordered[0]}, {ordered[1]})")

    # ---- SubClassOf ----
    for s, o in g.subject_objects(RDFS.subClassOf):
        # named superclass
        if isinstance(o, URIRef):
            add("SubClassOf", f"SubClassOf({qname_or_str(s)}, {qname_or_str(o)})")
        else:
            # restriction or intersection
            restr = normalize_restriction(g, o)
            if restr:
                add("SubClassOf", f"SubClassOf({qname_or_str(s)}, {restr})")
            else:
                inter = normalize_intersection(g, o)
                if inter:
                    add("SubClassOf", f"SubClassOf({qname_or_str(s)}, {inter})")
                else:
                    add("SubClassOf", f"SubClassOf({qname_or_str(s)}, {qname_or_str(o)})")

    return {"all": axioms, "by_type": by_type}

# ========== Restriction & intersection helpers ==========

def normalize_restriction(g, bnode):
    if (bnode, RDF.type, OWL.Restriction) not in g:
        return None
    onp = g.value(bnode, OWL.onProperty)
    some = g.value(bnode, OWL.someValuesFrom)
    allv = g.value(bnode, OWL.allValuesFrom)

    parts = []
    if onp:
        parts.append(f"onProperty={qname_or_str(onp)}")
    if some:
        parts.append(f"someValuesFrom={qname_or_str(some)}")
    if allv:
        parts.append(f"allValuesFrom={qname_or_str(allv)}")

    return "Restriction(" + ",".join(parts) + ")"

def normalize_intersection(g, bnode):
    coll = g.value(bnode, OWL.intersectionOf)
    if coll is None:
        return None
    try:
        items = list(Collection(g, coll))
    except:
        items = []
        cur = coll
        while cur and cur != RDF.nil:
            f = g.value(cur, RDF.first)
            if f:
                items.append(f)
            cur = g.value(cur, RDF.rest)
    return "Intersection(" + " & ".join(qname_or_str(i) for i in items) + ")"

# ========== Comparison ==========

def compare_graphs(original_path, converted_path):
    g1 = Graph()
    g2 = Graph()

    g1.parse(original_path)
    g2.parse(converted_path)

    A = extract_axioms(g1)
    B = extract_axioms(g2)

    set1 = A["all"]
    set2 = B["all"]

    missing = set1 - set2
    additional = set2 - set1

    print("\n===============================")
    print("       AXIOM COMPARISON        ")
    print("===============================\n")
    print(f"Original axioms:  {len(set1)}")
    print(f"Converted axioms: {len(set2)}")
    print(f"Common axioms:    {len(set1 & set2)}")

    # ---- per type correctness ----
    print("\n---------------------------------")
    print(" Checking domain/range/subprop/inverse")
    print("---------------------------------\n")

    CHECK_TYPES = ["Domain", "Range", "SubPropertyOf", "InverseOf"]

    for t in CHECK_TYPES:
        orig = A["by_type"].get(t, set())
        conv = B["by_type"].get(t, set())
        miss = orig - conv
        add = conv - orig

        print(f"\n### {t} ###")
        print(f"Original count:   {len(orig)}")
        print(f"Converted count:  {len(conv)}")
        print(f"Missing:          {len(miss)}")
        print(f"Additional:       {len(add)}")

        if miss:
            print("\nMissing axioms:")
            for m in sorted(miss):
                print("   ", m)
        if add:
            print("\nAdditional axioms:")
            for a in sorted(add):
                print("   ", a)

    # ----- global missing/additional -----
    print("\n===============================")
    print(" Missing axioms (global)")
    print("===============================")
    for ax in sorted(missing):
        print(ax)

    print("\n===============================")
    print(" Additional axioms (global)")
    print("===============================")
    for ax in sorted(additional):
        print(ax)

# ========== MAIN ==========

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_owl_axioms.py original.owl converted.owl")
        sys.exit(1)

    compare_graphs(sys.argv[1], sys.argv[2])
