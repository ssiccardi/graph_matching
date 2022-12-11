import sys
sys.path.insert(0, '..')

from Functions.Relation import create_relation_dir
from Functions.Connection import Connection

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

ES_attr, ET_attr = {'Name':'Pietro', 'Surname':'Masolini'}, {'NomeIndirizzo': 'via Del Belvedere', 'Numero_Civico': '2'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'RISIEDE_A', conn) #G1
create_relation_dir('Person', ES_attr, 2, 'Indirizzo', ET_attr, 2, 'RISIEDE_A', conn) #G2

conn.close()