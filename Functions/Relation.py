from Functions.DbUtilities import getEntityId
from Functions.Connection import Connection
from datetime import date
import neo4j


def sameSource(r1, r2, conn: Connection) -> bool:
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


def getLimit(tipo: str, conn: Connection) -> int:
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


def isSemiFissa(tipo: str, conn: Connection) -> bool:
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


def isFissa(tipo: str, conn: Connection) -> bool:
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


def isMultipla(tipo: str, conn: Connection) -> bool:
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


def canCreate(idDst, relName: str, conn: Connection) -> bool:
    # TODO
    """Capisce se la relazione tra le due entita' puo' essere creata. Quindi si chiede se tra le due e' gia' presente la relazione, se attiverebbe contraddizioni e cosi' via

    Args:
        idDst(int or str): id dell'entita' di destinazione
        relName (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se passa tutti i controlli, False altrimenti
    """
    if not isMultipla(relName, conn):
        q = (
            "MATCH () -[r:"
            + relName
            + "]-> (e) WHERE id(e) = "
            + str(idDst)
            + " return count(r)"
        )

        if isFissa(relName, conn):
            q += " = 1"
        else:
            q += " = " + str(getLimit(relName, conn))

        res = conn.query(q)

        return not res[0][0]  # type: ignore
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
    return conn.query(q)[0][0]  # type: ignore


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
        return conn.query(q)[0][0]  # type: ignore
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
    l = list()
    while len(res) > 0:  # type: ignore
        l.append(res.pop().get("tipo"))  # type: ignore

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
    return conn.query(q)[0][0]  # type: ignore


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
    return conn.query(q)[0][0]  # type: ignore


def checkInsertion(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
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

    for (
        p
    ) in (
        presentContr
    ):  # si controlla se nell'entita' sorgente e' presente questa relazione in contraddizione con quella da inserire
        if alreadyLinked(entSrc, entDst, p, conn):
            return False

    return True


def areDirectlyContraddictory(relType1, relType2, idR1, idR2, conn: Connection) -> bool:
    if sameSource(idR1, idR2, conn):
        g1 = getContraddictory(relType1, 1, conn)
        for el in g1:
            if el == relType2:
                return True
    return False


def checkScadenza(idSrc, idDst, relName: str, conn: Connection, scadenza=None):
    """Controlla se la relazione da inserire non si sovrapponga ad un altra non ancora scaduta

    Args:
        idSrc (int or str): id dell'entita' sorgente
        idDst (int or str): id dell'entita' destinazione
        relName (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j
        scadenza (str, optional): Valore della scadenza. Defaults to None.

    Returns:
        bool: True se inseribili, False altrimenti
    """
    if scadenza is None:
        pass
    else:
        pass
    return True


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
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:  # type: ignore
        with session.begin_transaction() as tx:
            idSrc, idDst = (
                getEntityId(typeES, ES_attr, gS, conn),
                getEntityId(typeET, ET_attr, gT, conn),
            )
            if checkInsertion(
                idSrc,
                idDst,
                relName,
                conn,
            ):
                return "RELAZIONE in contraddizione diretta con un'altra pre esistente"
            elif checkScadenza(idSrc, idDst, relName, conn):
                return "RELAZIONE in contraddizione con una relazione non ancora scaduta"
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
                tx.run(q)
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
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:  # type: ignore
        with session.begin_transaction() as tx:
            idSrc, idDst = (
                getEntityId(typeES, ES_attr, gS, conn),
                getEntityId(typeET, ET_attr, gT, conn),
            )
            if checkInsertion(
                idSrc,
                idDst,
                relName,
                conn,
            ):
                return "RELAZIONE in contraddizione diretta con un'altra pre esistente"
            elif checkScadenza(idSrc, idDst, relName, conn, relAttr["scadenza"]):
                return "RELAZIONE in contraddizione con una relazione non ancora scaduta"
            elif canCreate(idDst, relName, conn):
                q = (
                    "MATCH (eT) WHERE id(eT) = "
                    + str(idDst)
                    + " MATCH (eS) WHERE id(eS) = "
                    + str(idSrc)
                    + " CREATE (eS) -[r:"
                    + relName
                    + "{"
                )
                for el in relAttr.items():
                    q += el[0] + ': "' + el[1] + ", "
                q = q[:-2]
                q += " }]-> (eT)"
                tx.run(q)
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

    if len(result) == 0:  # type: ignore
        raise Exception("RelationID {} non ha attributo scadenza".format(relID))

    data = result.pop()[0]  # type: ignore
    data = data.split(data[2:3])

    return date(int(data[2]), int(data[1]), int(data[0])) < date.today()
