import sys
sys.path.insert(0, '..')

from Functions.Connection import Connection
from Functions.Entity import create_instance_mine

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#persona uno G1
instance = {"Name" : "Pietro", "Surname" : "Masolini"}
create_instance_mine(conn, "Person", instance, 1, 1)

#persona uno G2
instance = {"Name" : "Pietro", "Surname" : "Masolini"}
create_instance_mine(conn, "Person", instance, 2, 1)

conn.close()