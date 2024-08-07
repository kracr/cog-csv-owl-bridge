import logging


import pandas as pd
import re
from base64 import encode
from msilib.schema import Class
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
# Configure logging



def owl_csv_subclass(g, uri):
    global count
    class_dict = {}
    fields = ['Class', 'Parent']
    f = open('subclass.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subj, obj in g.subject_objects(predicate=RDFS.subClassOf):
        # subclass=(str)(subj).rsplit('/')[-1]
        # classs=(str)(obj).rsplit('/')[-1]
        # #print(classs + " " + subclass)
        # rows = [subclass, classs]
        # writer.writerow(rows)
        # class_dict[subclass]=class_dict.get(subclass,0)+1

        subclass = (str)(subj).rsplit('/')[-1]
        if (subj.rsplit('/')[0] == 'http:'):
            name = URIRef(subj)
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
            a = '_:'+subj
        classs = (str)(obj).rsplit('/')[-1]
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

#
        rows = [a, b]
        writer.writerow(rows)
        # class_dict[subj] = class_dict.get(subj, 0)+1

    # for subject, predicate, obj in g:
    #     if predicate == rdflib.RDF.type:
    #         if obj == rdflib.OWL.Class:
    #             subclass = (str)(subject).rsplit('/')[-1]
    #             # print(subclass)
    #             class_dict[subject] = class_dict.get(subject, 0)+1

    # for i in class_dict:
    #     if class_dict[i] == 1:
    #         rows = [i]
    #         writer.writerow(rows)

    # f.close()
    return 'subclass.csv'


def owl_csv_class(g, uri):
    global count
    fields = ['OWL Class']
    f = open('owlclass.csv', 'w')

    writer = csv.writer(f, lineterminator='\n')

    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.RDF.type:
            if obj == rdflib.OWL.Class:
                subclass = (str)(subject).rsplit('/')[-1]
                if (subject.rsplit('/')[0] == 'http:'):
                    name = URIRef(subject)
                    namespace, local_name = split_uri(str(name))
                    print(namespace +" " + local_name)
                    # rows=[local_name]
                    # writer.writerow(rows)
                    if namespace in uri:
                        rows = [uri[namespace]+":" + local_name]
                        writer.writerow(rows)
                    else:
                        prefix = 'ns'+str(count)
                        count += 1
                        uri[namespace] = prefix
                        rows = [uri[namespace]+":"+local_name]
                        writer.writerow(rows)
                else:
                    rows = ['_:'+subject]
                    writer.writerow(rows)
    f.close()
    # fields=['OWL Class']
    # f = open('owlclass.csv', 'w')

    # writer = csv.writer(f, lineterminator='\n')

    # writer.writerow(fields)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.RDF.type:
    #         if obj == rdflib.OWL.Class:
    #             subclass = (str)(subject).rsplit('/')[-1]
    #             rows=[subject]
    #             writer.writerow(rows)
    # f.close()
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

#     for subject, predicate, obj in g:
#             if predicate == rdflib.RDF.type:
#                 objj=(str)(obj)
#                 if not 'Property' in objj and not 'Class'in objj:
#                     subj=(str)(subject).rsplit('/')[-1]
#                     objj=(str)(objj).rsplit('/')[-1]
#                     print(subj + " " + objj)

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

                # print(subj + " " + objj)
                    rows = [a, b]
                    writer.writerow(rows)

    f.close()
    return 'instances.csv'


def owl_csv_subproperty(g, uri):
    global count
    fields = ['subproperty', 'Object']
    f = open('subproperty.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:

        if predicate == rdflib.RDFS.subPropertyOf:
            subProperty = (str)(subject).rsplit('/')[-1]
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
            object_prop = (str)(obj).rsplit('/')[-1]
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
    return 'subproperty.csv'


def owl_csv_inverseof(g, uri):
    global count
    fields = ['inverseOf', 'Object']
    f = open('inverseOf.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:

        if predicate == rdflib.OWL.inverseOf:
            inverseOf = (str)(subject).rsplit('/')[-1]
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
            object_prop = (str)(obj).rsplit('/')[-1]
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
    return 'inverseOf.csv'


# def owl_csv_allvaluesfrom(g):
#     fields = ['Class', 'Property']
#     f = open('somevaluesfrom.csv', 'w')
#     writer = csv.writer(f, lineterminator='\n')
#     writer.writerow(fields)
#     for subject, predicate, obj in g:
#         if predicate == rdflib.OWL.allValuesFrom:
#             rows = [subject, obj]
#             writer.writerow(rows)

#     f.close()
#     return 'allvaluesfrom.csv'


def owl_csv_allvaluesfrom(g, onproperty_dict, uri):
    global count
    allvaluesfrom_dict = {}
    fields = ['Class', 'Property']
    f2 = open('allvaluesfrom1.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.allValuesFrom:
            rows = [subject, obj]
            allvaluesfrom_dict[subject] = obj
            writer.writerow(rows)

    f2.close()

    f3 = open('allvaluesfrom_temp.csv', 'w')
    writer1 = csv.writer(f3, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'Allvaluesfrom']
    writer1.writerow(fields)

    for i in allvaluesfrom_dict:
        if i in onproperty_dict:
            rows = [i, onproperty_dict[i], allvaluesfrom_dict[i]]
            writer1.writerow(rows)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.OWL.allValuesFrom:
    #         rows = [subject, obj]
    #         writer1.writerow(rows)
    #         if subject in onproperty_dict:
    #             rows=[subject, onproperty_dict[subject], obj]
    #             writer1.writerow(rows)

    f3.close()
    temp = pd.read_csv('allvaluesfrom_temp.csv')
    classs = temp.iloc[:, 0].values
    # print(classs)
    onproperty = temp.iloc[:, 1].values
    # print(onproperty)
    allvaluesfrom = temp.iloc[:, 2].values

    f4 = open('allvaluesfrom.csv', 'w')
    writer4 = csv.writer(f4, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'allValuesFrom']
    writer4.writerow(fields)
    for (subject, predicate, obj) in zip(classs, onproperty, allvaluesfrom):

        if (subject.rsplit('/')[0] == 'http:'):
            name = URIRef(subject)
            namespace, local_name = split_uri(str(name))
            # a1=local_name
            if namespace in uri:
                a1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                a1 = uri[namespace]+":"+local_name
        else:
            a1 = '_:'+subject

        if (predicate.rsplit('/')[0] == 'http:'):
            name = URIRef(predicate)
            namespace, local_name = split_uri(str(name))
            # b1=local_name
            if namespace in uri:
                b1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                b1 = uri[namespace]+":"+local_name
        else:
            b1 = '_:'+predicate

        if (obj.rsplit('/')[0] == 'http:'):
            name = URIRef(obj)
            namespace, local_name = split_uri(str(name))
            # c1=local_name
            if namespace in uri:
                c1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                c1 = uri[namespace]+":"+local_name
        else:
            c1 = '_:'+obj
        # print(a1+" "+ b1+" "+ c1)
        rows = [a1, b1, c1]
        writer4.writerow(rows)

    f4.close()

    return 'allvaluesfrom.csv'


def owl_csv_somevaluesfrom(g, onproperty_dict, uri):
    global count
    somevaluesfrom_dict = {}
    fields = ['Class', 'Property']
    f2 = open('somevaluesfrom1.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.someValuesFrom:
            rows = [subject, obj]
            somevaluesfrom_dict[subject] = obj

            writer.writerow(rows)

    f2.close()

    f3 = open('somevaluesfrom_temp.csv', 'w')
    writer1 = csv.writer(f3, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'SomeValuesfrom']
    writer1.writerow(fields)

    fields = ['Class', 'Property']
    # f4 = open('allvaluesfrom.csv', 'w')
    # writer = csv.writer(f4, lineterminator='\n')
    # writer.writerow(fields)
    for i in somevaluesfrom_dict:
        if i in onproperty_dict:
            rows = [i, onproperty_dict[i], somevaluesfrom_dict[i]]
            writer1.writerow(rows)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.OWL.someValuesFrom:
    #         rows = [subject, obj]
    #         writer1.writerow(rows)
    #         if subject in onproperty_dict:
    #             rows=[subject, onproperty_dict[subject], obj]
    #             writer1.writerow(rows)

    f3.close()

    temp = pd.read_csv('somevaluesfrom_temp.csv')
    classs = temp.iloc[:, 0].values
    # print(classs)
    onproperty = temp.iloc[:, 1].values
    # print(onproperty)
    somevaluesfrom = temp.iloc[:, 2].values

    f4 = open('somevaluesfrom.csv', 'w')
    writer4 = csv.writer(f4, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'SomeValuesFrom']
    writer4.writerow(fields)
    for (subject, predicate, obj) in zip(classs, onproperty, somevaluesfrom):

        if (subject.rsplit('/')[0] == 'http:'):
            name = URIRef(subject)
            namespace, local_name = split_uri(str(name))
            # a1=local_name
            if namespace in uri:
                a1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                a1 = uri[namespace]+":"+local_name
        else:
            a1 = '_:'+subject

        if (predicate.rsplit('/')[0] == 'http:'):
            name = URIRef(predicate)
            namespace, local_name = split_uri(str(name))
            # b1=local_name
            if namespace in uri:
                b1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                b1 = uri[namespace]+":"+local_name
        else:
            b1 = '_:'+predicate

        if (obj.rsplit('/')[0] == 'http:'):
            name = URIRef(obj)
            namespace, local_name = split_uri(str(name))
            # c1=local_name
            if namespace in uri:
                c1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                c1 = uri[namespace]+":"+local_name
        else:
            c1 = '_:'+obj
        # print(a1+" "+ b1+" "+ c1)
        rows = [a1, b1, c1]
        writer4.writerow(rows)

    f4.close()
    return 'somevaluesfrom.csv'


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

    fields = ['Class', 'Property']
    # f4 = open('allvaluesfrom.csv', 'w')
    # writer = csv.writer(f4, lineterminator='\n')
    # writer.writerow(fields)
    for i in maxcardinality_dict:
        if i in onproperty_dict:
            rows = [i, onproperty_dict[i], maxcardinality_dict[i]]
            writer1.writerow(rows)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.OWL.someValuesFrom:
    #         rows = [subject, obj]
    #         writer1.writerow(rows)
    #         if subject in onproperty_dict:
    #             rows=[subject, onproperty_dict[subject], obj]
    #             writer1.writerow(rows)

    f3.close()

    temp = pd.read_csv('maxcardinality_temp.csv')
    classs = temp.iloc[:, 0].values
    # print(classs)
    onproperty = temp.iloc[:, 1].values
    # print(onproperty)
    maxcardinality = temp.iloc[:, 2].values

    f4 = open('maxcardinality.csv', 'w')
    writer4 = csv.writer(f4, lineterminator='\n')
    fields = ['Class', 'OnProperty', 'maxCardinality']
    writer4.writerow(fields)
    for (subject, predicate, obj) in zip(classs, onproperty, maxcardinality):

        if (subject.rsplit('/')[0] == 'http:'):
            name = URIRef(subject)
            namespace, local_name = split_uri(str(name))
            # a1=local_name
            if namespace in uri:
                a1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                a1 = uri[namespace]+":"+local_name
        else:
            a1 = '_:'+subject

        if (predicate.rsplit('/')[0] == 'http:'):
            name = URIRef(predicate)
            namespace, local_name = split_uri(str(name))
            # b1=local_name
            if namespace in uri:
                b1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                b1 = uri[namespace]+":"+local_name
        else:
            b1 = '_:'+predicate

        if (obj.rsplit('/')[0] == 'http:'):
            name = URIRef(obj)
            namespace, local_name = split_uri(str(name))
            # c1=local_name
            if namespace in uri:
                c1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                c1 = uri[namespace]+":"+local_name
        else:
            c1 = '_:'+obj
        # print(a1+" "+ b1+" "+ c1)
        rows = [a1, b1, c1]
        writer4.writerow(rows)

    f4.close()

    return 'maxcardinality.csv'


def owl_csv_firstrest(g, first_dict, uri):
    global count
    rest_dict = {}
    fields = ['Class', 'Property']
    f2 = open('rest.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.RDF.rest:
            rows = [subject, obj]
            rest_dict[subject] = obj

            writer.writerow(rows)

    f2.close()

    f3 = open('firstrest_temp.csv', 'w')
    writer1 = csv.writer(f3, lineterminator='\n')
    fields = ['Class', 'First', 'Rest']
    writer1.writerow(fields)

    # f4 = open('allvaluesfrom.csv', 'w')
    # writer = csv.writer(f4, lineterminator='\n')
    # writer.writerow(fields)
    for i in rest_dict:
        if i in first_dict:
            rows = [i, first_dict[i], rest_dict[i]]
            writer1.writerow(rows)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.OWL.someValuesFrom:
    #         rows = [subject, obj]
    #         writer1.writerow(rows)
    #         if subject in onproperty_dict:
    #             rows=[subject, onproperty_dict[subject], obj]
    #             writer1.writerow(rows)

    f3.close()

    temp = pd.read_csv('firstrest_temp.csv')
    classs = temp.iloc[:, 0].values
    # print(classs)
    first = temp.iloc[:, 1].values
    # print(onproperty)
    rest = temp.iloc[:, 2].values

    f4 = open('firstrest.csv', 'w')
    writer4 = csv.writer(f4, lineterminator='\n')
    fields = ['Class', 'First', 'Rest']
    writer4.writerow(fields)
    for (subject, predicate, obj) in zip(classs, first, rest):

        if (subject.rsplit('/')[0] == 'http:'):
            name = URIRef(subject)
            namespace, local_name = split_uri(str(name))
            # a1=local_name
            if namespace in uri:
                a1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                a1 = uri[namespace]+":"+local_name
        else:
            a1 = '_:'+subject

        if (predicate.rsplit('/')[0] == 'http:'):
            name = URIRef(predicate)
            namespace, local_name = split_uri(str(name))
            # b1=local_name
            if namespace in uri:
                b1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                b1 = uri[namespace]+":"+local_name
        else:
            b1 = '_:'+predicate

        if (obj.rsplit('/')[0] == 'http:'):
            name = URIRef(obj)
            namespace, local_name = split_uri(str(name))
            # c1=local_name
            if namespace in uri:
                c1 = uri[namespace]+":" + local_name
            else:
                prefix = 'ns'+str(count)
                count += 1
                uri[namespace] = prefix
                c1 = uri[namespace]+":"+local_name
        else:
            c1 = '_:'+obj
        # print(a1+" "+ b1+" "+ c1)
        rows = [a1, b1, c1]
        writer4.writerow(rows)

    f4.close()

    return 'firstrest.csv'

def not_processing(g, uri):
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)
    for subject, predicate, obj in g:
        if not ((predicate==RDFS.subClassOf) or (predicate == rdflib.RDF.type and obj == rdflib.OWL.Class) or (predicate == rdflib.RDFS.domain) or (predicate == rdflib.RDFS.range) or (predicate == rdflib.RDF.type and obj == rdflib.OWL.NamedIndividual) or (predicate == rdflib.RDFS.subPropertyOf) or (predicate == rdflib.OWL.inverseOf) or (predicate == rdflib.OWL.onProperty) or (predicate == rdflib.RDF.rest) or (predicate == rdflib.RDF.first)):
            # print(subject)
            # print(predicate)
            # print(obj)
            # print()
            logging.error(subject)
            logging.error(predicate)
            logging.error(obj+'\n')
            # logging.info('')




def func():
    return 'prefixiri.csv'


uri = {}


def main(file):
    
    g = Graph()
    
    g.parse(file)

    # xml_str = g.serialize(format="xml")

    # # search for the xml:base attribute using a regular expression
    # match = re.search(r'xml:base="(.+?)"', xml_str)

    # # extract the xml:base value if a match was found
    # xml_base = match.group(1) if match else None

    # # print the xml:base value
    # print(xml_base)

    
    global count
    count = 1
    # if ontology_iri[-1]!='/' or ontology_iri[-1]!='#':
    #     ontology_iri=ontology_iri+'#'
    # uri[ontology_iri]='ns'+str(count)
    # count+=1
    # print(ontology_iri)
    fields = ['Class', 'OnProperty']
    onproperty_dict = {}
    f1 = open('onproperty.csv', 'w')
    writer = csv.writer(f1, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.onProperty:
            rows = [subject, obj]
            onproperty_dict[subject] = obj
            writer.writerow(rows)

    f1.close()

    fields = ['Class', 'First']
    first_dict = {}
    f2 = open('first.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.RDF.first:
            rows = [subject, obj]
            first_dict[subject] = obj
            writer.writerow(rows)
    
    f9 = owl_csv_class(g, uri)
    f1 = owl_csv_domain(g, uri)
    f2 = owl_csv_subclass(g, uri)
    f3 = owl_csv_range(g, uri)
    f4 = owl_csv_instances(g, uri)
    f5 = owl_csv_subproperty(g, uri)
    f6 = owl_csv_inverseof(g, uri)
    f7 = owl_csv_allvaluesfrom(g, onproperty_dict, uri)
    f8 = owl_csv_somevaluesfrom(g, onproperty_dict, uri)
    f11 = owl_csv_maxcardinality(g, onproperty_dict, uri)
    f12 = owl_csv_firstrest(g, first_dict, uri)

    furi = open('prefixiri.csv', 'w')
    fields = ['Prefix', 'Namespace']
    writer = csv.writer(furi, lineterminator='\n')
    writer.writerow(fields)
    for i in uri:
        rows = [uri[i], i]
        writer.writerow(rows)
    furi.close()
    f10 = func()
    name=input('Output file name: ')
    name=name+'.xlsx'
    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    for filename in [f9, f1, f2, f3, f4, f5, f6, f7, f8, f9, f11, f12, f10]:
        df = pd.read_csv(filename)
        sheet_name = os.path.splitext(os.path.basename(filename))[0]
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer._save()
    print('The default namespace for the ontology is '+ str(uri.get('ns1')))
    not_processing(g, uri)
