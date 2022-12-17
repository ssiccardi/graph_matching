import pandas as pd
from Functions.AlgorithmUtilities import createTypeBucket, getRel, getSemi, overLimit, sameRel, sameSource, sameTarget
from Functions.Relation import areDirectlyContraddictory, isFissa
from Functions.Connection import Connection

##TODO: Controllo relazioni secche funziona?
##TODO: Controllo relazioni scadenza funziona?
##TODO: Amplia gli attributi che prendi con le get e togli confronti evitabili tramite interrogazione DB, tipo sameTarget

def getInfoSemi(id: int, conn: Connection, df: pd.DataFrame) -> pd.DataFrame:
    """Analizza le relazioni SemiFisse legate all'id passato in input, mostrando all'utente cosa nota

    Args:
        id (int): id appartenente all'entita' da analizzare\n
        conn (Connection): oggetto dedicato alla connessione a Neo4j
    """
    relP1, relP2 = getSemi(id, 1, 0, conn), getSemi(id, 2, 0, conn)  # zero analisi da fare qui
    relE1, relE2 = getSemi(id, 1, 1, conn), getSemi(id, 2, 1, conn)  # le analisi si fanno qui

    # Parte entranti:
    typeBucket = createTypeBucket(relE1, relE2)
    toRem = list()
    b = True
    for r1 in relE1:
        for r2 in relE2:
            if areDirectlyContraddictory(r1.get("tipo"), r2.get("tipo"), r1.get("id"), r2.get("id"), conn):
                print("Contraddittoria DIRETTA [{}] - [{}] -- getInfoSemi->areDirectlyContraddictoryEntranti".format(r1, r2))  # CONTRADDITTORIA
                toRem.append(r2.get("id"))
                # b = False
                # break #ora tolti
            if sameRel(r1.get("id"), r2.get("id"), id, 1, conn) and sameSource(r1.get("id"), r2.get("id"), conn):  # capisci se si può fare lo stesso usando le info disponibili in relE1 e relE2 (tipo e1.get('da') == ...)
                print("Relazione coincidente in G1 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemi->sameRelEntranti".format(r1.get("tipo"), r1.get("da"), r1.get("a")))
                typeBucket[r1.get("tipo")] += 1
                b = False
                toRem.append(r2.get("id"))
                break
        if b:
            # COMPLEMENTARI
            print("Relazione complementare in G1 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemi->if(b)Entranti".format(r1.get("tipo"), r1.get("da"), r1.get("a")))  
            typeBucket[r1.get("tipo")] += 1
        b = True
    for el in relE2:  
        if not len(toRem):
            typeBucket[el.get("tipo")] += 1
            print("Relazione complementare in G2 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemi->penultimoForEntranti".format(el.get("tipo"), el.get("da"), el.get("a")))  
        else:
            b = False
            for id in toRem:
                if id == el.get("id"):
                    b = True
            if not b:
                typeBucket[el.get("tipo")] += 1
                print("Relazione complementare in G2 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemi->penultimoForEntranti".format(el.get("tipo"), el.get("da"), el.get("a"))) 
    
    for t in typeBucket.keys():
        print("Relazione semifissa {} -- {} -- getInfoSemi-> ultimoForEntranti".format(t, overLimit(t, typeBucket.get(t), relE1, relE2, conn)))

    # Parte partenti:
    toRem = list()
    b = True
    for r1 in relP1:
        for r2 in relP2:
            if sameRel(r1.get("id"), r2.get("id"), id, 0, conn) and sameTarget(r1.get("id"), r2.get("id"), conn):  # capisci se si può fare lo stesso usando le info disponibili in relE1 e relE2 (tipo e1.get('da') == ...)
                print("Relazione coincidente in G1 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemi->sameRelPartenti".format(r1.get("tipo"), r1.get("da"), r1.get("a"))) 
                b = False
                toRem.append(r2.get("id"))
                break
        if b:
            print("Relazione complementare in G1 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemi->if(b)Partenti".format(r1.get("tipo"), r1.get("da"), r1.get("a")))  
        b = True

    for el in relP2:
        if not len(toRem):
            print("Relazione complementare in G2 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemiPartenti ultimo for".format(el.get("tipo"), el.get("da"), el.get("a")))
        else:
            b = False
            for id in toRem:
                if id == el.get("id"):
                    b = True
            if not b:
                print("Relazione complementare in G2 di tipo {} con entità di partenza id:{} e entità di arrivo id:{} -- getInfoSemiPartenti ultimo for".format(el.get("tipo"), el.get("da"), el.get("a"))) 
    return df

def relationMatching(id: int, conn: Connection):
    """Analizza le relazioni legate all'id passato in input, mostrando all'utente cosa nota\n
    PreCondizioni:
        1)Le entita' esistono e non sono contraddittorie\n
        2)Le relazioni fisse hanno subito un controllo in inserimento, non ci possono essere piu' relazioni fisse uguali appartenenti alla stessa entita' di uno stesso grafo\n
        3)Le relazioni semifisse hanno subito lo stesso controllo in inserimento!\n
    Args:
        id (int): [id appartenente all'entita' da analizzare]\n
        conn (Connection): [oggetto dedicato alla connessione a Neo4j]
    """    
    df = pd.DataFrame(data=None, index=["Rilevazione", "ID Entita' sorgente", "Attributi entita' sorgente", "Grafo sorgente", "ID Entita' destinazione", "Attributi entita' destinazione", "Grafo destinazione"])
    relP1, relP2 = getRel(id, 1, 0, conn), getRel(id, 2, 0, conn)
    relE1, relE2 = getRel(id, 1, 1, conn), getRel(id, 2, 1, conn)

    compl = None
    toRem = list()

    # PARTENTI:
    for rel1 in relP1:
        for rel2 in relP2:
            if sameRel(rel1.get("id"), rel2.get("id"), id, 0, conn):
                if sameTarget(rel1.get("id"), rel2.get("id"), conn):
                    print("Coincidente [{}] -- [{}] -- sameRel->sameTargetPartenti".format(rel1, rel2))  # COINCIDENTI
                    compl = None
                    toRem.append(rel2.get("id"))
                    break
                else:
                    compl = rel1
        if compl != None:
            print("Complementare -->", rel1)  # COMPLEMENTARE

    for rel in relP2:
        if not len(toRem):
            print("Complementare -->", rel)  # COMPLEMENTARE
        else:
            b = False
            for rem in toRem:
                if rel.get("id") == rem:
                    b = True
            if not b:
                print("Complementare -->", rel)  # COMPLEMENTARE

    # ENTRANTI:
    toRem = list()

    for rel1 in relE1:
        for rel2 in relE2:
            if areDirectlyContraddictory(rel1.get("tipo"), rel2.get("tipo"), rel1.get("id"), rel2.get("id"), conn):
                print("Contraddittoria DIRETTA [{}] - [{}] -- areDirContrPartenti".format(rel1, rel2))  # CONTRADDITTORIA
                toRem.append(rel2.get("id"))
                # compl = None
                # break #Per ora tolti
            if sameRel(rel1.get("id"), rel2.get("id"), id, 1, conn):
                if sameSource(rel1.get("id"), rel2.get("id"), conn):
                    print("Coincidente -->", rel1)  # COINCIDENTE
                    toRem.append(rel2.get("id"))
                    compl = None
                    break
                else:
                    if isFissa(rel1.get("tipo"), conn):
                        print("Contraddittoria [{}] - [{}]".format(rel1, rel2))  # CONTRADDITTORIA
                        toRem.append(rel2.get("id"))
                        compl = None
                        break
                    else:
                        compl = rel1
        if compl != None:
            print("Complementare -->", rel1)  # COMPLEMENTARE

    for rel in relE2:
        if not len(toRem):
            print("Complementare -->", rel)  # COMPLEMENTARE
        else:
            b = False
            for rem in toRem:
                if rel.get("id") == rem:
                    b = True
            if not b:
                print("Complementare -->", rel)  # COMPLEMENTARE

    getInfoSemi(id, conn, df)
    return df
