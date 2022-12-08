import neo4j


# @param(r1, r2) id delle relazioni
# return --> true se la relazione ha la stessa entita' di partenza, false altrimenti
def sameSource(r1, r2, conn):
    q = (
        "match (e) -[r]-> () where id(r) = "
        + str(r1)
        + " with e.id as id1 match (e) -[r]-> () where id(r) = "
        + str(r2)
        + " return e.id = id1"
    )
    return conn.query(q).pop()[0]  # type: ignore


# @title Funzione di creazione relazioni
def getLimit(tipo, conn):
    q = (
        "MATCH (e) -[:HAS]-> (ee) WHERE e.label ='"
        + tipo
        + "' and labels(ee)[0] = 'Cardinalita' return properties(ee).label"
    )
    return int(conn.query(q).pop()[0])  # type: ignore


# @param(tipo) il nome per trovarla nel metamodello
# return --> true se la relazione e' di tipo SemiFisso, false altrimenti
def isSemiFissa(tipo, conn):
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + tipo
        + "' and labels(something)[0] = 'Cardinalita' return something.label <> '1' and something.label <> 'n'"
    )
    return conn.query(q).pop()[0]  # type: ignore


# @param(tipo) il nome per trovarla nel metamodello
# return --> true se la relazione e' di tipo Fisso, false altrimenti
def isFissa(tipo, conn):
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + tipo
        + "' and labels(something)[0] = 'Cardinalita' return something.label = '1'"
    )
    return conn.query(q).pop()[0]  # type: ignore


def isMultipla(tipo, conn):
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + tipo
        + "' and labels(something)[0] = 'Cardinalita' return something.label = 'n'"
    )
    return conn.query(q).pop()[0]  # type: ignore


def canCreate(tipoT, attrT, grafoT, relName, conn):
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
        res = conn.query(q)  # fai un test!
        return not res[0][0]  # type: ignore
    return True


def getId(t, attr, g, conn):  # tipo, dizionario attributi, grafo
    q = "MATCH (e:" + t + " { graph:" + str(g)
    for el in attr.items():
        q += ", " + el[0] + ': "' + el[1] + '"'
    q += "}) RETURN id(e)"
    return conn.query(q)[0][0]  # type: ignore


# ES_attr && ET_attr --> dictionaries
def create_relation_dir(typeES, ES_attr, gS, typeET, ET_attr, gT, relName, conn):
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


# @title Aggiungere attributo a metamodello relazione esistente: [SKIP]
# AGGIUNGERE ATTRIBUTI
def addRelAttribute(conn, t, attribute):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            print(
                "A new attribute named "
                + str(attribute)
                + " will be added to relation type "
                + str(t)
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
                        + str(t)
                        + "'}) -[rel:HAS]-> (attr:"
                        + str(attribute)
                        + " {type: 'attr'}) RETURN instance, rel, attr"
                    )
                    attrPresentValues = attrAlreadyPresent.values()

                    if len(attrPresentValues) == 0:
                        attrCreate = tx.run(
                            "MATCH (type:Relazione{type: 'relation', label:'"
                            + str(t)
                            + "'}) CREATE (type) -[rel:HAS]-> (attr:"
                            + str(attribute)
                            + " {label: '"
                            + str(attribute)
                            + "', type: 'attr'}) RETURN type, rel, attr"
                        )
                        attrCreate.values()

                        print(
                            "Attribute "
                            + str(attribute)
                            + " added to entity type "
                            + str(t)
                        )
                    else:
                        print("Attribute " + str(attribute) + " already present.")

                else:
                    print(
                        "Problem with relation type. Number of "
                        + str(t)
                        + " type discovered: "
                        + str(len(typeValues))
                    )

            elif flag == "n":
                print("Operation aborted.")


# @title Utility function per integrare contraddizioni dirette

# funzione di utility per vedere se due metamodelli sono gia' collegati da una relazione di tipo t
# Pre-condizioni: t1, t2, t devono essere stringhe
# Post-condizioni: True se esiste gia' una relazione, False altrimenti
def alreadyExist(t1: str, t2: str, t: str, conn):
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
def addConstraint(relType1: str, relType2: str, relType: str, conn):
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


# ottieni attributi contraddittori
# Pre-condizioni: t == 0 --> par e' id di entita' di destinazione || t == 1 --> par e' tipo di relazione
# Post-condizioni: ottieni una lista di relazioni possibilmente contraddittorie
def getContraddictory(par, t: int, conn):
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


# Controlla se esiste rel tra le due entita'
def srcCheck(entSrc: int, entDst: int, rel: str, conn):
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


# per controllare che non avvengano inserimenti contraddittori
# Pre-condizioni:  entSrc deve essere un intero indicante un'entita' esistente all'interno del db
#                 entDst deve essere un intero indicante un'entita' esistente all'interno del db
#                 rel deve essere una stringa rappresentate una relazione che ha un metamodello definito
# Post-condizioni: True se l'inserimento puo' avvenire, False altrimenti
def checkInsertion(entSrc: int, entDst: int, rel: str, conn):
    presentContr = getContraddictory(
        rel, 1, conn
    )  # ottengo tutte le relazioni in contraddizioni con quella da inserire

    for p in presentContr:
        # si controlla se nell'entita' sorgente e' presente questa relazione in contraddizione con quella da inserire
        if srcCheck(entSrc, entDst, p, conn):
            return False

    return True


# funzione inserita in relationMatching per il controllo delle contraddizioni dirette/secche
# i parametri sono i due tipi di relazione estratti dai for innestati, in caso l'uno compaia nella lista dell'altro e' contraddittorio
def areDirectlyContraddictory(relType1, relType2, idR1, idR2, conn):
    if sameSource(idR1, idR2, conn):
        g1 = getContraddictory(relType1, 1, conn)
        for el in g1:
            if el == relType2:
                return True
        return False


# @title Utility function per integrare (almeno) le relazioni con scadenza

# per inserire relazioni con attributi devo ampliare la funzione pre-esistente, utilizzando overloading della vecchia funzione

# per controllare se non e' scaduta e se puo' essere inserita o se considerarla in analisi
def isOver(relID, conn):
    # TODO
    return False
