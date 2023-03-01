import sys
sys.path.insert(0, '..')

from Functions.Connection import Connection
from Functions.Entity import create_instance_mine
from Functions.MetaModelli import metamodelloAutomobile, addAttribute

conn = Connection("bolt+s://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#GRAFO 1:
create_instance_mine(conn, "Person", {"Name" : "Pietro", "Surname" : "Masolini"}, 1, 1)
create_instance_mine(conn, "Person", {"Name" : "Paola", "Surname" : "Scaramellini"}, 1, 2)
create_instance_mine(conn, "Person", {"Name" : "Aneli", "Surname" : "Balatti"}, 1, 3)
create_instance_mine(conn, "Person", {"Name" : "Tina", "Surname" : "Del Fante"}, 1, 4)
create_instance_mine(conn, "Person", {"Name" : "Ferruccio", "Surname" : "Scaramellini"}, 1, 5)
create_instance_mine(conn, "Person", {"Name" : "Fabio", "Surname" : "Masolini"}, 1, 6)
create_instance_mine(conn, "Person", {"Name" : "Gioele", "Surname" : "Bellosi"}, 1, 7)
create_instance_mine(conn, "Person", {"Name" : "Celeste", "Surname" : "Bellosi"}, 1, 8)
create_instance_mine(conn, "Person", {"Name" : "Sergio", "Surname" : "Masolini"}, 1, 9)
create_instance_mine(conn, "Person", {"Name" : "Tamara", "Surname" : "Rosetti"}, 1, 10)

#GRAFO 2:
create_instance_mine(conn, "Person", {"Name" : "Pietro", "Surname" : "Masolini"}, 2, 1)
create_instance_mine(conn, "Person", {"Name" : "Pina", "Surname" : "Scaramellini"}, 2, 2)
create_instance_mine(conn, "Person", {"Name" : "Anna", "Surname" : "Cerletti"}, 2, 3)
create_instance_mine(conn, "Person", {"Name" : "Ferruccio", "Surname" : "Scaramellini"}, 2, 5)
create_instance_mine(conn, "Person", {"Name" : "Fabio", "Surname" : "Masolini"}, 2, 6)
create_instance_mine(conn, "Person", {"Name" : "Gioele", "Surname" : "Bellosi"}, 2, 7)
create_instance_mine(conn, "Person", {"Name" : "Giada", "Surname" : "Masolini"}, 2, 8)
create_instance_mine(conn, "Person", {"Name" : "Sergio", "Surname" : "Masolini"}, 2, 9)
create_instance_mine(conn, "Person", {"Name" : "Vanessa", "Surname" : "Della Morte"}, 2, 10)


create_instance_mine(conn, "Automobile", {"Targa" : "DC952JK", "Marca" : "Fiat", "NomeModello" : "Punto", "Colore" : "Nero", "Pneumatici" : "Neve",
                                          "AriaCondizionata" : "Presente", "LitriSerbatoio" :  "48"}, 1, 952) #E_1
create_instance_mine(conn, "Automobile", {"Targa" : "DC952JK", "Marca" : "Fiat", "NomeModello" : "Punto", "Colore" : "Grigio", "Pneumatici" : "4Stagioni",
                                          "AriaCondizionata" : "Assente", "Porte" : "3"}, 2, 952) #E_2

conn.close() 