import sys
sys.path.insert(0, '..')

import Functions.EntityMatching as em
import Functions.Entity as e
from Functions.Connection import Connection

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#print("TESTING algoritmo confronto tra entita\':")
#for i in range(1, 30):
#    print("Confronto entita' numero " + str(i))
#    print(em.entityMatching(i, conn))
#    print("------------------------------------------------------------------------------------------------------")

e.getEntity(201, conn)

conn.close()
