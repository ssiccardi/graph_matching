import sys
sys.path.insert(0, '..')

from Functions.RelationMatching import relationMatching
from Functions.Connection import Connection

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

df = relationMatching(1, conn)

conn.close()

f = open("../Contents/RelationMatchingAnalisi.csv", "w")
f.write(df.to_csv())
f.close()