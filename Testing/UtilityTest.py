import sys
sys.path.insert(0, '..')

from Functions.Connection import Connection
from Functions.DbUtilities import getEntityId
from Functions.Relation import isOver

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

print(isOver(117, conn))
print(getEntityId("Person", {"Name" : "Pietro", "Surname" : "Masolini"}, 1, conn))

conn.close()
