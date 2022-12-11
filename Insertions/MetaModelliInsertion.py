import sys
sys.path.insert(0, '..')

from Functions.Connection import Connection
import Functions.MetaModelli as md

conn = Connection("bolt://e3a58db5.databases.neo4j.io:7687", "neo4j", "KR14Xk19s07EJwooFQ9-3dAnH7cL-b9FxnEAVSmG3f0")

#MetaModelli di entita':
md.metamodelloPersona(conn)
md.metamodelloSocieta(conn)
md.metamodelloLuogo(conn)
md.metamodelloIndirizzo(conn)

#Attributi extra per MetaModelli di entita':
md.addAttribute(conn, 'Person', 'Sesso') #aggiunta sesso a persone
md.addAttribute(conn, 'Person', 'Altezza') #aggiunta altezza a persone
md.addAttribute(conn, 'Person', 'Peso') #aggiunta peso a persone

md.addAttribute(conn, 'Indirizzo', 'Numero_Civico') #aggiunta numero civico ad indirizzo

md.addAttribute(conn, 'Luogo', 'CAP') #aggiunta CAP a luogo
md.addAttribute(conn, 'Luogo', 'Regione') #aggiunta di regione a luogo

md.addAttribute(conn, 'Società', 'Capitale') #aggiunta di capitale a società
md.addAttribute(conn, 'Società', 'NumDipendenti') #aggiunta di numero di dipendenti a società

#MetaModelli di relazioni:
#ESEMPI Person (driver, NOME, RIFL, CARD)
md.relazione(conn, 'NONNO_DI', 0, 2)
md.relazione(conn, 'PADRE_DI', 0, 1)
md.relazione(conn, 'MADRE_DI', 0, 1)
md.relazione(conn, 'NONNA_DI', 0, 2)
md.relazione(conn, 'CUGINO_DI', 1, "n")
md.relazione(conn, 'CUGINA_DI', 1, "n")
md.relazione(conn, 'NIPOTE_DI', 0, "n")
md.relazione(conn, 'FIGLIO_DI', 0, "n")
md.relazione(conn, 'LAVORA_IN', 0, "n") 
md.relazione(conn, 'RISIEDE_A', 0, 1)
md.relazione(conn, 'HA_VISITATO', 0, "n")
md.relazione(conn, 'POSSIEDE', 0, "n")

#ESEMPI Società
md.relazione(conn, 'SEDE_CENTRALE_IN', 0, 1)
md.relazione(conn, 'HA_SEDE_IN', 0, "n")
md.relazione(conn, 'ESPONE_ALLA_FIERA_DI', 0, "n")
md.relazione(conn, 'HA_ASSUNTO', 0, "n")
md.relazione(conn, 'CEO', 1, 1)

#ESEMPI Indirizzo
md.relazione(conn, 'SI_TROVA_VICINO_A', 0, 1)

#ESEMPI Luogo
md.relazione(conn, 'OSPITA_SOCIETA', 0, "n")

conn.close()