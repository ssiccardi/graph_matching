from Functions.AlgorithmUtilities import getIdenNameId, getAttrId, getLimit
from Functions.Entity import getEntityId
from Functions.Connection import Connection
from datetime import date
import neo4j

def sameTargetIden(r1, r2, conn: Connection) -> bool:
    q = ("MATCH () -[r]-> (e) WHERE id(r) = " + str(r1) + " WITH id(e) as id1 MATCH () -[r]-> (e) WHERE id(r) = " + str(r2) + " RETURN id1, id(e) as id2")
    res = conn.query(q)
    if res is None:
        raise Exception("Errore con query" + q)
    iden1, iden2 = getIdenNameId(res[0][0], conn), getIdenNameId(res[0][1], conn)
    if iden1 == iden2:
        attr1, attr2 = getAttrId(res[0][0], conn), getAttrId(res[0][1], conn)
        for i in iden1:
            if attr1.get(i) != attr2.get(i):
                return False
        return True
    return False

def sameSourceIden(r1, r2, conn: Connection) -> bool:
    q = ("MATCH (e) -[r]-> () WHERE id(r) = " + str(r1) + " WITH id(e) as id1 MATCH (e) -[r]-> () WHERE id(r) = " + str(r2) + " RETURN id1, id(e) as id2")
    res = conn.query(q)
    if res is None:
        raise Exception("Errore con query" + q)
    iden1, iden2 = getIdenNameId(res[0][0], conn), getIdenNameId(res[0][1], conn)
    if iden1 == iden2:
        attr1, attr2 = getAttrId(res[0][0], conn), getAttrId(res[0][1], conn)
        for i in iden1:
            if attr1.get(i) != attr2.get(i):
                return False
        return True
    return False;

def sameSource(r1, r2, conn: Connection)-> bool:
    """Stabilisce sue due relazioni hanno la stessa entita' sorgente sulla base degli id extra

    Args:
        r1 (int or str): id relazione
        r2 (int or str): id relazione_
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        Exception: Se la query non va a buon fine 

    Returns:
        bool: True se hanno gli stessi ID extra, False altrimenti
    """    
    q = (
        "match (e) -[r]-> () where id(r) = "
        + str(r1)
        + " with e.id as id1 match (e) -[r]-> () where id(r) = "
        + str(r2)
        + " return e.id = id1"
    )
    
    res = conn.query(q)

    if res is None:
        raise Exception("Errore con query" + q)

    return res.pop()[0] 

def sameTarget(r1, r2, conn: Connection) -> bool:
    """Stabilisce sue due relazioni hanno la stessa entita' target sulla base degli id extra

    Args:
        r1 (int or str): id relazione
        r2 (int or str): id relazione_
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        Exception: Se la query non va a buon fine 

    Returns:
        bool: True se hanno gli stessi ID extra, False altrimenti
    """    
    q = (
        "match () -[r]-> (e) where id(r) = "
        + str(r1)
        + " with e.id as id1 match () -[r]-> (e) where id(r) = "
        + str(r2)
        + " return e.id = id1"
    )
    
    res = conn.query(q)

    if res is None:
        raise Exception("Errore con query" + q)

    return res.pop()[0]  

def isFissa(t: str, conn: Connection) -> bool:
    """Capisce se la relazione e' di tipo Fisso

    Args:
        t (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se Fissa, False altrimenti
    """
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + t
        + "' and labels(something)[0] = 'Cardinalita' return something.label = '1'"
    )
    res = conn.query(q)
    if res == None:
        raise Exception("Errore per relazione di tipo {}".format(t))
    return res.pop()[0]


def isMultipla(t: str, conn: Connection) -> bool:
    """Capisce se la relazione e' di tipo Multiplo

    Args:
        t (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se Multipla, False altrimenti
    """
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + t
        + "' and labels(something)[0] = 'Cardinalita' return something.label = 'n'"
    )
    res = conn.query(q)
    if res == None:
        raise Exception("Errore per relazione di tipo {}".format(t))
    return res.pop()[0]  

def getScadute(idDst, relName: str, conn: Connection)-> int:
    """Conta il numero di relazioni di tipo indicato, che arrivano all'entita' indicata, sono scadute

    Args:
        idDst (str or int): ID dell'entita' di destinazione
        relName (str): tipo di relazione
        conn (Connection): oggetto dedicato alla connessione a Neo

    Returns:
        int: numero di relazioni di tipo relName scadute ed indirizzate ad idDst
    """
    tot = 0
    q = (
            "MATCH () -[r:"
            + relName
            + "]-> (e) WHERE id(e) = "
            + str(idDst)
            + " return id(r)"
        )
    res = conn.query(q)

    if res == None:
        return 0
    
    while len(res) > 0: 
        if isOver(res.pop()[0], conn):
            tot += 1
    
    return tot

def canCreate(idDst, relName: str, conn: Connection, scadenza = None) -> bool:
    """Capisce se la relazione tra le due entita' puo' essere creata. Quindi si chiede se tra le due e' gia' presente la relazione, se attiverebbe contraddizioni e cosi' via

    Args:
        idDst(int or str): id dell'entita' di destinazione
        relName (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se passa tutti i controlli, False altrimenti
    """
    if scadenza is not None:
        scadenza = scadenza.split(scadenza[2:3])
        if date(int(scadenza[2]), int(scadenza[1]), int(scadenza[0])) < date.today():
            return True
    if not isMultipla(relName, conn):
        q = (
            "MATCH () -[r:"
            + relName
            + "]-> (e) WHERE id(e) = "
            + str(idDst)
            + " return count(r)"
        )

        if isFissa(relName, conn):
            q += " = " + str(1 + getScadute(idDst, relName, conn))
        else:
            q += " = " + str(getLimit(relName, conn) + getScadute(idDst, relName, conn))

        res = conn.query(q)

        if res == None:
            raise Exception("Errore con entita' {} e relazione di tipo {}".format(idDst, relName))

        return not res[0][0] 
    return True


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
                    + "'}) RETURN instance" # type: ignore
                )
                typeValues = typePresence.values()

                if len(typeValues) == 1:
                    attrAlreadyPresent = tx.run(
                        "MATCH (instance:Relazione {type: 'relation', label:'"
                        + t
                        + "'}) -[rel:HAS]-> (attr:"
                        + attribute
                        + " {type: 'attr'}) RETURN instance, rel, attr" # type: ignore
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
                            + "', type: 'attr'}) RETURN type, rel, attr" # type: ignore
                        )
                        attrCreate.values()

                        print("Attribute " + attribute + " added to entity type " + t)
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


def alreadyExist(t1: str, t2: str, t: str, conn: Connection) -> bool:
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
    res = conn.query(q)

    if res == None:
        raise Exception("Errore tra metamodello {} e {} con nuova relazione {}".format(t1, t2, t))

    return res[0][0]  


def addConstraint(relType1: str, relType2: str, relType: str, conn) -> bool:
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

        res = conn.query(q)

        if res == None:
            raise Exception("Errore tra metamodello {} e {} con nuova relazione {}".format(relType1, relType2, relType))

        return res[0][0]  
    return False


def getContraddictory(par, t: int, conn: Connection) -> list:
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

    if res == None:
        raise Exception("Errore con" + par)

    l = list()
    while len(res) > 0:  
        l.append(res.pop().get("tipo"))  

    return l


def srcCheck(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
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

    res = conn.query(q)

    if res == None:
        raise Exception("Errore con entita' sorgente {}, destinazione {} e relazione {}".format(entSrc, entDst, rel))

    return res[0][0] 


def alreadyLinked(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
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
    
    res = conn.query(q)

    if res == None:
        raise Exception("Errore con entita' sorgente {}, destinazione {} e relazione {}".format(entSrc, entDst, rel))

    return res[0][0] 

def checkInsertion(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
    """Controlla che non avvengano inserimenti contraddittori (o non sia gia' presente)

    Args:
        entSrc (int): deve essere un intero indicante un'entita' esistente all'interno del db
        entDst (int): deve essere un intero indicante un'entita' esistente all'interno del db
        rel (str): deve essere una stringa rappresentate una relazione che ha un metamodello definito
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se esiste, False altrimenti
    """
    if alreadyLinked(entSrc, entDst, rel, conn):
        return False

    presentContr = getContraddictory(rel, 1, conn)
    #ottengo tutte le relazioni in contraddizioni con quella da inserire

    for p in presentContr:  # si controlla se nell'entita' sorgente e' presente questa relazione in contraddizione con quella da inserire
        if alreadyLinked(entSrc, entDst, p, conn):
            return False

    return True

def areDirectlyContraddictory(relType1: str, relType2:str, idR1, idR2, conn: Connection) -> bool:
    #SOLO PER ENTRANTI
    if relType1 == relType2 or not sameSourceIden(idR1, idR2, conn):
        return False
    
    return getContraddictory(relType1, 1, conn).__contains__(relType2)

def create_relation_dir(typeES: str, ES_attr: dict, gS, typeET: str, ET_attr: dict, gT, relName: str, conn: Connection) -> str:
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
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:  
        with session.begin_transaction() as tx:
            idSrc, idDst = (
                getEntityId(typeES, ES_attr, gS, conn),
                getEntityId(typeET, ET_attr, gT, conn),
            )
            if not checkInsertion(
                idSrc,
                idDst,
                relName,
                conn
            ):
                return "RELAZIONE in contraddizione diretta con un'altra pre esistente"
            elif canCreate(idDst, relName, conn):
                q = (
                    "MATCH (eT) WHERE id(eT) = "
                    + str(idDst)
                    + " MATCH (eS) WHERE id(eS) = "
                    + str(idSrc)
                    + " CREATE (eS) -[r:"
                    + relName
                    + "]-> (eT)"
                )
                tx.run(q) # type: ignore
                return "OK"
            else:
                return "RELAZIONE già presente/supera il limite"


def create_relation_with_attribute(typeES: str, ES_attr: dict, gS, typeET: str, ET_attr: dict, gT, relName: str, relAttr: dict, conn: Connection) -> str:
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
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:  
        with session.begin_transaction() as tx:
            idSrc, idDst = (
                getEntityId(typeES, ES_attr, gS, conn),
                getEntityId(typeET, ET_attr, gT, conn),
            )
            if not checkInsertion(
                idSrc,
                idDst,
                relName,
                conn,
            ):
                return "RELAZIONE in contraddizione diretta con un'altra pre esistente"
            elif canCreate(idDst, relName, conn, relAttr["scadenza"]):
                q = (
                    "MATCH (eT) WHERE id(eT) = "
                    + str(idDst)
                    + " MATCH (eS) WHERE id(eS) = "
                    + str(idSrc)
                    + " CREATE (eS) -[r:"
                    + relName
                    + " {"
                )
                for el in relAttr.items():
                    q += el[0] + ': "' + el[1] + '", '
                q = q[:-2]
                q += " }]-> (eT)"
                tx.run(q) # type: ignore
                return "OK"
            else:
                return "RELAZIONE già presente/supera il limite"

def isOver(relID, conn: Connection):
    """Controlla se la relazione e' scaduta

    Args:
        relID (str or int): ID della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        Exception: Se la relazione non ha scadenza

    Returns:
        bool: True se scaduta, False altrimenti
    """
    q = "match () -[r]-> () where id(r) = " + str(relID) + " return r.scadenza"

    result = conn.query(q)

    if result == None or len(result) == 0:  
        raise Exception("RelationID {} non ha attributo scadenza".format(relID))

    data = result.pop()[0]  

    if data == None:
        return False

    data = data.split(data[2:3])

    return date(int(data[2]), int(data[1]), int(data[0])) < date.today()
