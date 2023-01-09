from Functions.AlgorithmUtilities import (
    canProceed,
    getAttr,
    getIdenName,
    retrieveInfos,
    removeAttr,
    createDFEnt
)
from Functions.Connection import Connection
import pandas as pd

#TODO code optimization

def entityMatching(ideng: int, conn: Connection):
    """Analizza due entita' e i loro attributi in due sottografi differenti

    Args:
        ideng (int): id dell'entita', deve esistere
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        str: esito dell'analisi
    """    
    
    if canProceed(ideng, conn):
        df = pd.DataFrame(columns=["Tipo", "IDG1", "AttributoG1", "ValoreG1", "IDG2", "AttributoG2", "ValoreG2"])

        attrG1, attrG2 = getAttr(ideng, "G1", conn), getAttr(ideng, "G2", conn)
        toExaminG1, toExaminG2 = getIdenName(ideng, "G1", conn), getIdenName(ideng, "G2", conn)  
        # gia' ordinati per chiave alfabeticamente
        
        toRemoveG1 = list()

        if toExaminG1 == toExaminG2: #per ora non includiamo casi in cui abbiamo diversi identificativi
            for el in toExaminG1:
                if attrG1.get(el) != attrG2.get(el):
                    return "Entita' non confrontabili, sono entita' con identificativi differenti"
        else:
            print(retrieveInfos(toExaminG1, toExaminG2, attrG1, attrG2))

        # rimozione attributi identificativi, analizzati sopra
        removeAttr(attrG1, toExaminG1)
        removeAttr(attrG2, toExaminG2)

        for keyG1 in attrG1:
            for keyG2 in attrG2:
                if keyG1 == keyG2:
                    if attrG1.get(keyG1) == attrG2.get(keyG2):
                        df = pd.concat([df, createDFEnt("Coincidente", attrG1.get('id'), attrG1.get('id'), keyG1, keyG2, attrG1.get(keyG1), attrG2.get(keyG2))], axis=0) # type: ignore
                        #print("Attributo {} di G1 coincidente con attributo {} in G2, valore attributo --> {}".format(keyG1, keyG2, attrG1.get(keyG1))
                    else:
                        df = pd.concat([df, createDFEnt("Contraddittorio", attrG1.get('id'), attrG1.get('id'), keyG1, keyG2, attrG1.get(keyG1), attrG2.get(keyG2))], axis=0) # type: ignore
                        #print(
                        #    "Attributo {} di G1 contraddittorio con attributo {} in G2, valore attributo in G1 --> {}, valore attributo in G2 -->  {}".format(
                        #        keyG1, keyG2, attrG1.get(keyG1), attrG2.get(keyG2)
                        #    )
                        #)
                    toRemoveG1.append(keyG1)
                    break

        for rem in toRemoveG1:
            attrG1.pop(rem)
            attrG2.pop(rem)

        for key in attrG1:
            df = pd.concat([df, createDFEnt("Complementare", attrG1.get('id'), -1, key, "", attrG1.get(key), "")], axis=0) # type: ignore
            #print(
            #    "Attributo {} in G1 con valore {}, complementare".format(
            #        key, attrG1.get(key)
            #    )
            #)

        for key in attrG2:
            df = pd.concat([df, createDFEnt("Complementare", -1, attrG1.get('id'), "", key, "", attrG2.get(key))], axis=0) # type: ignore
            #print(
            #    "Attributo {} in G2 con valore {}, complementare".format(
            #        key, attrG2.get(key)
            #    )
            #)

        return "Entita confrontate correttamente"
    return "Una delle due entita (o entrambe) non esiste (esistono)"
