from Functions.Connection import Connection
import neo4j

def sameSource(r1, r2, conn: Connection)-> bool:
    """Controlla se le relazioni hanno la stessa entita' di partenza

    Args:
        r1 (int or str): id della relazione in grafo1
        r2 (int or str): id della relazione in grafo2
        conn (Connnection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se hanno stessa fonte, False altrimenti
    """    
    q = (
        "match (e) -[r]-> () where id(r) = "
        + str(r1)
        + " with e.id as id1 match (e) -[r]-> () where id(r) = "
        + str(r2)
        + " return e.id = id1"
    )
    return conn.query(q).pop()[0]  # type: ignore

def getLimit(tipo: str, conn: Connection)-> int:
    """Ottiene la Cardinalita per una relazione semifissa

    Args:
        tipo (str): nome della relazione
        conn (Connectio): oggetto dedicato alla connessione a Neo4j

    Returns:
        int: Cardinalita relazione se presente, ?unknown? altrimenti
    """    
    q = (
        "MATCH (e) -[:HAS]-> (ee) WHERE e.label ='"
        + tipo
        + "' and labels(ee)[0] = 'Cardinalita' return properties(ee).label"
    )
    return int(conn.query(q).pop()[0])  # type: ignore


def isSemiFissa(tipo: str, conn: Connection)-> bool:
    """Capisce se la relazione e' di tipo SemiFisso

    Args:
        tipo (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se SemiFissa, False altrimenti
    """    
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + tipo
        + "' and labels(something)[0] = 'Cardinalita' return something.label <> '1' and something.label <> 'n'"
    )
    return conn.query(q).pop()[0]  # type: ignore


# @param(tipo) il nome per trovarla nel metamodello
# return --> true se la relazione e' di tipo Fisso, false altrimenti
def isFissa(tipo: str, conn: Connection)-> bool:
    """Capisce se la relazione e' di tipo Fisso

    Args:
        tipo (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se Fissa, False altrimenti
    """    
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + tipo
        + "' and labels(something)[0] = 'Cardinalita' return something.label = '1'"
    )
    return conn.query(q).pop()[0]  # type: ignore


def isMultipla(tipo: str, conn: Connection)-> bool:
    """Capisce se la relazione e' di tipo Multiplo

    Args:
        tipo (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se Multipla, False altrimenti
    """    
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + tipo
        + "' and labels(something)[0] = 'Cardinalita' return something.label = 'n'"
    )
    return conn.query(q).pop()[0]  # type: ignore


def canCreate(tipoT: str, attrT: dict, grafoT, relName: str, conn: Connection)-> bool:
    """Capisce se la relazione tra le due entita' puo' essere creata. Quindi si chiede se tra le due e' gia' presente la relazione, se attiverebbe contraddizioni e cosi' via

    Args:
        tipoT (str): tipo dell'entita' target
        attrT (dict): attributi dell'entita' target
        grafoT (int or str): grafo dell'entita' target
        relName (str): nome della relazione 
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se passa tutti i controlli, False altrimenti
    """    
    if not isMultipla(relName, conn):
        q = (
            "MATCH () -[r:"
            + relName
            + "]-> (e:"
            + tipoT
            + ") WHERE e.graph = "
            + str(grafoT)
            + " and "
        )
        for el in attrT.items():
            q += "e." + el[0] + ' = "' + el[1] + '" and '
        q = q[:-4]
        q += " return count(r)"
        if isFissa(relName, conn):
            q += " = 1"
        else:
            q += " = " + str(getLimit(relName, conn))
        res = conn.query(q)
        return not res[0][0]  # type: ignore
    return True


def getId(t: str, attr: dict, g, conn: Connection)->  int:
    """Ottiene l'ID dell'entita riconosciuta da attributi dati e nel grafo indicato. 

    Args:
        t (str): tipo dell'entita'
        attr (dict): key-value attributes
        g (int o str): grafo
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        int: id automatico di Neo4j
    """    
    q = "MATCH (e:" + t + " { graph:" + str(g)
    for el in attr.items():
        q += ", " + el[0] + ': "' + el[1] + '"'
    q += "}) RETURN id(e)"
    return conn.query(q)[0][0]  # type: ignore

def create_relation_dir(typeES: str, ES_attr: dict, gS, typeET: str, ET_attr: dict, gT, relName: str, conn: Connection)-> str: 
    """Crea, se possibile, una relazione tra l'entita' sorgente e quella destinazione, riconosciute tramite i parametri passati, con nome specificato

    Args:
        typeES (str): tipo dell'entita' sorgente 
        ES_attr (dict): key-value attributes sorgente
        gS (int or str): grafo sorgente
        typeET (str): tipo dell'entita' destinazione
        ET_attr (dict): key-value attributes destinazione
        gT (int or str): grafo destinazione
        relName (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        str: OK se non ci sono errori
    """    
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:  # type: ignore
        with session.begin_transaction() as tx:
            if checkInsertion(
                getId(typeES, ES_attr, gS, conn),
                getId(typeET, ET_attr, gT, conn),
                relName,
                conn,
            ):
                return "RELAZIONE in contraddizione diretta con un'altra pre esistente"
            elif canCreate(typeET, ET_attr, gT, relName, conn):
                q = "MATCH (eT:" + typeET + " { graph:" + str(gT)
                for el in ET_attr.items():
                    q += ", " + el[0] + ': "' + el[1] + '"'
                q += "}) MATCH (eS:" + typeES + "{ graph: " + str(gS)
                for el in ES_attr.items():
                    q += ", " + el[0] + ': "' + el[1] + '"'
                q += "}) CREATE (eS) -[r:" + relName + "]-> (eT)"
                tx.run(q)
                return "OK"
            else:
                return "RELAZIONE già presente/supera il limite"


def addRelAttribute(conn: Connection, t: str, attribute: str):
    """Aggiunge un'attributo al metamodello di una relazione

    Args:
        conn (Connection): oggetto dedicato alla connessione a Neo4j
        t (str): tipo della relazione
        attribute (str): nome dell'attributo da aggiungere
    """    
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            print(
                "A new attribute named "
                + attribute
                + " will be added to relation type "
                + t
                + ". Continue?"
            )
            print("y - yes, n - no")
            flag = input()

            if flag == "y":
                typePresence = tx.run(
                    "MATCH (instance:Relazione {type: 'relation', label:'"
                    + str(t)
                    + "'}) RETURN instance"
                )
                typeValues = typePresence.values()

                if len(typeValues) == 1:
                    attrAlreadyPresent = tx.run(
                        "MATCH (instance:Relazione {type: 'relation', label:'"
                        + t
                        + "'}) -[rel:HAS]-> (attr:"
                        + attribute
                        + " {type: 'attr'}) RETURN instance, rel, attr"
                    )
                    attrPresentValues = attrAlreadyPresent.values()

                    if len(attrPresentValues) == 0:
                        attrCreate = tx.run(
                            "MATCH (type:Relazione{type: 'relation', label:'"
                            + t
                            + "'}) CREATE (type) -[rel:HAS]-> (attr:"
                            + attribute
                            + " {label: '"
                            + attribute
                            + "', type: 'attr'}) RETURN type, rel, attr"
                        )
                        attrCreate.values()

                        print(
                            "Attribute "
                            + attribute
                            + " added to entity type "
                            + t
                        )
                    else:
                        print("Attribute " + attribute + " already present.")

                else:
                    print(
                        "Problem with relation type. Number of "
                        + t
                        + " type discovered: "
                        + str(len(typeValues))
                    )

            elif flag == "n":
                print("Operation aborted.")

def alreadyExist(t1: str, t2: str, t: str, conn: Connection)-> bool:
    """funzione di utility per vedere se due metamodelli sono gia' collegati da una relazione di tipo t

    Args:
        t1 (str): nome primo metamodello
        t2 (str): nome secondo metamodello
        t (str): _description_
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se esiste gia' una relazione, False altrimenti
    """    
    q = (
        "match (t1) match (t2) where t1.label = '"
        + t1
        + "' and t2.label = '"
        + t2
        + "' match (t1) -[r:"
        + t
        + "]- (t2) return count(r) = 1"
    )
    return conn.query(q)[0][0]  # type: ignore


# per aggiungere un link tra metamodelli
# Pre-condizioni:  relType1 e relType2 devono essere stringhe indicanti un tipo di relazioni presente nei metamodelli
#                 relType deve essere una stringa che indica una relazione tra metamodelli (eg: CONTRADDITTORI)
# Post-condizioni: True se la relazione non era pre esistente e la creazione ha avuto successo, False altrimenti
def addConstraint(relType1: str, relType2: str, relType: str, conn)-> bool:
    """Aggiunge un link, con nome specificato in relType, tra metamodelli (se non esiste gia')

    Args:
        relType1 (str): nome prima relazione
        relType2 (str): nome seconda relazione
        relType (str): nome link da aggiungere
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se e' stato possibile aggiungerlo, False altrimenti
    """    
    if not alreadyExist(relType1, relType2, relType, conn):
        q = (
            "match (t1) match (t2) where t1.label = '"
            + relType1
            + "' and t2.label = '"
            + relType2
            + "' create (t1) -[r:"
            + relType
            + "]-> (t2) return count(r) = 1"
        )
        return conn.query(q)[0][0]  # type: ignore
    return False

def getContraddictory(par, t: int, conn: Connection)-> list:
    """Ottiene relazioni contraddittorie

    Args:
        par (int or str): id dell'entita' di destinazione or tipo di relazione
        t (int): specifica dove cercare, 0 per entita' o 1 per relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        ValueError: t != 0 and t != 1

    Returns:
        list: lista di relazioni contraddittorie per l'entita' o la relazione data
    """    
    if t == 1:  # tipo di relazione
        q = (
            "match (e1) where e1.label = '"
            + par
            + "' match (e1) -[r:CONTRADDITTORI]- (e2) return e2.label as tipo"
        )
    elif t == 0:  # id di entita' di relazione
        q = (
            "match (e) <-[r]- () where id(e) = "
            + str(par)
            + " with type(r) as t match (e) -[:CONTRADDITTORI]- (c) where e.label = t return c.label as tipo"
        )
    else:
        raise ValueError("Parametro t non corrisponde a nessuna possibile opzione:", t)
    res = conn.query(q)
    l = list()
    while len(res) > 0:  # type: ignore
        l.append(res.pop().get("tipo"))  # type: ignore

    return l

def srcCheck(entSrc: int, entDst: int, rel: str, conn: Connection)-> bool:
    """Controlla se esiste rel tra le due entita'

    Args:
        entSrc (int): id dell'entita' di destinazione
        entDst (int): id dell'entita' di destinazione
        rel (str): relazione da controllare
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se esiste, False altrimenti
    """    
    q = (
        "match (e1) -[r:"
        + rel
        + "]-> (e2) where id(e1) = "
        + str(entSrc)
        + " and id(e2) = "
        + str(entDst)
        + " return count(r) > 0"
    )
    return conn.query(q)[0][0]  # type: ignore


def alreadyLinked(entSrc : int, entDst: int, rel: str, conn: Connection)-> bool:
    """Controlla se esiste rel tra le due entita'

    Args:
        entSrc (int): id dell'entita' di destinazione
        entDst (int): id dell'entita' di destinazione
        rel (str): relazione da controllare
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se esiste, False altrimenti
    """ 
    q = (
        "match (e1) -[r:"
        + rel
        + "]-> (e2) where id(e1) = "
        + str(entSrc)
        + " and id(e2) = "
        + str(entDst)
        + " return count(r) > 0"
    )
    return conn.query(q)[0][0]  # type: ignore


def checkInsertion(entSrc: int, entDst: int, rel: str, conn: Connection)-> bool:
    """Controlla che non avvengano inserimenti contraddittori / non sia gia' presente

    Args:
        entSrc (int): deve essere un intero indicante un'entita' esistente all'interno del db
        entDst (int): deve essere un intero indicante un'entita' esistente all'interno del db
        rel (str): deve essere una stringa rappresentate una relazione che ha un metamodello definito
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se inseribile, False altrimenti
    """    
    if alreadyLinked(entSrc, entDst, rel, conn):
        return False
    
    presentContr = getContraddictory(rel, 1, conn)  
    # ottengo tutte le relazioni in contraddizioni con quella da inserire

    for p in presentContr: # si controlla se nell'entita' sorgente e' presente questa relazione in contraddizione con quella da inserire
        if alreadyLinked(entSrc, entDst, p, conn):
            return False

    return True


# funzione inserita in relationMatching per il controllo delle contraddizioni dirette/secche
# i parametri sono i due tipi di relazione estratti dai for innestati, in caso l'uno compaia nella lista dell'altro e' contraddittorio
def areDirectlyContraddictory(relType1, relType2, idR1, idR2, conn: Connection)-> bool:
    if sameSource(idR1, idR2, conn):
        g1 = getContraddictory(relType1, 1, conn)
        for el in g1:
            if el == relType2:
                return True
    return False

def create_relation_with_attribute(typeES: str, ES_attr: dict, gS, typeET: str, ET_attr: dict, gT, relName: str, relAttr: dict, conn: Connection)-> str:
    """Crea, se possibile, una relazione tra l'entita' sorgente e quella destinazione, riconosciute tramite i parametri passati, con nome e con attributi specificati

    Args:
        typeES (str): tipo dell'entita' sorgente 
        ES_attr (dict): key-value attributes sorgente
        gS (int or str): grafo sorgente
        typeET (str): tipo dell'entita' destinazione
        ET_attr (dict): key-value attributes destinazione
        gT (int or str): grafo destinazione
        relName (str): nome della relazione
        relAttr (dict): attributi associati alla relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        str: OK se non ci sono errori
    """ 
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:  # type: ignore
        with session.begin_transaction() as tx:
            if checkInsertion(
                getId(typeES, ES_attr, gS, conn),
                getId(typeET, ET_attr, gT, conn),
                relName,
                conn,
            ):
                return "RELAZIONE in contraddizione diretta con un'altra pre esistente"
            elif canCreate(typeET, ET_attr, gT, relName, conn):
                q = "MATCH (eT:" + typeET + " { graph:" + str(gT)
                for el in ET_attr.items():
                    q += ", " + el[0] + ': "' + el[1] + '"'
                q += "}) MATCH (eS:" + typeES + "{ graph: " + str(gS)
                for el in ES_attr.items():
                    q += ", " + el[0] + ': "' + el[1] + '"'
                q += "}) CREATE (eS) -[r:" + relName + "{ "
                for el in relAttr.items():
                    q += el[0] + ': "' + el[1] + ", "
                q = q[:-2]
                q += " }]-> (eT)"
                tx.run(q)
                return "OK"
            else:
                return "RELAZIONE già presente/supera il limite"

# @title Utility function per integrare (almeno) le relazioni con scadenza
# per inserire relazioni con attributi devo ampliare la funzione pre-esistente, utilizzando overloading della vecchia funzione
# per controllare se non e' scaduta e se puo' essere inserita o se considerarla in analisi
def isOver(relID, conn: Connection):
    q = "match () -[r]-> () where id(r) = " + str(relID) + " return r.scadenza"
    result = conn.query(q)
    if (len(result) == 0): # type: ignore
        raise Exception("RelationID {} non ha attributo scadenza".format(relID))
    data = result.pop()[0] # type: ignore
    print(data)
    return False
