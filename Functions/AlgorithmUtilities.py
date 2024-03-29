from Functions.Connection import Connection
import pandas as pd 

def removeExpired(lst: list, rmv:  list):
    """Rimuove tutti gli attributi presenti in rmv da lst e pulisce rmv

    Args:
        lst (list): lista da cui togliere elementi
        rmv (list): lista con elementi da togliere
    """    
    for r in rmv:
        lst.remove(r)
    rmv.clear()

def _whichGraph(g):
    if g == "G1":
        return "p.graph = 1 and "
    elif g == "G2":
        return "p.graph = 2 and "
    raise Exception("Errore con variabile", g, " -- Valore non ammesso")

def getLimit(t: str, conn: Connection) -> int:
    """Ottiene la Cardinalita per una relazione semifissa

    Args:
        t (str): nome della relazione
        conn (Connectio): oggetto dedicato alla connessione a Neo4j

    Returns:
        int: Cardinalita relazione se presente, ?unknown? altrimenti
    """
    q = (
        "MATCH (e) -[:HAS]-> (ee) WHERE e.label ='"
        + t
        + "' and labels(ee)[0] = 'Cardinalita' return properties(ee).label"
    )
    res = conn.query(q)
    if res == None:
        raise Exception("Errore per relazione di tipo {}".format(t))
    return int(res.pop()[0])

def _isSemiFissa(t: str, conn: Connection) -> bool:
    """Capisce se la relazione e' di tipo SemiFisso

    Args:
        t (str): nome della relazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se SemiFissa, False altrimenti
    """
    q = (
        "match (e) -[:HAS]-> (something) where e.label = '"
        + t
        + "' and labels(something)[0] = 'Cardinalita' return something.label <> '1' and something.label <> 'n'"
    )
    
    res = conn.query(q)
    if res == None:
        raise Exception("Errore per relazione di tipo {}".format(t))
    return res.pop()[0]  

def getAttrId(id, conn: Connection) -> dict:
    """Ritorna una lista di chiavi valori con gli attributi

    Args:
        id (int): id dell'entità dato da AuraDB
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        Exception: segnala errore nella query

    Returns:
        dict: attributi chiave-valore
    """    
    d = {}
    q = (
        "match (p) where "
        + "id(p) = "
        + str(id)
        + " return properties(p)"
    )

    result = conn.query(q) 

    if result is None:
        raise Exception("Errore con query" + q)

    if len(result) < 1:  
        return d

    result = result.pop()  
    result = result.get("properties(p)")

    for e in result:  # itera sulle KEYS e poi estrapola dal nodo tramite key
        if e != "graph" and e != "id":
            d[e] = result.get(e)
    
    return dict(sorted(d.items()))  # ORA RITORNA UN DIZIONARIO

def getAttr(ideng, g, conn: Connection):  
    """Ritorna una lista di chiavi valori con gli attributi

    Args:
        ideng (int): id dell'entita'
        g (str): grafo da cui prendere gli attributi
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        dict: attributi chiave-valore
    """    
    d = {}
    q = (
        "match (p) where "
        + _whichGraph(g)
        + "p.id = "
        + str(ideng)
        + " return properties(p), id(p), labels(p) as tipo"
    )

    result = conn.query(q) 

    if result is None:
        raise Exception("Errore con query" + q)

    if len(result) < 1:  
        return d
    
    d["tipo"] = result.__getitem__(0).get("tipo")[0]
    d["idDB"] = result.__getitem__(0).get("id(p)")
    result = result.__getitem__(0).get("properties(p)")
    for e in result:  # itera sulle KEYS e poi estrapola dal nodo tramite key
        if e != "graph" and e != "id":
            d[e] = result.get(e)
    return dict(sorted(d.items()))  # ORA RITORNA UN DIZIONARIO

def getIdenNameId(id, conn: Connection) -> list:
    """Ritorna una lista di attributi identitari

    Args:
        id (int): id dell'entita' dato da AuraDB
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        list: attributi identitari
    """    
    l = list()
    q = (
        "match (p) where "
        + "id(p) = "
        + str(id)
        + " return labels(p)"
    )
    result = conn.query(q)  

    if result is None:
        raise Exception("Errore con query" + q)

    if len(result) == 0:
        return l
        
    res = result.pop()[0][0]  
    q = (
        "match (:"
        + res
        + ") -[:IDENTIFIED]-> (:Identifier) -[:IDENTIFIED_BY]-> (p) return p.label as iden"
    )
    result = conn.query(q)  

    if result is None:
        raise Exception("Errore con query" + q)

    for res in result:  
        l.append(res[0])
    l.sort()
    return l

def getIdenName(ideng, g, conn : Connection):
    """Ritorna una lista di attributi identitari

    Args:
        ideng (int): id dell'entita'
        g (str): grafo da cui prendere gli attributi
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        list: attributi identitari
    """    
    l = list()
    q = (
        "match (p) where "
        + _whichGraph(g)
        + "p.id = "
        + str(ideng)
        + " return labels(p)"
    )
    result = conn.query(q)  

    if result is None:
        raise Exception("Errore con query" + q)

    if len(result) == 0:
        return l
        
    res = result.pop()[0][0]  
    q = (
        "match (:"
        + res
        + ") -[:IDENTIFIED]-> (:Identifier) -[:IDENTIFIED_BY]-> (p) return p.label as iden"
    )
    result = conn.query(q)  

    if result is None:
        raise Exception("Errore con query" + q)

    for res in result:  
        l.append(res[0])
    l.sort()
    return l

def canProceed(ideng, conn: Connection):
    """Controlla se le istanze delle Entità identificate dall'id esistono

    Args:
        ideng (int or str): id dato dal sistema alle entità nei due grafi diversi 
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """    
    # PARTI DA PRESUPPOSTO entita' abbiano un codice identificativo 
    # e che quindi in input ci sia solo un ideng
    res = conn.query("MATCH (e) WHERE e.id = " + str(ideng) + " RETURN COUNT(e) as ents")
    
    if res is None:
        raise Exception("Errore con" + ideng)
    
    return res[0][0] == 2  

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
    """Rimuove attributi contenuti in rem da attr

    Args:
        attr (_type_): attributi
        rem (_type_): attributi da rimuovere
    """    
    for r in rem:
        attr.pop(r)

def _onlySemi(lista, conn: Connection):
    """Filtra le relazioni non SemiFisse

    Args:
        lista (list): lista di relazioni
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        list: lista di relazioni SemiFisse
    """    
    l = list()
    for el in lista:
        if _isSemiFissa(el.get("tipo"), conn):
            l.append(el)
    return l

def _deleteSemi(lista, conn: Connection):
    """Filtra le relazioni SemiFisse

    Args:
        lista (list): lista di relazioni
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        list: lista di relazioni SemiFisse
    """    
    l = list()
    for el in lista:
        if not _isSemiFissa(el.get("tipo"), conn):
            l.append(el)
    return l

def getSemi(id: int, grafo: int, direzione: int, conn: Connection) -> list :
    """Dati i parametri restituisce la lista delle relazioni di tipo SemiFisso ad essa collegate

    Args:
        id (int): identifica l'istanza
        grafo (int): indica il grafo a cui ppartiene l'istanza identificata tramite id
        direzione (int): se 0 implica entità sorgente, se 1 implica entità destinazione
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Raises:
        Exception: in caso la query non vada a buon fine

    Returns:
        list: lista di relazioni SemiFisse associate all'istanza specificata in input
    """    
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
    result = conn.query(q)  

    if result is None:
        raise Exception("Errore con query" + q)

    while len(result) != 0: 
        res = result.pop()  
        l.append(
            {
                "id": res.get("id"),
                "tipo": res.get("tipo"),
                "da": res.get("da"),
                "a": res.get("a"),
            }
        )

    return _onlySemi(l, conn)

def getRel(id, grafo, direzione: int, conn: Connection)-> list:
    """Restituisce la lista delle relazioni (non SemiFisse) associate ad un istanza di Entità specificata

    Args:
        id (int or str): identificatore dell'istanza dato dal sistema
        grafo (int or str): grafo di  appartenenenza dell'istanza
        direzione (int): 0 se l'entità è sorgente, 1 se è destinazione
        conn (Connection): oggett dedicato alla connessione a Neo4j

    Raises:
        Exception: se la query non va a buon fine

    Returns:
        list: lista di relazioni (non SemiFisse) 
    """    
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
    
    result = conn.query(q) 
    
    if result is None:
        raise Exception("Errore con query" + q)

    while len(result) != 0:  
        res = result.pop()  
        l.append(
            {
                "id": res.get("id"),
                "tipo": res.get("tipo"),
                "da": res.get("da"),
                "a": res.get("a"),
            }
        )

    return _deleteSemi(l, conn)

def _getDir(d: int):
    if d == 0:
        return "(e) -[r]-> () "
    return "() -[r]-> (e) "

def sameRel(r1, r2, id, direzione: int, conn: Connection):
    """Stabilisce se due relazioni sono uguali

    Args:
        r1 (int or str): id di Neo4j per relazione
        r2 (int or str): id di Neo4j per relazione
        id (int or str): id dato dal sistema per l'istanza di Entità
        direzione (int): 0 se l'entità è sorgente, 1 se è destinazione
        conn (Connection): oggetto dedicato alla connessione con Neo4j

    Raises:
        Exception: se la query non va a buon fine

    Returns:
        bool: True se le relazioni sono dello stesso tipo, nome e direzione, False altrimenti
    """    
    q = (
        "MATCH "
        + _getDir(direzione)
        + "where id(r) = "
        + str(r1)
        + " and e.id = "
        + str(id)
        + " with r as rr match "
        + _getDir(direzione)
        + " where id(r) = "
        + str(r2)
        + " and e.id = "
        + str(id)
        + " return type(r) = type(rr)"
    )

    res = conn.query(q)

    if res is None:
        raise Exception("Errore con query" + q)

    return res.pop()[0]  

def toStr(l : list[str])-> str:
    s = "\n"
    for el in l: s += el + "\n"
    return s

def overLimit(tipo: str, val, conn: Connection)-> list:
    """Ritorna una lista di stringhe che descrivono lo stato delle relazioni SemiFisse considerate

    Args:
        tipo (str): tipo della relazione
        val (int or str): Valore limite associato a tipo
        conn (Connection): oggetto dedicato alla connessione con Neo4j

    Returns:
        list: stringhe che descrivono lo stato delle relazioni considerate
    """    
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


def createTypeBucket(relL1: list, relL2: list)-> dict[str, int]:
    """Crea un dizionario di tipi presenti nelle due liste

    Args:
        relL1 (list): lista di relazioni come stringhe
        relL2 (list): lista di relazioni come stringh

    Returns:
        dict[str, int]: dizionario con relazioni come chiavi e 0 come valore
    """    
    d = dict()
    for r in relL1:
        d[r.get("tipo")] = 0

    for r in relL2:
        d[r.get("tipo")] = 0
    return d

def updateDF_Entity(cfr: str, typeEnt: str = " ", id1: int = -1, id2: int = -1, typeAttr1: str = " ", 
                    typeAttr2: str = " ", valueAttr1: str = " ", valueAttr2: str = " ")-> pd.DataFrame :
    return pd.DataFrame({
            "Descrizione confronto attributo" : [cfr],
            "Tipo Entità" :  [typeEnt], "ID Entità Grafo1" : [id1], 
            "Tipo attributo Entità Grafo1" : [typeAttr1], "Attributo Entità Grafo1" : [valueAttr1],
            "ID Entità Grafo2" : [id2], 
            "Tipo attributo Entità Grafo2" : [typeAttr2], "Attributo Entità Grafo2" : [valueAttr2]
    })
    
def updateDF(ril: str, src: dict = dict(), dst: dict = dict(), rel1: int = -1, rel2: int = -1, tipo1: str = "", tipo2: str = "")-> pd.DataFrame:
    l = []
    s = ""
    if src != dict():
        for key in src.keys(): s += str(key) + " : " + str(src.get(key)) + " -- "
    l.append(s) 
    s = ""
    if dst != dict():
        for key in dst.keys(): s += str(key) + " : " + str(dst.get(key)) + " -- "
    l.append(s) 

    return pd.DataFrame({
        "Tipo" : [ril],
        "IDRelazioneG1" : [rel1],
        "TipoRelG1" : [tipo1],
        "IDRelazioneG2" : [rel2],
        "TipoRelG2" : [tipo2],
        "Attr. G1" : [l[0]],
        "Attr. G2" : [l[1]]
        })