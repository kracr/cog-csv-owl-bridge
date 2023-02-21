#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def owl_csv_subclass(g):

    class_dict={}
    fields = ['Class', 'Parent']
    f= open('rdftocsv_subclass.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subj,obj in g.subject_objects(predicate=RDFS.subClassOf):
        subclass=(str)(subj).rsplit('/')[-1]
        classs=(str)(obj).rsplit('/')[-1]
        print(classs + " " + subclass)
        rows = [subclass, classs]
        writer.writerow(rows)
        class_dict[subclass]=class_dict.get(subclass,0)+1

    for subject, predicate, obj in g:
        if predicate == rdflib.RDF.type:
            if obj==rdflib.RDFS.Class:
                subclass=(str)(subject).rsplit('/')[-1]
                print(subclass)
                class_dict[subclass]=class_dict.get(subclass,0)+1

    for i in class_dict:
        if class_dict[i]==1:
            rows = [i]
            writer.writerow(rows)


    f.close()  
    
    

def owl_csv_domain(g):
    
    fields = ['Object', 'Domain']
    f= open('rdftocsv_domain.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.RDFS.domain:
            object_prop= (str)(subject).rsplit('/')[-1]
            domain=(str)(obj).rsplit('/')[-1]
            rows = [object_prop, domain]
            writer.writerow(rows)

    f.close()
    

def owl_csv_range(g):
    
    fields = ['Object', 'Range']
    f= open('rdftocsv_range.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(fields)
    for subject, predicate, obj in g:
        if predicate == rdflib.RDFS.range:
            object_prop= (str)(subject).rsplit('/')[-1]
            range=(str)(obj).rsplit('/')[-1]
            rows = [object_prop, range]
            writer.writerow(rows)

    f.close()

    
def owl_csv_instances(g):
    prop=[]
    fields = ['Instances', 'Class']
    f= open('rdftocsv_instances.csv', 'w')
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
                    subj=(str)(subject).rsplit('/')[-1]
                    objj=(str)(obj).rsplit('/')[-1]
                    print(subj + " " + objj)
                    rows = [subj, objj]
                    writer.writerow(rows)
    
    f.close()




owl_csv_instances(g)

