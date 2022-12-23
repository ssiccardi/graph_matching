## Directory Functions 

 ### File DbUtilities.py 

 

 ### Function Header --> 

` getEntityId(t: str, attr: dict, graph, conn: Connection)-> int:
    ` 

 - Ottieni l'ID automatico dato da Neo4j al momento dell'inserimento
- Args:
  - t (str): tipo dell'entita'
  - attr (dict): key-value attributes
  - graph (str or int): identificatore grafo di appartenenza
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Raises:
  - Exception: quando troviamo piu' entita' con stessi parametri
- Returns:
  - int: ID entita' riconosciuta dai parametri
 

 <hr> 

### File Connection.py 

 

 ### Function Header --> 

` query(self, query: str, db=None):
        ` 

 - Permette di interrogare il database, senza controlli in input
- Args:
  - query (str): query\n
  - db (str, optional): In caso di piu' DB. Defaults to None.
- Returns:
  - Neo4jRecord: In base alla query
 

 <hr> 

### File AlgorithmUtilities.py 

 

 ### Function Header --> 

` getLimit(t: str, conn: Connection) -> int:
    ` 

 - Ottiene la Cardinalita per una relazione semifissa
- Args:
  - t (str): nome della relazione
  - conn (Connectio): oggetto dedicato alla connessione a Neo4j
- Returns:
  - int: Cardinalita relazione se presente, ?unknown? altrimenti


 ### Function Header --> 

` isSemiFissa(t: str, conn: Connection) -> bool:
    ` 

 - Capisce se la relazione e' di tipo SemiFisso
- Args:
  - t (str): nome della relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se SemiFissa, False altrimenti


 ### Function Header --> 

` getAttr(ideng, g, conn: Connection):  
    ` 

 - Ritorna una lista di chiavi valori con gli attributi
- Args:
  - ideng (int): id dell'entita'
  - g (str): grafo da cui prendere gli attributi
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - dict: key-value attributes


 ### Function Header --> 

` getIdenName(ideng, g, conn : Connection):
    ` 

 - Ritorna una lista di attributi identitari
- Args:
  - ideng (int): id dell'entita'
  - g (str): grafo da cui prendere gli attributi
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - list: attributi identitari


 ### Function Header --> 

` onlySemi(lista, conn: Connection):
    ` 

 - Filtra le relazioni non SemiFisse
- Args:
  - lista (list): lista di relazioni
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - list: lista di relazioni SemiFisse


 ### Function Header --> 

` deleteSemi(lista, conn: Connection):
    ` 

 - Filtra le relazioni SemiFisse
- Args:
  - lista (list): lista di relazioni
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - list: lista di relazioni SemiFisse
 

 <hr> 

### File Relation.py 

 

 ### Function Header --> 

` sameSource(r1, r2, conn: Connection)-> bool:
    ` 

 - Stabilisce sue due relazioni hanno la stessa entita' sorgente sulla base degli id extra
- Args:
  - r1 (int or str): id relazione
  - r2 (int or str): id relazione_
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Raises:
  - Exception: Se la query non va a buon fine
- Returns:
  - bool: True se hanno gli stessi ID extra, False altrimenti


 ### Function Header --> 

` sameTarget(r1, r2, conn: Connection) -> bool:
    ` 

 - Stabilisce sue due relazioni hanno la stessa entita' target sulla base degli id extra
- Args:
  - r1 (int or str): id relazione
  - r2 (int or str): id relazione_
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Raises:
  - Exception: Se la query non va a buon fine
- Returns:
  - bool: True se hanno gli stessi ID extra, False altrimenti


 ### Function Header --> 

` isFissa(t: str, conn: Connection) -> bool:
    ` 

 - Capisce se la relazione e' di tipo Fisso
- Args:
  - t (str): nome della relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se Fissa, False altrimenti


 ### Function Header --> 

` isMultipla(t: str, conn: Connection) -> bool:
    ` 

 - Capisce se la relazione e' di tipo Multiplo
- Args:
  - t (str): nome della relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se Multipla, False altrimenti


 ### Function Header --> 

` getScadute(idDst, relName: str, conn: Connection)-> int:
    ` 

 - Conta il numero di relazioni di tipo indicato, che arrivano all'entita' indicata, sono scadute
- Args:
  - idDst (str or int): ID dell'entita' di destinazione
  - relName (str): tipo di relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo
- Returns:
  - int: numero di relazioni di tipo relName scadute ed indirizzate ad idDst


 ### Function Header --> 

` canCreate(idDst, relName: str, conn: Connection, scadenza = None) -> bool:
    ` 

 - Capisce se la relazione tra le due entita' puo' essere creata. Quindi si chiede se tra le due e' gia' presente la relazione, se attiverebbe contraddizioni e cosi' via
- Args:
  - idDst(int or str): id dell'entita' di destinazione
  - relName (str): nome della relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se passa tutti i controlli, False altrimenti


 ### Function Header --> 

` addRelAttribute(conn: Connection, t: str, attribute: str):
    ` 

 - Aggiunge un'attributo al metamodello di una relazione
- Args:
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
  - t (str): tipo della relazione
  - attribute (str): nome dell'attributo da aggiungere


 ### Function Header --> 

` alreadyExist(t1: str, t2: str, t: str, conn: Connection) -> bool:
    ` 

 - funzione di utility per vedere se due metamodelli sono gia' collegati da una relazione di tipo t
- Args:
  - t1 (str): nome primo metamodello
  - t2 (str): nome secondo metamodello
  - t (str): _description_
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se esiste gia' una relazione, False altrimenti


 ### Function Header --> 

` addConstraint(relType1: str, relType2: str, relType: str, conn) -> bool:
    ` 

 - Aggiunge un link, con nome specificato in relType, tra metamodelli (se non esiste gia')
- Args:
  - relType1 (str): nome prima relazione
  - relType2 (str): nome seconda relazione
  - relType (str): nome link da aggiungere
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se e' stato possibile aggiungerlo, False altrimenti


 ### Function Header --> 

` getContraddictory(par, t: int, conn: Connection) -> list:
    ` 

 - Ottiene relazioni contraddittorie
- Args:
  - par (int or str): id dell'entita' di destinazione or tipo di relazione
  - t (int): specifica dove cercare, 0 per entita' o 1 per relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Raises:
  - ValueError: t != 0 and t != 1
- Returns:
  - list: lista di relazioni contraddittorie per l'entita' o la relazione data


 ### Function Header --> 

` srcCheck(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
    ` 

 - Controlla se esiste rel tra le due entita'
- Args:
  - entSrc (int): id dell'entita' di destinazione
  - entDst (int): id dell'entita' di destinazione
  - rel (str): relazione da controllare
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se esiste, False altrimenti


 ### Function Header --> 

` alreadyLinked(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
    ` 

 - Controlla se esiste rel tra le due entita'
- Args:
  - entSrc (int): id dell'entita' di destinazione
  - entDst (int): id dell'entita' di destinazione
  - rel (str): relazione da controllare
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - bool: True se esiste, False altrimenti


 ### Function Header --> 

` checkInsertion(entSrc: int, entDst: int, rel: str, conn: Connection) -> bool:
    ` 

 - Controlla che non avvengano inserimenti contraddittori / non sia gia' presente
- Args:
  - entSrc (int): deve essere un intero indicante un'entita' esistente all'interno del db
  - entDst (int): deve essere un intero indicante un'entita' esistente all'interno del db


 ### Function Header --> 

`inito
        conn (Connection): oggetto dedicato alla connessione a Neo4j

    Returns:
        bool: True se inseribile, False altrimenti
    ` 

 - 
  - if alreadyLinked(entSrc, entDst, rel, conn):
  - return False
- presentContr = getContraddictory(rel, 1, conn)
  - # ottengo tutte le relazioni in contraddizioni con quella da inserire
- for p in presentContr:  # si controlla se nell'entita' sorgente e' presente questa relazione in contraddizione con quella da inserire
  - if alreadyLinked(entSrc, entDst, p, conn):
  - return False
- return True
- #SOLO PER ENTRANTI


 ### Function Header --> 

` create_relation_dir(typeES: str, ES_attr: dict, gS, typeET: str, ET_attr: dict, gT, relName: str, conn: Connection) -> str:
    ` 

 - Crea, se possibile, una relazione tra l'entita' sorgente e quella destinazione, riconosciute tramite i parametri passati, con nome specificato
- Args:
  - typeES (str): tipo dell'entita' sorgente
  - ES_attr (dict): key-value attributes sorgente
  - gS (int or str): grafo sorgente
  - typeET (str): tipo dell'entita' destinazione
  - ET_attr (dict): key-value attributes destinazione
  - gT (int or str): grafo destinazione
  - relName (str): nome della relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - str: OK se non ci sono errori


 ### Function Header --> 

` create_relation_with_attribute(typeES: str, ES_attr: dict, gS, typeET: str, ET_attr: dict, gT, relName: str, relAttr: dict, conn: Connection) -> str:
    ` 

 - Crea, se possibile, una relazione tra l'entita' sorgente e quella destinazione, riconosciute tramite i parametri passati, con nome e con attributi specificati
- Args:
  - typeES (str): tipo dell'entita' sorgente
  - ES_attr (dict): key-value attributes sorgente
  - gS (int or str): grafo sorgente
  - typeET (str): tipo dell'entita' destinazione
  - ET_attr (dict): key-value attributes destinazione
  - gT (int or str): grafo destinazione
  - relName (str): nome della relazione
  - relAttr (dict): attributi associati alla relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - str: OK se non ci sono errori


 ### Function Header --> 

` isOver(relID, conn: Connection):
    ` 

 - Controlla se la relazione e' scaduta
- Args:
  - relID (str or int): ID della relazione
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Raises:
  - Exception: Se la relazione non ha scadenza
- Returns:
  - bool: True se scaduta, False altrimenti
 

 <hr> 

### File RelationMatching.py 

 

 ### Function Header --> 

` getInfoSemi(id: int, conn: Connection, df: pd.DataFrame) -> pd.DataFrame:
    ` 

 - Analizza le relazioni SemiFisse legate all'id passato in input, mostrando all'utente cosa nota
- Args:
  - id (int): id appartenente all'entita' da analizzare\n
  - conn (Connection): oggetto dedicato alla connessione a Neo4j


 ### Function Header --> 

` relationMatching(id: int, conn: Connection):
    ` 

 - Analizza le relazioni legate all'id passato in input, mostrando all'utente cosa nota\n
  - PreCondizioni:
  - 1)Le entita' esistono e non sono contraddittorie\n
  - 2)Le relazioni fisse hanno subito un controllo in inserimento, non ci possono essere piu' relazioni fisse uguali appartenenti alla stessa entita' di uno stesso grafo\n
  - 3)Le relazioni semifisse hanno subito lo stesso controllo in inserimento!\n
  - Args:
  - id (int): [id appartenente all'entita' da analizzare]\n
  - conn (Connection): [oggetto dedicato alla connessione a Neo4j]
 

 <hr> 

### File MetaModelli.py 

 

 ### Function Header --> 

` relazione(conn: Connection, nome: str, riflessiva: int, card):
    ` 

 - Definisce un metamodello per una relazione
- Args:
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
  - nome (str): nome della relazione
  - riflessiva (int): per capire se la relazione e' bidirezionale
  - card (int or str): identifica il numero massimo con cui la relazione puo' essere utilizzata su una singola entita'
 

 <hr> 

### File Entity.py 

 

 ### Function Header --> 

` create_instance_mine(conn: Connection, t, attributes, graph, id):
    ` 

 - Crea un'entita' con attributi dati, nel grafo dato e di tipologia data. Inoltre permette di specificare un id extra
- Args:
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
  - t (str): tipo dell'entita'
  - attributes (dict): key-value attributes
  - graph (str): descrive il grafo
  - id (int): identificatore aggiuntivo
- Returns:
  - void:


 ### Function Header --> 

` delete_instance(conn: Connection, t: str, attributes: dict):
    ` 

 - Elimina un'entita' con attributi dati e di tipologia data. IN ENTRAMBI I GRAFI
- Args:
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
  - t (str): tipo dell'entita'
  - attributes (dict): key-value attributes
- Returns:
  - void:


 ### Function Header --> 

` delete_instance_id(conn: Connection, id: int):
    ` 

 - Elimina un'entita' con attributi dati e di tipologia data. IN ENTRAMBI I GRAFI
- Args:
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
  - id (int): ID univoco dell'entita'
- Returns:
  - void:
 

 <hr> 

### File EntityMatching.py 

 

 ### Function Header --> 

` entityMatching(ideng: int, conn: Connection):
    ` 

 - Analizza due entita' e i loro attributi in due sottografi differenti
- Args:
  - ideng (int): id dell'entita', deve esistere
  - conn (Connection): oggetto dedicato alla connessione a Neo4j
- Returns:
  - str: esito dell'analisi
 

 <hr> 

