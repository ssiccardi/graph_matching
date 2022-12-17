import sys
sys.path.insert(0, '..')

from Functions.RelationMatching import relationMatching
import Functions.Relation as r
import Functions.Entity as e
from Functions.Connection import Connection

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

"""
e.create_instance_mine(conn, "Person", {'Name':'Piero', 'Surname':'Maso'}, 1, 100)
e.create_instance_mine(conn, "Person", {'Name':'Piero', 'Surname':'Maso'}, 2, 100)
e.create_instance_mine(conn, "Person", {'Name':'Paola', 'Surname':'Maso'}, 1, 101)
e.create_instance_mine(conn, "Person", {'Name':'Paola', 'Surname':'Maso'}, 2, 101)
e.create_instance_mine(conn, "Person", {'Name':'Gina', 'Surname':'Maso'}, 1, 102)
e.create_instance_mine(conn, "Person", {'Name':'Gina', 'Surname':'Maso'}, 2, 102)

r.create_relation_dir("Person", {'Name':'Paola', 'Surname':'Maso'}, 1, "Person", {'Name':'Piero', 'Surname':'Maso'}, 1, "MADRE_DI", conn)
r.create_relation_dir("Person", {'Name':'Paola', 'Surname':'Maso'}, 2, "Person", {'Name':'Piero', 'Surname':'Maso'}, 2, "PADRE_DI", conn)
r.create_relation_dir("Person", {'Name':'Gina', 'Surname':'Maso'}, 2, "Person", {'Name':'Piero', 'Surname':'Maso'}, 2, "MADRE_DI", conn)

e.create_instance_mine(conn, "Person", {'Name':'Sina', 'Surname':'Maso'}, 1, 104)
e.create_instance_mine(conn, "Person", {'Name':'Sina', 'Surname':'Maso'}, 2, 104)
r.create_relation_with_attribute("Person", {'Name':'Gina', 'Surname':'Maso'}, 2, "Person", {'Name':'Piero', 'Surname':'Maso'}, 2, "MADRE_DI", {'scadenza':'10-02-2002'}, conn)

print(r.create_relation_dir("Person", {'Name':'Gina', 'Surname':'Maso'}, 2, "Person", {'Name':'Piero', 'Surname':'Maso'}, 2, "PADRE_DI", conn))
"""

print(relationMatching(100, conn))

conn.close()
