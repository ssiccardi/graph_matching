from Functions.Relation import getLimit, isSemiFissa

# @title Matching di entità
def isNode(el):
    return str(type(el)) == "<class 'neo4j.graph.Node'>"


def whichGraph(g):
    if g == "G1":
        return "p.graph = 1 and "
    elif g == "G2":
        return "p.graph = 2 and "
    raise Exception("Errore con variabile", g, " -- Valore non ammesso")


# @param(ideng) = {key:value, ...}
# @param(g) = "G1" or "G2"
def getAttr(ideng, g, conn):  # ritorna una lista di chiavi valori
    d = {}
    q = (
        "match (p) where "
        + whichGraph(g)
        + "p.id = "
        + str(ideng)
        + " return properties(p)"
    )

    result = conn.query(q)  # type: ignore

    if len(result) < 1:  # type: ignore
        return d

    result = result.pop()  # type: ignore
    result = result.get("properties(p)")
    for e in result:  # itera sulle KEYS e poi estrapola dal nodo tramite key
        if e != "graph" and e != "id":
            d[e] = result.get(e)
    return dict(sorted(d.items()))  # ORA RITORNA UN DIZIONARIO


def getIdenName(ideng, g, conn):
    l = list()
    q = (
        "match (p) where "
        + whichGraph(g)
        + "p.id = "
        + str(ideng)
        + " return labels(p)"
    )
    result = conn.query(q)  # type: ignore
    if len(result) == 0:
        return l
    res = result.pop()[0][0]  # type: ignore
    q = (
        "match (:"
        + res
        + ") -[:IDENTIFIED]-> (:Identifier) -[:IDENTIFIED_BY]-> (p) return p.label as iden"
    )
    result = conn.query(q)  # type: ignore
    for res in result:  # type: ignore
        l.append(res[0])
    l.sort()
    return l


def canProceed(ideng, conn):
    # PARTI DA PRESUPPOSTO entita' abbiano un codice identificativo e che quindi in input ci sia solo un ideng
    return conn.query("MATCH (e) WHERE e.id = " + str(ideng) + " RETURN COUNT(e) as ents")[0][0] == 2  # type: ignore


def retrieveInfos(toExaminG1, toExaminG2, attrG1, attrG2):
    toPrint = "Entita' in G1: { "
    for el in toExaminG1:
        toPrint += str(el) + ":" + str(attrG1.get(el)) + ", "
    toPrint = toPrint[:-2]
    toPrint += "}\nEntita' in G2: { "
    for el in toExaminG2:
        toPrint += str(el) + ":" + str(attrG2.get(el)) + ", "
    toPrint = toPrint[:-2]
    toPrint += "}"
    return toPrint


def removeAttr(attr, rem):
    for r in rem:
        attr.pop(r)


# @title Utility per relazioni

# Data una lista di relazioni, ritorna solo le SemiFisse
def onlySemi(lista, conn):
    l = list()
    for el in lista:
        if isSemiFissa(el.get("tipo"), conn):
            l.append(el)
    return l


# Data una lista di relazioni, elimina le SemiFisse
def deleteSemi(lista, conn):
    l = list()
    for el in lista:
        if not isSemiFissa(el.get("tipo"), conn):
            l.append(el)
    return l


# Dato id di entita', grafo e direzione delle relazioni (partenti/entranti) ritorna la lista delle relazioni semifisse ad essa collegate
def getSemi(id, grafo, direzione, conn):
    l = list()
    q = "MATCH "
    if direzione == 0:
        q += "(e) -[r]-> () "
    else:
        q += "() -[r]-> (e) "
    q += (
        "WHERE e.graph = "
        + str(grafo)
        + " AND e.id = "
        + str(id)
        + " RETURN id(r) as id, type(r) as tipo, id(startNode(r)) as da, id(endNode(r)) as a"
    )
    result = conn.query(q)  # type: ignore

    while len(result) != 0:  # type: ignore
        res = result.pop()  # type: ignore
        l.append(
            {
                "id": res.get("id"),
                "tipo": res.get("tipo"),
                "da": res.get("da"),
                "a": res.get("a"),
            }
        )

    return onlySemi(l, conn)


# @param(id) id_ent
# @param(grafo) numero che indica in quale grafo prendere le relazioni
# @param(direzione) numero che indica la direzione, 0 --> / 1 <--
# return --> lista di relazioni direzionate da o per id nel grafo specificato
def getRel(id, grafo, direzione, conn):
    l = list()
    q = "MATCH "
    if direzione == 0:
        q += "(e) -[r]-> () "
    else:
        q += "() -[r]-> (e) "
    q += (
        "WHERE e.graph = "
        + str(grafo)
        + " AND e.id = "
        + str(id)
        + " RETURN id(r) as id, type(r) as tipo, id(startNode(r)) as da, id(endNode(r)) as a"
    )
    result = conn.query(q)  # type: ignore

    while len(result) != 0:  # type: ignore
        res = result.pop()  # type: ignore
        l.append(
            {
                "id": res.get("id"),
                "tipo": res.get("tipo"),
                "da": res.get("da"),
                "a": res.get("a"),
            }
        )

    return deleteSemi(l, conn)


def getDir(d):
    if d == 0:
        return "(e) -[r]-> () "
    return "() -[r]-> (e) "


# @param(r1, r2) id delle relazioni
# return --> true se la relazione e' dello stesso tipo, nome e direzione, false altrimenti
def sameRel(r1, r2, id, direzione, conn):
    q = (
        "MATCH "
        + getDir(direzione)
        + "where id(r) = "
        + str(r1)
        + " and e.id = "
        + str(id)
        + " with r as ee match "
        + getDir(direzione)
        + " where id(r) = "
        + str(r2)
        + " and e.id = "
        + str(id)
        + " return type(r) = type(ee)"
    )
    return conn.query(q).pop()[0]  # type: ignore


# @param(r1, r2) id delle relazioni
# return --> true se la relazione ha la stessa entita' di arrivo, false altrimenti
def sameTarget(r1, r2, conn):
    q = (
        "match () -[r]-> (e) where id(r) = "
        + str(r1)
        + " with e.id as id1 match () -[r]-> (e) where id(r) = "
        + str(r2)
        + " return e.id = id1"
    )
    return conn.query(q).pop()[0]  # type: ignore


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


# crea stringhe dove segnali coincidenze o complementarità' se non sopra limite, contraddittorietà' altrimenti
def overLimit(tipo, val, l1, l2, conn):
    l = list()
    if val > getLimit(tipo, conn):
        l.append(
            "Relazione di tipo "
            + tipo
            + " contraddittoria, nei due grafi esplorati esistono ben "
            + str(val)
            + " di queste relazioni"
        )
    else:
        l.append("Relazione di tipo " + tipo + " corretta")
    return l


# crea dizionario di tipi presenti inizializzato a 0 per ogni tipo
def createTypeBucket(relL1, relL2):
    d = dict()
    for r in relL1:
        d[r.get("tipo")] = 0

    for r in relL2:
        d[r.get("tipo")] = 0
    return d
