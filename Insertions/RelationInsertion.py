import sys
sys.path.insert(0, '..')

from Functions.Relation import create_relation_dir, create_relation_with_attribute, addConstraint
from Functions.Connection import Connection

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#TODO prima di eseguire definisci MARITO e MOGLIE, ma soprattutto definisci le contraddizioni dirette necessarie al corretto svolgimento...
#contraddizioni dirette:
addConstraint('MARITO_DI', 'MOGLIE_DI', 'CONTRADDITTORI', conn)
addConstraint('MADRE_DI', 'PADRE_DI', 'CONTRADDITTORI', conn)
addConstraint('ZIO_DI', 'ZIA_DI', 'CONTRADDITTORI', conn)
addConstraint('NONNO_DI', 'NONNA_DI', 'CONTRADDITTORI', conn)
addConstraint('CUGINO_DI', 'CUGINA_DI', 'CONTRADDITTORI', conn)

#GRAFO 1:
ES_attr, ET_attr = {'Name': 'Fabio', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'PADRE_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'Paola', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MADRE_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'g', 'Surname': 'g'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MARITO_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'Aneli', 'Surname': 'Balatti'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'NONNA_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'Lino', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'NONNO_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'Ferruccio', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'NONNO_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'Michela', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'ZIO_DI', conn) #G1
ES_attr, ET_attr = {'Name': 'Marilena', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'ZIA_DI', conn) #G1

#aggiungi scadenza
ES_attr, ET_attr = {'Name': 'zz', 'Surname': 'zz'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_with_attribute('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MARITO_DI', {'scadenza': '02/09/21'}, conn) #G1

#aggiungi scadenza
ES_attr, ET_attr = {'Name': 'x', 'Surname': 'x'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_with_attribute('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MOGLIE_DI', {'scadenza': '01/10/21'}, conn) #G1

ES_attr, ET_attr = {'Name': 'Pietro', 'Surname': 'Masolini'}, {'Name':'Gioele', 'Surname':'Bellosi'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'CUGINO_DI', conn) #G1

#GRAFO 2:
ES_attr, ET_attr = {'Name': 'Pina', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MADRE_DI', conn) #G2
ES_attr, ET_attr = {'Name': 'Fabio', 'Surname': 'Masolini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'PADRE_DI', conn) #G2
ES_attr, ET_attr = {'Name': 'Gigi', 'Surname': 'Balatti'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'NONNO_DI', conn) #G2
ES_attr, ET_attr = {'Name': 'Tina', 'Surname': 'Del Fante'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'NONNA_DI', conn) #G2
ES_attr, ET_attr = {'Name': 'Michela', 'Surname': 'Scaramellini'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'ZIA_DI', conn) #G2

#aggiungi scadenza
ES_attr, ET_attr = {'Name': 'z', 'Surname': 'z'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_with_attribute('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MARITO_DI', {'scadenza': '01/10/21'}, conn) #G2

ES_attr, ET_attr = {'Name': 'y', 'Surname': 'y'}, {'Name':'Pietro', 'Surname':'Masolini'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MOGLIE_DI', conn) #G2
ES_attr, ET_attr = {'Name': 'Pietro', 'Surname': 'Masolini'}, {'Name':'f', 'Surname':'f'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'MARITO_DI', conn) #G2
ES_attr, ET_attr = {'Name': 'Pietro', 'Surname': 'Masolini'}, {'Name':'Celeste', 'Surname':'Bellosi'}
create_relation_dir('Person', ES_attr, 1, 'Indirizzo', ET_attr, 1, 'CUGINO_DI', conn) #G2


conn.close()