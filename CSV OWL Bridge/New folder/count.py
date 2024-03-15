import os
from rdflib import Graph
import csv
import pprint
from funowl.converters.functional_converter import to_python
f1=open('/home/rohit19268/test/didntwork.csv', 'w')
dir_path='/home/rohit19268/test/files'
files=os.listdir(dir_path)
total=0
axioms_dict={}
for file_name in files:
    file_path=os.path.join(dir_path,file_name)
    try:
        if os.path.isfile(file_path):
            internal_file=to_python(file_path)
            g=Graph()
            internal_file.to_rdf(g)
            s1=file_path.rsplit('_')[-1]
            s2=s1.split('.')
            print(s2)
            s='/home/rohit19268/test/files'+ 'ore'+s2[0]+ '.owl'
            g.serialize(destination=s, format='xml')
            
            
            for stmt in g:
    #             pprint.pprint(stmt[0])
    #             pprint.pprint(stmt[1])
    #             pprint.pprint(stmt[2])
    #             print()

                s=stmt[1]
                if '#' in s:
                    index=s.index('#')
                    s1=s[index+1:]
                    if s1!='type':
                        axioms_dict[s1]=axioms_dict.get(s1,0)+1
                        total+=1

            


            
            
    #         s1=file_path.rsplit('_')[-1]
    #         s2=s1.split('.')
    #         print(s2)
    #         s='C:/Users/Rohit Bhatia/Desktop/btp/pool_sample/'+ 'ore'+s2[0]+ '.csv'
    except Exception as e:
        writer = csv.writer(f1, lineterminator='\n')
        writer.writerow(s2[0]+'.owl')
        writer.writerow("")
        
    fields = ['Axiom', 'Count']
    s='/home/rohit19268/test/count_ontology_new.csv'
    f= open(s, 'w')
    writer = csv.writer(f, lineterminator='\n')
    row=["Total axioms for ontologies", total]
    writer.writerow(row)
    writer.writerow("")
    writer.writerow(fields)
    for key, value in axioms_dict.items():
        percent= (value/total)*100
        row=[key, value, percent]
        writer.writerow(row)


fields = ['Axiom', 'Count']
s='/home/rohit19268/test/count_ontology.csv'
f= open(s, 'w')
writer = csv.writer(f, lineterminator='\n')
row=["Total axioms for ontologies", total]
writer.writerow(row)
writer.writerow("")
writer.writerow(fields)
for key, value in axioms_dict.items():
    percent= (value/total)*100
    row=[key, value, percent]
    writer.writerow(row)

f1.close()
f.close()
