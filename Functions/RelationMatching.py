import pandas as pd
from Functions.AlgorithmUtilities import (
    createTypeBucket,
    getRel,
    getSemi,
    overLimit,
    sameRel,
    createDF
)
from Functions.Relation import (
    areDirectlyContraddictory, 
    isFissa, 
    isOver,
    sameSourceIden,
    sameTargetIden
)
from Functions.Connection import Connection
from Functions.Entity import getEntity


def getInfoSemi(id: int, conn: Connection, df: pd.DataFrame) -> pd.DataFrame:
    """Analizza le relazioni SemiFisse legate all'id passato in input, mostrando all'utente cosa nota

    Args:
        id (int): id appartenente all'entita' da analizzare\n
        conn (Connection): oggetto dedicato alla connessione a Neo4j
    """
    relP1, relP2 = getSemi(id, 1, 0, conn), getSemi(id, 2, 0, conn)
    relE1, relE2 = getSemi(id, 1, 1, conn), getSemi(id, 2, 1, conn)

    # Parte entranti:
    typeBucket = createTypeBucket(relE1, relE2)
    toRem = list()
    b = True
    for r1 in relE1:
        if not isOver(r1.get('id'), conn):
            for r2 in relE2:
                if not isOver(r2.get('id'), conn):
                    if areDirectlyContraddictory(r1.get("tipo"), r2.get("tipo"), r1.get("id"), r2.get("id"), conn): # CONTRADDITTORIA
                        
                        src, dst = getEntity(r1.get('da'), conn), getEntity(r2.get('da'), conn)
                        df = pd.concat([df, createDF(src, dst, r1.get('id'), r2.get('id'), r1.get('tipo'), r2.get('tipo'), "Contraddittoria diretta Grafo 1 - SemiFissa")], axis=0)
                        
                        toRem.append(r2.get("id"))
                        # b = False
                        # break #ora tolti
                    if sameRel(r1.get("id"), r2.get("id"), id, 1, conn) and sameSourceIden(r1.get("id"), r2.get("id"), conn):  
                        
                        src, dst = getEntity(r1.get('da'), conn), getEntity(r2.get('da'), conn)
                        df = pd.concat([df, createDF(src, dst, r1.get('id'), r2.get('id'), r1.get('tipo'), r2.get('tipo'), "Coincidente - SemiFissa")], axis=0)

                        typeBucket[r1.get("tipo")] += 1
                        b = False
                        toRem.append(r2.get("id"))
                        break
                else:
                    toRem.append(r2.get("id"))
            if b:
                # COMPLEMENTARI
                src = getEntity(r1.get('da'), conn)
                df = pd.concat([df, createDF(src, None, r1.get('id'), -1, r1.get('tipo'), "", "Complementare Grafo1")], axis=0) # type: ignore
                typeBucket[r1.get("tipo")] += 1
            b = True
            
    for el in relE2:
        if not isOver(el.get('id'), conn):
            if not len(toRem):
                typeBucket[el.get("tipo")] += 1
                src, dst = getEntity(el.get('a'), conn), getEntity(el.get('a'), conn)
                df = pd.concat([df, createDF(src, dst, el.get('id'), -1, el.get('tipo'), "", "Complementare Grafo2")], axis=0)
            else:
                b = False
                for id in toRem:
                    if id == el.get("id"):
                        b = True
                if not b:
                    typeBucket[el.get("tipo")] += 1
                    src, dst = getEntity(el.get('a'), conn), getEntity(el.get('a'), conn)
                    df = pd.concat([df, createDF(src, dst, el.get('id'), -1, el.get('tipo'), "", "Complementare Grafo2")], axis=0)

    for t in typeBucket.keys():
        df = pd.concat([df, createDF(None, None, -1, -1, "", "", "SemiFissa" + str(overLimit(t, typeBucket.get(t), relE1, relE2, conn)))], axis=0) # type: ignore 

    # Parte partenti:
    toRem = list()
    b = True
    for r1 in relP1:
        if not isOver(r1.get('id'), conn):
            for r2 in relP2:
                if not isOver(r2.get('id'), conn):
                    if sameRel(r1.get("id"), r2.get("id"), id, 0, conn) and sameTargetIden(r1.get("id"), r2.get("id"), conn):  
                        
                        src, dst = getEntity(r1.get('a'), conn), getEntity(r2.get('a'), conn)
                        df = pd.concat([df, createDF(src, dst, r1.get('id'), r2.get('id'), r1.get('tipo'), r2.get('tipo'), "Coincidente")], axis=0)
                        b = False
                        
                        toRem.append(r2.get("id"))
                        break
                else:
                    toRem.append(r2.get("id"))        
            if b:
                src = getEntity(r1.get('a'), conn)
                df = pd.concat([df, createDF(src, None, r1.get('id'), -1, r1.get('tipo'), "", "Complementare Grafo1")], axis=0)# type: ignore
            b = True

    for el in relP2:
        if not isOver(el.get('id'), conn):
            if not len(toRem):
                src = getEntity(el.get('a'), conn)
                df = pd.concat([df, createDF(src, None, el.get('id'), -1, el.get('tipo'), "", "Complementare Grafo2")], axis=0)# type: ignore
            else:
                b = False
                for id in toRem:
                    if id == el.get("id"):
                        b = True
                if not b:
                    src = getEntity(el.get('a'), conn)
                    df = pd.concat([df, createDF(src, None, el.get('id'), -1, el.get('tipo'), "", "Complementare Grafo2")], axis=0)# type: ignore
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
    df = pd.DataFrame(columns=["Tipo", "IDRelazioneG1", "TipoRelG1", "IDRelazioneG2", "TipoRelG2", "Attr. G1","Attr. G2"])
    
    relP1, relP2 = getRel(id, 1, 0, conn), getRel(id, 2, 0, conn)
    relE1, relE2 = getRel(id, 1, 1, conn), getRel(id, 2, 1, conn)

    compl = False
    toRem = list()

    # PARTENTI:
    for rel1 in relP1:
        if not isOver(rel1.get('id'), conn):
            for rel2 in relP2:
                if not isOver(rel2.get('id'), conn):
                    if sameRel(rel1.get("id"), rel2.get("id"), id, 0, conn):
                        if sameTargetIden(rel1.get("id"), rel2.get("id"), conn):# COINCIDENTI
                            src, dst = getEntity(rel1.get('a'), conn), getEntity(rel2.get('a'), conn)
                            df = pd.concat([df, createDF(src, dst, rel1.get('id'), rel2.get('id'), rel1.get('tipo'), rel2.get('tipo'), "Coincidente")], axis=0)
                            compl = False
                            toRem.append(rel2.get("id"))
                            break
                        else:
                            compl = True
                else:
                    toRem.append(rel2.get("id"))
            if compl:# COMPLEMENTARE
                src, dst = getEntity(rel1.get('da'), conn), getEntity(rel1.get('a'), conn)
                df = pd.concat([df, createDF(src, dst, rel1.get('id'), -1, rel1.get('tipo'), "", "Complementare Grafo1")], axis=0)
                compl = False #TODO NOT SURE

    for rel in relP2:
        if not isOver(rel.get('id'), conn):
            if not len(toRem):
                src, dst = getEntity(rel.get('a'), conn), getEntity(rel.get('a'), conn)
                df = pd.concat([df, createDF(src, dst, rel.get('id'), -1, rel.get('tipo'), "", "Complementare Grafo2")], axis=0)# COMPLEMENTARE
            else:
                compl = False
                for rem in toRem:
                    if rel.get("id") == rem:
                        compl = True
                if not compl:
                    src = getEntity(rel.get('a'), conn)
                    df = pd.concat([df, createDF(src, None, rel.get('id'), -1, rel.get('tipo'), "", "Complementare Grafo2")], axis=0) # type: ignore # COMPLEMENTARE
    
    # ENTRANTI:
    compl = False
    toRem = list()

    for rel1 in relE1:
        if not isOver(rel1.get('id'), conn):
            for rel2 in relE2:
                if not isOver(rel2.get('id'), conn):
                    if areDirectlyContraddictory(rel1.get("tipo"), rel2.get("tipo"), rel1.get("id"), rel2.get("id"), conn):# CONTRADDITTORIA
                        
                        src, dst = getEntity(rel1.get('da'), conn), getEntity(rel2.get('da'), conn)
                        df = pd.concat([df, createDF(src, dst, rel1.get('id'), rel2.get('id'), rel1.get('tipo'), rel2.get('tipo'), "Contraddittoria diretta")], axis=0)
                        
                        toRem.append(rel2.get("id"))
                        # compl = None
                        # break #Per ora tolti
                    if sameRel(rel1.get("id"), rel2.get("id"), id, 1, conn):
                        if sameSourceIden(rel1.get("id"), rel2.get("id"), conn): # COINCIDENTE
                            src, dst = getEntity(rel1.get('da'), conn), getEntity(rel2.get('da'), conn)
                            df = pd.concat([df, createDF(src, dst, rel1.get('id'), rel2.get('id'), rel1.get('tipo'), rel2.get('tipo'), "Coincidente")], axis=0)
                            toRem.append(rel2.get("id"))
                            compl = False
                            break
                        else:
                            if isFissa(rel1.get("tipo"), conn): # CONTRADDITTORIA
                                
                                src, dst = getEntity(rel1.get('da'), conn), getEntity(rel2.get('da'), conn)
                                df = pd.concat([df, createDF(src, dst, rel1.get('id'), rel2.get('id'), rel1.get('tipo'), rel2.get('tipo'), "Contraddittoria")], axis=0)

                                toRem.append(rel2.get("id"))
                                compl = False
                                break
                            else:
                                compl = True
            if compl: # COMPLEMENTARE
                src = getEntity(rel1.get('da'), conn)
                df = pd.concat([df, createDF(src, None, rel1.get('id'), -1, rel1.get('tipo'), "", "Complementare Grafo1")], axis=0)# type: ignore

    for rel in relE2:
        if not isOver(rel.get('id'), conn):
            if not len(toRem):# COMPLEMENTARE
                src = getEntity(rel.get('da'), conn)
                df = pd.concat([df, createDF(src, None, rel.get('id'), -1, rel.get('tipo'), "", "Complementare Grafo2")], axis=0)# type: ignore
            else:
                compl = False
                for rem in toRem:
                    if rel.get("id") == rem:
                        compl = True
                if not compl:# COMPLEMENTARE
                    src = getEntity(rel.get('da'), conn)
                    df = pd.concat([df, createDF(src, None, rel.get('id'), -1, rel.get('tipo'), "", "Complementare Grafo2")], axis=0)# type: ignore

    df = getInfoSemi(id, conn, df)
    return df
