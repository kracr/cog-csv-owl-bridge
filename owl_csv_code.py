import pandas as pd
from base64 import encode
from msilib.schema import Class
from token import ENCODING
import csv
import rdflib
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib import BNode
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD
import pandas as pd
import pprint
import os


def owl_csv_subclass(g):

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
        classs = (str)(obj).rsplit('/')[-1]
#          print(classs + " " + subclass)
        rows = [subj, obj]
        writer.writerow(rows)
        class_dict[subj] = class_dict.get(subj, 0)+1

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

def owl_csv_class(g):
    fields=['OWL Class']
    f = open('owlclass.csv', 'w')
    
    writer = csv.writer(f, lineterminator='\n')

    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.RDF.type:
            if obj == rdflib.OWL.Class:
                subclass = (str)(subject).rsplit('/')[-1]
                rows=[subject]
                writer.writerow(rows)
    f.close()
    return 'owlclass.csv'

def owl_csv_domain(g):

    fields = ['Object', 'Domain']
    f = open('domain.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:

        if predicate == rdflib.RDFS.domain:
            object_prop = (str)(subject).rsplit('/')[-1]
            domain = (str)(obj).rsplit('/')[-1]
            rows = [subject, obj]
            writer.writerow(rows)

    f.close()
    return 'domain.csv'


def owl_csv_range(g):

    fields = ['Object', 'Range']
    f = open('range.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        
        if predicate == rdflib.RDFS.range:
            object_prop = (str)(subject).rsplit('/')[-1]
            range = (str)(obj).rsplit('/')[-1]
            rows = [subject, obj]
            writer.writerow(rows)

    f.close()
    return 'range.csv'


def owl_csv_instances(g):
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

    for subject, predicate, obj in g:

        if predicate == rdflib.RDF.type:
            for s, p, o in g.triples((None, rdflib.RDF.type, rdflib.RDFS.Class)):
                if str(s) == str(obj):
                    subj = (str)(subject).rsplit('/')[-1]
                    objj = (str)(obj).rsplit('/')[-1]
                    # print(subj + " " + objj)
                    rows = [subject, obj]
                    writer.writerow(rows)

    f.close()
    return 'instances.csv'


def owl_csv_subproperty(g):
    fields = ['subproperty', 'Object']
    f = open('subproperty.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        
        if predicate == rdflib.RDFS.subPropertyOf:
            subProperty = (str)(subject).rsplit('/')[-1]
            object_prop = (str)(obj).rsplit('/')[-1]
            rows = [subject, obj]
            writer.writerow(rows)

    f.close()
    return 'subproperty.csv'


def owl_csv_inverseof(g):
    fields = ['inverseOf', 'Object']
    f = open('inverseOf.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        
        if predicate == rdflib.OWL.inverseOf:
            inverseOf = (str)(subject).rsplit('/')[-1]
            object_prop = (str)(obj).rsplit('/')[-1]
            rows = [subject, obj]
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


def owl_csv_allvaluesfrom(g, onproperty_dict):
    
    allvaluesfrom_dict={}
    fields = ['Class', 'Property']
    f2 = open('allvaluesfrom1.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.allValuesFrom:
            rows = [subject, obj]
            allvaluesfrom_dict[subject]=obj
            writer.writerow(rows)

    f2.close()


    
    f3=open('allvaluesfrom.csv','w')
    writer1=csv.writer(f3, lineterminator='\n')
    fields=['Class', 'OnProperty', 'Allvaluesfrom']
    writer1.writerow(fields)
    
    fields = ['Class', 'Property']
    # f4 = open('allvaluesfrom.csv', 'w')
    # writer = csv.writer(f4, lineterminator='\n')
    # writer.writerow(fields)
    for i in allvaluesfrom_dict:
        if i in onproperty_dict:
            rows=[i, onproperty_dict[i], allvaluesfrom_dict[i]]
            writer1.writerow(rows)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.OWL.allValuesFrom:
    #         rows = [subject, obj]
    #         writer1.writerow(rows)
    #         if subject in onproperty_dict:
    #             rows=[subject, onproperty_dict[subject], obj]
    #             writer1.writerow(rows)


    f3.close()
    
    return 'allvaluesfrom.csv'

def owl_csv_somevaluesfrom(g, onproperty_dict):
    somevaluesfrom_dict={}
    fields = ['Class', 'Property']
    f2 = open('somevaluesfrom1.csv', 'w')
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.someValuesFrom:
            rows = [subject, obj]
            somevaluesfrom_dict[subject]=obj

            writer.writerow(rows)

    f2.close()


    
    f3=open('somevaluesfrom.csv','w')
    writer1=csv.writer(f3, lineterminator='\n')
    fields=['Class', 'OnProperty', 'SomeValuesfrom']
    writer1.writerow(fields)
    
    fields = ['Class', 'Property']
    # f4 = open('allvaluesfrom.csv', 'w')
    # writer = csv.writer(f4, lineterminator='\n')
    # writer.writerow(fields)
    for i in somevaluesfrom_dict:
        if i in onproperty_dict:
            rows=[i, onproperty_dict[i], somevaluesfrom_dict[i]]
            writer1.writerow(rows)
    # for subject, predicate, obj in g:
    #     if predicate == rdflib.OWL.someValuesFrom:
    #         rows = [subject, obj]
    #         writer1.writerow(rows)
    #         if subject in onproperty_dict:
    #             rows=[subject, onproperty_dict[subject], obj]
    #             writer1.writerow(rows)


    f3.close()
    
    return 'somevaluesfrom.csv'    


def main(file):
    g = Graph()
    g.parse(file)
    fields = ['Class', 'OnProperty']
    onproperty_dict={}
    f1 = open('onproperty.csv', 'w')
    writer = csv.writer(f1, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.OWL.onProperty:
            rows = [subject, obj]
            onproperty_dict[subject]=obj
            writer.writerow(rows)

    f1.close()
    f1 = owl_csv_domain(g)
    f2 = owl_csv_subclass(g)
    f3 = owl_csv_range(g)
    f4 = owl_csv_instances(g)
    f5 = owl_csv_subproperty(g)
    f6 = owl_csv_inverseof(g)
    f7 = owl_csv_allvaluesfrom(g, onproperty_dict)
    f8 = owl_csv_somevaluesfrom(g, onproperty_dict)
    f9 = owl_csv_class(g)

    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    for filename in [f9, f1, f2, f3, f4, f5, f6, f7, f8]:
        df = pd.read_csv(filename)
        sheet_name = os.path.splitext(os.path.basename(filename))[0]
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()
