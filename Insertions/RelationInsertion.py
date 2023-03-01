import sys
sys.path.insert(0, '..')

from Functions.Relation import  create_relation_dir, create_relation_with_attribute
from Functions.Connection import Connection

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#GRAFO 1:
ES_attr, ET_attr = {'Name': 'Paola', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'MADRE_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Aneli', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'NONNA_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Agostina', 'Surname': 'Del Fante'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'NONNA_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Ferruccio', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'NONNO_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Fabio', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'PADRE_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Gioele', 'Surname': 'Bellosi'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'CUGINO_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Celeste', 'Surname': 'Bellosi'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'CUGINA_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Sergio', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'ZIA_DI', conn)) #G1
ES_attr, ET_attr = {'Name': 'Tamara', 'Surname': 'Rosetti'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 1, 'Person', ET_attr, 1, 'MOGLI_DI', conn)) #G1

#aggiungi scadenza
ES_attr, ET_attr = {'Name': 'Tamara', 'Surname': 'Rosetti'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_with_attribute('Person', ES_attr, 1, 'Person', ET_attr, 1, 'MOGLIE_DI', {'scadenza': '01/10/20'}, conn)) #G1

#GRAFO 2:
ES_attr, ET_attr = {'Name': 'Pina', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'MADRE_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Anna', 'Surname': 'Cerletti'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'NONNA_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Ferruccio', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'NONNO_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Fabio', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'PADRE_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Gioele', 'Surname': 'Bellosi'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'CUGINO_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Giada', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'CUGINA_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Sergio', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'ZIO_DI', conn)) #G2
ES_attr, ET_attr = {'Name': 'Vanessa', 'Surname': 'Della Morte'}, {'Name':'Pietro', 'Surname':'Masolini'}
print(create_relation_dir('Person', ES_attr, 2, 'Person', ET_attr, 2, 'MOGLIE_DI', conn)) #G2

conn.close()