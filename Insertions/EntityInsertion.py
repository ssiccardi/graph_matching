import sys
sys.path.insert(0, '..')

from Functions.Connection import Connection
from Functions.Entity import create_instance_mine

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#GRAFO 1:
#create_instance_mine(conn, "Person", {"Name" : "Pietro", "Surname" : "Masolini"}, 1, 1)
#create_instance_mine(conn, "Person", {"Name" : "Paola", "Surname" : "Scaramellini"}, 1, 2)
#create_instance_mine(conn, "Person", {"Name" : "Fabio", "Surname" : "Masolini"}, 1, 3)
#create_instance_mine(conn, "Person", {"Name" : "g", "Surname" : "g"}, 1, 4)
#create_instance_mine(conn, "Person", {"Name" : "Aneli", "Surname" : "Balatti"}, 1, 5)
#create_instance_mine(conn, "Person", {"Name" : "Lino", "Surname" : "Masolini"}, 1, 6)
#create_instance_mine(conn, "Person", {"Name" : "Ferruccio", "Surname" : "Scaramellini"}, 1, 7)
#create_instance_mine(conn, "Person", {"Name" : "Marilena", "Surname" : "Masolini"}, 1, 8)
#create_instance_mine(conn, "Person", {"Name" : "zz", "Surname" : "zz"}, 1, 9)
#create_instance_mine(conn, "Person", {"Name" : "x", "Surname" : "x"}, 1, 10)
#create_instance_mine(conn, "Person", {"Name" : "Gioele", "Surname" : "Bellosi"}, 1, 11)
#create_instance_mine(conn, "Person", {"Name" : "Michela", "Surname" : "Scaramellini"}, 1, 12)

#GRAFO 2:
#create_instance_mine(conn, "Person", {"Name" : "Pietro", "Surname" : "Masolini"}, 2, 1)
#create_instance_mine(conn, "Person", {"Name" : "Pina", "Surname" : "Scaramellini"}, 2, 2)
#create_instance_mine(conn, "Person", {"Name" : "Fabio", "Surname" : "Masolini"}, 2, 3)
#create_instance_mine(conn, "Person", {"Name" : "Tina", "Surname" : "Del Fante"}, 2, 4)
#create_instance_mine(conn, "Person", {"Name" : "Gigi", "Surname" : "Balatti"}, 2, 5)
#create_instance_mine(conn, "Person", {"Name" : "Michela", "Surname" : "Scaramellini"}, 2, 6)
#create_instance_mine(conn, "Person", {"Name" : "z", "Surname" : "z"}, 2, 7)
#create_instance_mine(conn, "Person", {"Name" : "y", "Surname" : "y"}, 2, 8)
#create_instance_mine(conn, "Person", {"Name" : "f", "Surname" : "f"}, 2, 9)
#create_instance_mine(conn, "Person", {"Name" : "Celeste", "Surname" : "Bellosi"}, 2, 10)

conn.close()