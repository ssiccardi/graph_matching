import sys
sys.path.insert(0, '..')
from Functions.AlgorithmUtilities import (
    canProceed,
    getAttr,
    getIdenName,
    retrieveInfos,
    removeAttr,
    updateDF_Entity
)
from Functions.Connection import Connection
import pandas as pd

def entityMatching(ideng: int, conn: Connection)-> str:
    """Analizza due entita' e i loro attributi in due sottografi differenti

    Args:
        ideng (int): id dell'entita', deve esistere
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        str: esito dell'analisi
    """    
    if not canProceed(ideng, conn):
        return "Una delle due entita (o entrambe) non esiste (esistono)"
    attrG1, attrG2 = getAttr(ideng, "G1", conn), getAttr(ideng, "G2", conn)
    toExaminG1, toExaminG2 = getIdenName(ideng, "G1", conn), getIdenName(ideng, "G2", conn)  
    # già ordinati per chiave alfabeticamente
        
    id1, id2 = attrG1.pop("idDB"), attrG2.pop("idDB")
    tipo1 =  attrG1.pop("tipo"); attrG2.pop("tipo")
    
    # DataFrame per i risultati
    df = pd.DataFrame(columns=[
        "Descrizione confronto attributo",
        "Tipo Entità", "ID Entità Grafo1", "Tipo attributo Entità Grafo1", "Attributo Entità Grafo1",
        "ID Entità Grafo2", "Tipo attributo Entità Grafo2", "Attributo Entità Grafo2"])
    
    toRemoveG1 = list()

    if toExaminG1 == toExaminG2:
        for el in toExaminG1:
            if attrG1.get(el) != attrG2.get(el):
                return "Entita' non confrontabili, sono entita' con identificativi differenti"
    else:
        print(retrieveInfos(toExaminG1, toExaminG2, attrG1, attrG2))

    # rimozione attributi identificativi, analizzati sopra
    removeAttr(attrG1, toExaminG1)
    removeAttr(attrG2, toExaminG2)

    
    for keyG1 in attrG1:
        tmpRemove = None
        tmpBool = False
        for keyG2 in attrG2:
            if keyG1 == keyG2:
                if attrG1.get(keyG1) == attrG2.get(keyG2):
                    print(
                        "Attributo {} di G1 coincidente con attributo {} in G2, valore attributo --> {}".format(
                            keyG1, keyG2, attrG1.get(keyG1)
                        )
                    )
                    df = pd.concat([df, updateDF_Entity(cfr="Coincidenti", typeEnt=tipo1, id1=id1, id2=id2, typeAttr1=keyG1, typeAttr2=keyG2, valueAttr1=str(attrG1.get(keyG1)), valueAttr2=str(attrG2.get(keyG2)))], axis=0)
                        
                else:
                    print(
                        "Attributo {} di G1 contraddittorio con attributo {} in G2, valore attributo in G1 --> {}, valore attributo in G2 -->  {}".format(
                            keyG1, keyG2, attrG1.get(keyG1), attrG2.get(keyG2)
                        )
                    )
                    df = pd.concat([df, updateDF_Entity(cfr="Contraddittorie", typeEnt=tipo1, id1=id1, id2=id2, typeAttr1=keyG1, typeAttr2=keyG2, valueAttr1=str(attrG1.get(keyG1)), valueAttr2=str(attrG2.get(keyG2)))], axis=0)
                    
                toRemoveG1.append(keyG1)
                tmpRemove = keyG1
                tmpBool = True
                break
        if tmpBool:
            attrG2.pop(tmpRemove)

    for rem in toRemoveG1:
        attrG1.pop(rem)

    for key in attrG1:
        print(
            "Attributo {} in G1 con valore {}, complementare".format(
                key, attrG1.get(key)
            )
        )
        df = pd.concat([df, updateDF_Entity(cfr="Complementare", typeEnt=tipo1, id1=id1, typeAttr1=key, valueAttr1=str(attrG1.get(key)))], axis=0)

    for key in attrG2:
        print(
            "Attributo {} in G2 con valore {}, complementare".format(
                key, attrG2.get(key)
            )
        )
        df = pd.concat([df, updateDF_Entity(cfr="Complementare", typeEnt=tipo1, id2=id2, typeAttr2=key, valueAttr2=str(attrG2.get(key)))], axis=0)
            
    f = open("../Contents/EntityMatchingAnalisi.csv", "w")
    f.write(df.to_csv())
    f.close()

    return "Entita confrontate correttamente"