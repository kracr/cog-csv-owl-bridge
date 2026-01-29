# csv_owl_code.py
"""
CSV -> OWL converter (fixed prefix handling + no duplicate axioms + minimal declarations)

This version unpacks (prefix_map, xml_base) returned by load_prefixes at each call site.
"""

import csv
import pandas as pd
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from typing import Dict, Optional

# --------------------- Helpers ---------------------

def normalize_ns_for_join(ns: str) -> str:
    if ns is None:
        return ""
    return str(ns).strip()

from rdflib import Graph, Namespace

# --- load_prefixes: returns (prefix_map, xml_base) and prints debug including xml:base ---
def load_prefixes(prefix_file: str):
    """
    Reads a CSV of prefixes. Expected rows: prefix, namespace
    Returns (prefix_map, xml_base) where xml_base is the value for xml:base if present.
    """
    prefix_map = {}
    xml_base = None
    try:
        import csv
        with open(prefix_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = [r for r in reader if any(cell.strip() for cell in r)]
            if not rows:
                return prefix_map, xml_base

            # detect header heuristics (prefix, namespace)
            first = rows[0]
            data_rows = rows
            if len(first) >= 2 and first[0].strip().lower() in ('prefix', 'pref') and first[1].strip().lower() in ('namespace', 'ns', 'iri'):
                data_rows = rows[1:]

            for r in data_rows:
                if len(r) < 2:
                    continue
                raw_pref = r[0].strip()
                raw_ns = r[1].strip()
                if raw_pref.lower() == 'xml:base':
                    xml_base = raw_ns
                else:
                    # normalize the default marker to empty string key
                    if raw_pref in ("", ":", "default"):
                        key = ""
                    else:
                        key = raw_pref
                    prefix_map[key] = raw_ns
    except FileNotFoundError:
        print(f"[WARN] Prefix file '{prefix_file}' not found.")
    except Exception as e:
        print(f"[ERROR] Error reading prefix file '{prefix_file}': {e}")

    # debug printing: include xml:base in count display so terminal shows what you expect
    total_count = len(prefix_map) + (1 if xml_base else 0)
    print(f"[DEBUG] Loaded prefixes (count={total_count}):")
    for k, v in prefix_map.items():
        display_k = ':' if k == '' else k
        print(f"    prefix='{display_k}' -> '{v}'")
    if xml_base:
        print(f"    prefix='xml:base' -> '{xml_base}'")
        print(f"[DEBUG] xml:base = '{xml_base}'")
    return prefix_map, xml_base


# --- bind prefixes to rdflib Graph (normalize bind names to legal tokens) ---
# def _bind_prefixes_to_graph(g: Graph, prefixes_map):
#     """
#     Bind prefixes to rdflib Graph. prefixes_map keys may include empty string for default prefix.
#     rdflib.bind allows an empty string to denote the default prefix. However it does not accept ':'.
#     This function maps ':'/illegal tokens into a safe name for binding but preserves the mapping
#     semantics by using the original namespace.
#     """
#     for prefix_key, ns in prefixes_map.items():
#         try:
#             bind_name = prefix_key
#             # rdflib.bind expects a token without colon; convert ":" to empty default,
#             # and any other illegal characters to underscores.
#             if bind_name == "":
#                 # default namespace binding uses an empty string as prefix
#                 g.bind('', Namespace(ns))
#             else:
#                 # create a safe prefix token for rdflib binding
#                 safe = bind_name.replace(':', '_').replace(' ', '_')
#                 # ensure non-empty safe token
#                 if not safe:
#                     safe = 'ns'
#                 g.bind(safe, Namespace(ns))
#         except Exception as e:
#             print(f"[WARN] Could not bind prefix '{prefix_key}' -> '{ns}': {e}")

from rdflib import Graph, Namespace

def _bind_prefixes_to_graph(g: Graph, prefixes_map):
    """
    Bind prefixes to rdflib Graph. prefixes_map keys may include empty string for default prefix.
    rdflib.bind allows an empty string to denote the default prefix. However it does not accept ':'.
    This function maps ':'/illegal tokens into a safe name for binding but preserves the mapping
    semantics by using the original namespace.
    """
    bound_count = 0
    print("[INFO] Number of items in prefix map:", len(prefixes_map))
    for prefix_key, ns in prefixes_map.items():
        try:
            bind_name = prefix_key
            # rdflib.bind expects a token without colon; convert ":" to empty default,
            # and any other illegal characters to underscores.
            if bind_name == "":
                # default namespace binding uses an empty string as prefix
                bound_count +=1
                g.bind('', Namespace(ns))
            else:
                # create a safe prefix token for rdflib binding
                safe = bind_name.replace(':', '_').replace(' ', '_')
                # ensure non-empty safe token
                if not safe:
                    safe = 'ns'
                bound_count +=1
                g.bind(safe, Namespace(ns))
            # bound_count += 1
        except Exception as e:
            print(f"[WARN] Could not bind prefix '{prefix_key}' -> '{ns}': {e}")

    print(f"[INFO] Successfully bound {bound_count} prefixes.")
    return bound_count


from rdflib import URIRef, RDF, RDFS, Namespace

def combine_owl_files(owl_files, output_file="combined.owl", prefix_file="prefixiri.csv", force_prefix_usage=True):
    """
    Parse all partial OWL files into a merged graph, bind prefixes from prefix_file,
    optionally add a tiny dummy triple per prefix to force rdflib to keep unused prefixes,
    then serialize to output_file (passing xml:base if present).
    """
    merged_graph = Graph()

    # parse all parts
    for file in owl_files:
        try:
            merged_graph.parse(file, format="xml")
            print(f"[INFO] Parsed {file}")
        except Exception as e:
            print(f"[ERROR] Failed to parse {file}: {e}")

    # load prefixes and xml:base from CSV (uses your load_prefixes function)
    prefixes, xml_base = load_prefixes(prefix_file)

    # bind prefixes to the merged graph (uses your _bind_prefixes_to_graph)
    _bind_prefixes_to_graph(merged_graph, prefixes)

    # Optionally add a tiny declaration triple per namespace to force inclusion
    # of that namespace in the serialized RDF/XML header even if otherwise unused.
    # This creates a synthetic URI <ns>#_prefix_decl (or /_prefix_decl) and declares it as rdfs:Resource.
    if force_prefix_usage:
        for pref_key, ns in prefixes.items():
            try:
                if not ns:
                    continue
                ns_norm = str(ns)
                # choose a safe local name
                if ns_norm.endswith(('#', '/')):
                    dummy_uri = URIRef(ns_norm + "_prefix_decl")
                else:
                    dummy_uri = URIRef(ns_norm + "#_prefix_decl")
                # Add only if not already present (avoid duplicates)
                if (dummy_uri, None, None) not in merged_graph:
                    merged_graph.add((dummy_uri, RDF.type, RDFS.Resource))
            except Exception as e:
                print(f"[WARN] Could not add dummy declaration for prefix '{pref_key}' -> '{ns}': {e}")

    # serialize, pass xml:base to have xml:base attribute in RDF/XML header if provided
    try:
        # if xml_base:
        #     merged_graph.serialize(destination=output_file, format='xml', base=xml_base)
        #     merged_graph.serialize(destination=output_file, format='turtle', base=xml_base)
        # else:
        #     merged_graph.serialize(destination=output_file, format='xml')
        #     merged_graph.serialize(destination=output_file, format='turtle')
        base_arg = xml_base or None
        merged_graph.serialize(destination=output_file, format='xml', base=base_arg)
        # merged_graph.serialize(destination=output_file, format='turtle', base=base_arg)

        print(f"\n✅ Combined OWL written to {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to serialize combined graph: {e}")


def resolve_uri(name: Optional[str], prefixes: Dict[str, str]) -> Optional[URIRef]:
    if name is None:
        return None
    text = str(name).strip()
    if not text:
        return None
    if text.startswith("http://") or text.startswith("https://"):
        return URIRef(text)
    if ":" not in text:
        default_ns = prefixes.get("", None)
        if default_ns:
            ns = normalize_ns_for_join(default_ns)
            sep = "" if ns.endswith(('#', '/')) else '#'
            return URIRef(ns + sep + text)
        print(f"[WARN] Bare name '{text}' encountered but no default prefix defined. Returning raw URIRef.")
        return URIRef(text)
    prefix, local = text.split(":", 1)
    if prefix in ("", ":"):
        ns = prefixes.get("", None)
    else:
        ns = prefixes.get(prefix, None)
    if not ns:
        print(f"[WARN] Prefix '{prefix}' not found when resolving '{text}'. Returning raw URIRef.")
        return URIRef(text)
    ns_norm = normalize_ns_for_join(ns)
    sep = "" if ns_norm.endswith(('#', '/')) else '#'
    return URIRef(ns_norm + sep + local)

def ensure_declaration(g: Graph, uri: Optional[URIRef], rdf_type):
    """
    Only add declaration if uri is a named URIRef (not a BNode).
    This avoids inflating 'declaration axiom' counts by declaring anonymous restriction nodes.
    """
    if uri is not None and isinstance(uri, URIRef):
        g.add((uri, RDF.type, rdf_type))

def reconstruct_intersection(g: Graph, uris):
    bnode = BNode()
    Collection(g, bnode, uris)
    return bnode

# --------------------- CSV → OWL Conversion Functions ---------------------

def csv_to_owl_class(class_csv_file: str, prefix_file: str, output_file="classes.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        df = pd.read_csv(class_csv_file, dtype=str)
    except FileNotFoundError:
        print(f"[WARN] class CSV '{class_csv_file}' not found — skipping classes.")
        return
    except Exception as e:
        print(f"[ERROR] reading classes CSV '{class_csv_file}': {e}")
        return
    candidates = [c for c in df.columns if c.lower().strip() in ('owl class', 'owlclass', 'class')]
    if not candidates:
        print(f"[WARN] No 'OWL Class' column found in {class_csv_file}; columns = {df.columns.tolist()}")
        return
    col = candidates[0]
    for val in df[col].dropna().astype(str):
        uri = resolve_uri(val.strip(), prefixes)
        ensure_declaration(g, uri, OWL.Class)
    g.serialize(destination=output_file, format='xml')
    print(f"✅ Class triples written to: {output_file}")

def csv_to_owl_subclass(subclass_csv_file: str, prefix_file: str, output_file="subclass.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        df = pd.read_csv(subclass_csv_file, dtype=str).fillna("")
    except FileNotFoundError:
        print(f"[WARN] subclass CSV '{subclass_csv_file}' not found — skipping subclasses.")
        return
    except Exception as e:
        print(f"[ERROR] reading subclass CSV '{subclass_csv_file}': {e}")
        return

    def find_col(cols, candidates):
        for cand in candidates:
            for c in cols:
                if c.lower().strip() == cand.lower().strip():
                    return c
        return None

    subj_col = find_col(df.columns, ["Subclass", "subclass"])
    super_col = find_col(df.columns, ["Superclass", "superclass"])
    prop_col = find_col(df.columns, ["Restriction (onProperty)", "onProperty", "Restriction (onproperty)", "on_property"])
    quant_col = find_col(df.columns, ["Restriction (quantifier)", "quantifier", "Restriction (quantifier)"])

    def build_restriction(prop_uri, quantifier, filler_uri):
        b = BNode()
        g.add((b, RDF.type, OWL.Restriction))
        g.add((b, OWL.onProperty, prop_uri))
        if quantifier == "some":
            g.add((b, OWL.someValuesFrom, filler_uri))
        else:
            g.add((b, OWL.allValuesFrom, filler_uri))
        return b

    for row_idx, row in df.iterrows():
        subclass_str = (row.get(subj_col, "") or "").strip()
        superclass_str = (row.get(super_col, "") or "").strip()
        on_property_str = (row.get(prop_col, "") or "").strip()
        quantifier = (row.get(quant_col, "") or "").strip().lower()

        on_property_uri = resolve_uri(on_property_str, prefixes) if on_property_str else None
        superclass_uri = resolve_uri(superclass_str, prefixes) if superclass_str else None

        # textual restriction in subclass column => create anonymous restriction ⊑ Superclass (GCI)
        if subclass_str and (" some " in subclass_str or " all " in subclass_str):
            if " some " in subclass_str:
                parts = subclass_str.split(" some ", 1); q = "some"
            else:
                parts = subclass_str.split(" all ", 1); q = "all"
            prop_part = parts[0].strip()
            fill_part = parts[1].strip() if len(parts) > 1 else ""
            prop_uri = resolve_uri(prop_part, prefixes) if prop_part else None
            filler_uri = resolve_uri(fill_part, prefixes) if fill_part else None
            if prop_uri and filler_uri and superclass_uri:
                restriction_bnode = build_restriction(prop_uri, q, filler_uri)
                # Do NOT declare the restriction bnode (anonymous). Declare only named IRIs.
                ensure_declaration(g, prop_uri, OWL.ObjectProperty)
                ensure_declaration(g, filler_uri, OWL.Class)
                ensure_declaration(g, superclass_uri, OWL.Class)
                g.add((restriction_bnode, RDFS.subClassOf, superclass_uri))
                continue
            else:
                print(f"[WARN] Could not resolve textual restriction in Subclass column (row {row_idx}): '{subclass_str}'")

        # intersection A & B ⊑ C
        if subclass_str and "&" in subclass_str:
            parts = [p.strip() for p in subclass_str.split("&") if p.strip()]
            class_uris = [resolve_uri(p, prefixes) for p in parts]
            class_uris = [u for u in class_uris if u is not None]
            for cls in class_uris:
                ensure_declaration(g, cls, OWL.Class)
            anon_cls = BNode()
            g.add((anon_cls, OWL.intersectionOf, reconstruct_intersection(g, class_uris)))
            if superclass_uri:
                g.add((anon_cls, RDFS.subClassOf, superclass_uri))
            continue

        # A ⊑ (∃R.C) or (∀R.C)
        if subclass_str and on_property_uri and quantifier and superclass_uri:
            subclass_uri = resolve_uri(subclass_str, prefixes)
            restriction = BNode()
            g.add((restriction, RDF.type, OWL.Restriction))
            g.add((restriction, OWL.onProperty, on_property_uri))
            if quantifier == "some":
                g.add((restriction, OWL.someValuesFrom, superclass_uri))
            else:
                g.add((restriction, OWL.allValuesFrom, superclass_uri))
            ensure_declaration(g, subclass_uri, OWL.Class)
            ensure_declaration(g, on_property_uri, OWL.ObjectProperty)
            ensure_declaration(g, superclass_uri, OWL.Class)
            g.add((subclass_uri, RDFS.subClassOf, restriction))
            continue

        # GCI row: empty Subclass but restriction columns filled -> restriction ⊑ Superclass
        if (not subclass_str) and on_property_uri and quantifier and superclass_uri:
            restriction_bnode = build_restriction(on_property_uri, quantifier, superclass_uri)
            ensure_declaration(g, on_property_uri, OWL.ObjectProperty)
            ensure_declaration(g, superclass_uri, OWL.Class)
            g.add((restriction_bnode, RDFS.subClassOf, superclass_uri))
            continue

        # Simple A ⊑ B
        if subclass_str and superclass_uri:
            subclass_uri = resolve_uri(subclass_str, prefixes)
            ensure_declaration(g, subclass_uri, OWL.Class)
            ensure_declaration(g, superclass_uri, OWL.Class)
            g.add((subclass_uri, RDFS.subClassOf, superclass_uri))
            continue

        if any([subclass_str, on_property_str, superclass_str, quantifier]):
            print(f"[WARN] Unhandled subclass row {row_idx}: Subclass='{subclass_str}', onProperty='{on_property_str}', quantifier='{quantifier}', Superclass='{superclass_str}'")

    g.serialize(destination=output_file, format='xml')
    print(f"✅ Subclass triples written to {output_file}")

def csv_to_owl_domain(domain_csv_file: str, prefix_file: str, output_file="domain.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        with open(domain_csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            colnames = list(reader.fieldnames or [])
            prop_col = None; dom_col = None
            for c in colnames:
                lc = c.lower().strip()
                if lc in ("object","property","prop","predicate"):
                    prop_col = c
                if lc in ("domain","class","domain_class"):
                    dom_col = c
            if prop_col is None and colnames:
                prop_col = colnames[0]
            if dom_col is None and len(colnames) > 1:
                dom_col = colnames[1]
            for row in reader:
                prop_uri = resolve_uri(row.get(prop_col, ""), prefixes)
                domain_uri = resolve_uri(row.get(dom_col, ""), prefixes)
                ensure_declaration(g, prop_uri, OWL.ObjectProperty)
                ensure_declaration(g, domain_uri, OWL.Class)
                g.add((prop_uri, RDFS.domain, domain_uri))
    except FileNotFoundError:
        print(f"[WARN] domain CSV '{domain_csv_file}' not found — skipping domain.")
        return
    except Exception as e:
        print(f"[ERROR] reading domain CSV '{domain_csv_file}': {e}")
        return
    g.serialize(destination=output_file, format='xml')
    print(f"✅ Domain triples written to {output_file}")

def csv_to_owl_range(range_csv_file: str, prefix_file: str, output_file="range.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        with open(range_csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            colnames = list(reader.fieldnames or [])
            prop_col = None; range_col = None
            for c in colnames:
                lc = c.lower().strip()
                if lc in ("object","property","prop","predicate"):
                    prop_col = c
                if lc in ("range","class","range_class"):
                    range_col = c
            if prop_col is None and colnames:
                prop_col = colnames[0]
            if range_col is None and len(colnames) > 1:
                range_col = colnames[1]
            for row in reader:
                prop_uri = resolve_uri(row.get(prop_col, ""), prefixes)
                rng_uri = resolve_uri(row.get(range_col, ""), prefixes)
                ensure_declaration(g, prop_uri, OWL.ObjectProperty)
                ensure_declaration(g, rng_uri, OWL.Class)
                g.add((prop_uri, RDFS.range, rng_uri))
    except FileNotFoundError:
        print(f"[WARN] range CSV '{range_csv_file}' not found — skipping range.")
        return
    except Exception as e:
        print(f"[ERROR] reading range CSV '{range_csv_file}': {e}")
        return
    g.serialize(destination=output_file, format='xml')
    print(f"✅ Range triples written to {output_file}")

def csv_to_owl_instances(instances_csv_file: str, prefix_file: str, output_file="instances.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        with open(instances_csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            colnames = list(reader.fieldnames or [])
            inst_col = None; class_col = None
            for c in colnames:
                lc = c.lower().strip()
                if lc in ("instances","instance","subject","individual","iri"):
                    inst_col = c
                if lc in ("class","type","rdf:type"):
                    class_col = c
            if inst_col is None and colnames:
                inst_col = colnames[0]
            if class_col is None and len(colnames) > 1:
                class_col = colnames[1]
            for row in reader:
                inst_uri = resolve_uri(row.get(inst_col, ""), prefixes)
                cls_uri = resolve_uri(row.get(class_col, ""), prefixes)
                ensure_declaration(g, inst_uri, OWL.NamedIndividual)
                ensure_declaration(g, cls_uri, OWL.Class)
                g.add((inst_uri, RDF.type, cls_uri))
    except FileNotFoundError:
        print(f"[WARN] instances CSV '{instances_csv_file}' not found — skipping instances.")
        return
    except Exception as e:
        print(f"[ERROR] reading instances CSV '{instances_csv_file}': {e}")
        return
    g.serialize(destination=output_file, format='xml')
    print(f"✅ Instances written to {output_file}")

def csv_to_owl_subproperty(subproperty_csv_file: str, prefix_file: str, output_file="subproperty.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        df = pd.read_csv(subproperty_csv_file, dtype=str).fillna("")
    except FileNotFoundError:
        print(f"[WARN] subproperty CSV '{subproperty_csv_file}' not found — skipping subproperty.")
        return
    except Exception as e:
        print(f"[ERROR] reading subproperty CSV '{subproperty_csv_file}': {e}")
        return

    def find_col(cols, cand_list):
        for cand in cand_list:
            for c in cols:
                if c.lower().strip() == cand.lower().strip():
                    return c
        return None

    sub_col = find_col(df.columns, ["subproperty","subProperty","sub_property"])
    sup_col = find_col(df.columns, ["superproperty","superProperty","super_property"])
    r1_col = find_col(df.columns, ["role1","role_1","role 1"])
    r2_col = find_col(df.columns, ["role2","role_2","role 2"])
    if sub_col is None and len(df.columns) > 0:
        sub_col = df.columns[0]
    if sup_col is None and len(df.columns) > 1:
        sup_col = df.columns[-1]

    for _, row in df.iterrows():
        sub_raw = (row.get(sub_col, "") or "").strip()
        sup_raw = (row.get(sup_col, "") or "").strip()
        role1_raw = (row.get(r1_col, "") or "").strip()
        role2_raw = (row.get(r2_col, "") or "").strip()

        sub_uri = resolve_uri(sub_raw, prefixes) if sub_raw else None
        sup_uri = resolve_uri(sup_raw, prefixes) if sup_raw else None

        # Build role list (support several separators)
        roles = []
        if role1_raw:
            if " o " in role1_raw:
                roles.extend([r.strip() for r in role1_raw.split(" o ") if r.strip()])
            elif "," in role1_raw:
                roles.extend([r.strip() for r in role1_raw.split(",") if r.strip()])
            else:
                roles.append(role1_raw.strip())
        if role2_raw:
            roles.extend([r.strip() for r in role2_raw.split(" o ") if r.strip()])

        # If chain roles present and sup is present => create propertyChainAxiom only (no subPropertyOf)
        if sup_uri and roles:
            chain_nodes = []
            for r in roles:
                r_uri = resolve_uri(r, prefixes)
                if r_uri:
                    ensure_declaration(g, r_uri, OWL.ObjectProperty)
                    chain_nodes.append(r_uri)
            if chain_nodes:
                ensure_declaration(g, sup_uri, OWL.ObjectProperty)
                chain_bnode = BNode()
                Collection(g, chain_bnode, chain_nodes)
                g.add((sup_uri, OWL.propertyChainAxiom, chain_bnode))
            else:
                print(f"[WARN] Could not resolve roles for property chain of '{sup_raw}' -> roles: {roles}")
            continue

        # If explicit subproperty present (and no chain), add subPropertyOf
        if sub_uri and sup_uri:
            ensure_declaration(g, sub_uri, OWL.ObjectProperty)
            ensure_declaration(g, sup_uri, OWL.ObjectProperty)
            g.add((sub_uri, RDFS.subPropertyOf, sup_uri))
            continue

        if any([sub_raw, sup_raw, role1_raw, role2_raw]):
            print(f"[WARN] Unhandled subproperty row: sub='{sub_raw}', sup='{sup_raw}', role1='{role1_raw}', role2='{role2_raw}'")

    g.serialize(destination=output_file, format='xml')
    print(f"✅ Subproperty triples (with chains) written to {output_file}")

def csv_to_owl_maxcardinality(maxcard_csv_file: str, prefix_file: str, output_file="maxcardinality.owl"):
    g = Graph()
    prefixes, xml_base = load_prefixes(prefix_file)
    _bind_prefixes_to_graph(g, prefixes)
    try:
        df = pd.read_csv(maxcard_csv_file, dtype=str).fillna("")
    except FileNotFoundError:
        print(f"[WARN] maxcard CSV '{maxcard_csv_file}' not found — skipping maxcardinality.")
        return
    except Exception as e:
        print(f"[ERROR] reading maxcard CSV '{maxcard_csv_file}': {e}")
        return
    cols = list(df.columns)
    cls_col = next((c for c in cols if c.lower().strip() in ("class","owl class")), cols[0] if cols else None)
    onprop_col = next((c for c in cols if c.lower().strip() in ("onproperty","on_property","on property")), cols[1] if len(cols)>1 else None)
    card_col = next((c for c in cols if c.lower().strip() in ("maxcardinality","max_cardinality","maxCardinality")), cols[2] if len(cols)>2 else None)

    for _, row in df.iterrows():
        cls_raw = (row.get(cls_col, "") or "").strip()
        prop_raw = (row.get(onprop_col, "") or "").strip()
        card_raw = (row.get(card_col, "") or "").strip()
        if not (cls_raw and prop_raw and card_raw):
            print(f"[WARN] Skipping incomplete maxcard row: class='{cls_raw}', onprop='{prop_raw}', card='{card_raw}'")
            continue
        try:
            card_int = int(card_raw)
        except Exception:
            print(f"[WARN] Non-integer maxCardinality '{card_raw}' for {cls_raw} — skipping")
            continue
        cls_uri = resolve_uri(cls_raw, prefixes)
        prop_uri = resolve_uri(prop_raw, prefixes)
        ensure_declaration(g, cls_uri, OWL.Class)
        ensure_declaration(g, prop_uri, OWL.ObjectProperty)
        restriction = BNode()
        g.add((restriction, RDF.type, OWL.Restriction))
        g.add((restriction, OWL.onProperty, prop_uri))
        g.add((restriction, OWL.maxCardinality, Literal(card_int, datatype=XSD.nonNegativeInteger)))
        g.add((cls_uri, RDFS.subClassOf, restriction))
    g.serialize(destination=output_file, format='xml')
    print(f"✅ MaxCardinality triples written to {output_file}")

def combine_owl_files(owl_files, output_file="combined.owl"):
    merged_graph = Graph()
    for file in owl_files:
        try:
            merged_graph.parse(file, format="xml")
            print(f"[INFO] Parsed {file}")
        except Exception as e:
            print(f"[ERROR] Failed to parse {file}: {e}")
    merged_graph.serialize(destination=output_file, format='xml')
    print(f"\n✅ Combined OWL written to {output_file}")

# --------------------- CLI-like main runner ---------------------
if __name__ == "__main__":
    csv_to_owl_class("owlclass.csv", "prefixiri.csv", "classes.owl")
    csv_to_owl_subclass("subclass.csv", "prefixiri.csv", "subclass.owl")
    csv_to_owl_domain("domain.csv", "prefixiri.csv", "domain.owl")
    csv_to_owl_range("range.csv", "prefixiri.csv", "range.owl")
    csv_to_owl_instances("instances.csv", "prefixiri.csv", "instances.owl")
    csv_to_owl_subproperty("subproperty.csv", "prefixiri.csv", "subproperty.owl")
    csv_to_owl_maxcardinality("maxcardinality.csv", "prefixiri.csv", "maxcardinality.owl")

    combine_owl_files([
        "classes.owl",
        "subclass.owl",
        "domain.owl",
        "range.owl",
        "instances.owl",
        "subproperty.owl",
        "maxcardinality.owl"
    ])
