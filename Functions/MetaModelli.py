import neo4j
from Functions.DbUtilities import check_metamodello
from Functions.Connection import Connection

def metamodelloPersona(conn: Connection):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            checkPresence = tx.run(
                "MATCH (instance:Person) - [r:HAS] - (n:Name) RETURN instance,r,n"
            )
            checkPresenceValues = checkPresence.values()

            if len(checkPresenceValues) == 0:
                personScheme = tx.run(
                    "CREATE (instance:Person {label: 'Person', type: 'entity'}) - [:HAS] -> (:Name {label: 'Name', type: 'attr'}), (instance) - [:HAS] -> (:Surname {label: 'Surname', type: 'attr'}) RETURN id(instance) AS node_id"
                )
                personSchemeNode = personScheme.single()

                if personSchemeNode is None:
                    raise Exception("Errore con personScheme.single()")
                    
                tx.run(
                    "MATCH (instance:Person), (n:Name), (s:Surname) WHERE id(instance) = $node_id CREATE (i:Identifier {label: 'iden'}) <- [:IDENTIFIED] - (instance), (i) - [:IDENTIFIED_BY] -> (n), (i) - [:IDENTIFIED_BY] -> (s)",
                    node_id=personSchemeNode["node_id"] 
                )

            else:
                print("Metamodello entità tipo Persona già presente")

            tx.commit()
            tx.close()

def metamodelloSocieta(conn: Connection):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            checkPresence = tx.run(
                "MATCH (instance:Società) - [r:HAS] -> (a:RagioneSociale) RETURN instance,r,a"
            )
            checkPresenceValues = checkPresence.values()

            if len(checkPresenceValues) == 0:
                tx.run(
                    "CREATE (instance:Società {label: 'Società', type: 'entity'}) - [:HAS] -> (a:RagioneSociale {label: 'RagioneSociale', type: 'attr'}), (instance) - [:IDENTIFIED] -> (iden:Identifier {label: 'iden'}), (iden) - [:IDENTIFIED_BY] -> (a) RETURN id(instance) AS node_id"
                )
            else:
                print("Metamodello entità tipo Società già presente")

            tx.commit()
            tx.close()

def metamodelloLuogo(conn: Connection):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            checkPresence = tx.run(
                "MATCH (instance:Luogo) - [r:HAS] -> (a:NomeLuogo) RETURN instance,r,a"
            )
            checkPresenceValues = checkPresence.values()

            if len(checkPresenceValues) == 0:
                tx.run(
                    "CREATE (instance:Luogo {label: 'Luogo', type: 'entity'}) - [r:HAS] -> (a:NomeLuogo {label: 'NomeLuogo', type: 'attr'}), (instance) - [:IDENTIFIED] -> (iden:Identifier {label: 'iden'}), (iden) - [:IDENTIFIED_BY] -> (a) RETURN id(instance) AS node_id"
                )
            else:
                print("Metamodello entità tipo Luogo già presente")

            tx.commit()
            tx.close()

def metamodelloIndirizzo(conn: Connection):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            checkPresence = tx.run(
                "MATCH (instance:Indirizzo) - [r:HAS] -> (a:NomeIndirizzo) RETURN instance,r,a"
            )
            checkPresenceValues = checkPresence.values()

            if len(checkPresenceValues) == 0:
                tx.run(
                    "CREATE (instance:Indirizzo {label: 'Indirizzo', type: 'entity'}) - [:HAS] -> (a:NomeIndirizzo {label: 'NomeIndirizzo', type: 'attr'}), (instance) - [:IDENTIFIED] -> (iden:Identifier {label: 'iden'}), (iden) - [:IDENTIFIED_BY] -> (a) RETURN id(instance) AS node_id"
                )
            else:
                print("Metamodello entità tipo Indirizzo già presente")

            tx.commit()
            tx.close()

def metamodelloAutomobile(conn: Connection):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            checkPresence = tx.run(
                "MATCH (instance:Automobile) - [r:HAS] -> (a:Targa) RETURN instance,r,a"
            )
            checkPresenceValues = checkPresence.values()

            if len(checkPresenceValues) == 0:
                tx.run(
                    "CREATE (instance:Automobile {label: 'Automobile', type: 'entity'}) - [:HAS] -> (a:Targa {label: 'Targa', type: 'attr'}), (instance) - [:IDENTIFIED] -> (iden:Identifier {label: 'iden'}), (iden) - [:IDENTIFIED_BY] -> (a) RETURN id(instance) AS node_id"
                )
            else:
                print("Metamodello entità tipo Automobile già presente")

            tx.commit()
            tx.close()

def addType(conn: Connection, t: str):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            print("A new entity type named " + str(t) + " will be added. Continue?")
            print("y - yes, n - no")
            flag = input()

            if flag == "y":
                alreadyPresent = tx.run(
                    "MATCH (instance:" + str(t) + " {type: 'entity'}) RETURN instance" # type: ignore 
                )
                alreadyPresentValues = alreadyPresent.values()

                if len(alreadyPresentValues) == 0:
                    newType = tx.run(
                        "CREATE (instance:" #type: ignore
                        + str(t)
                        + " {label: '"
                        + str(t)
                        + "', type: 'entity'}) RETURN instance"
                    )
                    newTypeValue = newType.values()

                    print("Entity type created")
                    print(newTypeValue)
                else:
                    print("Entity type already present")

            elif flag == "n":
                print("Operation aborted.")

def addAttribute(conn: Connection, t: str, attribute: str, y: bool=False):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if not y :
                print(
                    "A new attribute named "
                    + str(attribute)
                    + " will be added to entity type "
                    + str(t)
                    + ". Continue?"
                )
                print("y - yes, n - no")
                flag = input()
            else:
                flag = "y"
            if flag == "y":
                typePresence = tx.run(
                    "MATCH (instance:" + str(t) + " {type: 'entity'}) RETURN instance" #type: ignore
                )
                typeValues = typePresence.values()

                if len(typeValues) == 1:
                    attrAlreadyPresent = tx.run(
                        "MATCH (instance:" #type: ignore
                        + str(t)
                        + " {type: 'entity'}) - [rel:HAS] -> (attr:"
                        + str(attribute)
                        + " {type: 'attr'}) RETURN instance, rel, attr"
                    )
                    attrPresentValues = attrAlreadyPresent.values()

                    if len(attrPresentValues) == 0:
                        tx.run(
                            "MATCH (type:" #type: ignore
                            + str(t)
                            + " {type: 'entity'}) CREATE (type) - [rel:HAS] -> (attr:"
                            + str(attribute)
                            + " {label: '"
                            + str(attribute)
                            + "', type: 'attr'}) RETURN type, rel, attr"
                        )

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
                        "Problem with entity type. Number of "
                        + str(t)
                        + " type discovered: "
                        + str(len(typeValues))
                    )

            elif flag == "n":
                print("Operation aborted.")

def addIdentifier(conn: Connection, t: str, attribute: str):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:

            print(
                "A new identifier node will be added to entity type "
                + t
                + " to attributes: "
                + attribute
                + ". Continue?"
            )
            print("y - yes, n - no")
            flag = input()

            if flag == "y":
                typePresence = tx.run(
                    "MATCH (instance:" + t + " {type: 'entity'}) RETURN instance" #type: ignore
                )
                typeValues = typePresence.values()

                legal_attrs = []

                if len(typeValues) == 1:
                    for attr in attribute:
                        if check_metamodello(conn, t, attr):
                            legal_attrs.append(attr)
                        else:
                            print("Attribute " + attr + " not found.")

                    if len(legal_attrs) > 0:
                        nodeToIden = tx.run(
                            "MATCH (instance:" #type: ignore
                            + t
                            + " {type: 'entity'}) CREATE (instance) - [rel:IDENTIFIED] -> (iden:Identifier {label: 'iden'}) RETURN id(iden) AS iden_id"
                        )
                        nodeToIden.single()

                        for attr in legal_attrs:
                            tx.run(
                                "MATCH (iden:Identifier), (attr:"
                                + attr
                                + " {type: 'attr'}) CREATE (iden) - [rel:IDENTIFIED_BY] -> (attr) RETURN iden, rel, attr"
                            )

                        print("Identifier node created.")

                    else:
                        print("Can't create identifier node. Check attributes.")

                else:
                    print(
                        "Problem with entity type. Number of "
                        + t
                        + " type discovered: "
                        + str(len(typeValues))
                    )

            elif flag == "n":
                print("Operation aborted")

def relazione(conn: Connection, nome: str, riflessiva: int, card):
    """Definisce un metamodello per una relazione

    Args:
        conn (Connection): oggetto dedicato alla connessione a Neo4j
        nome (str): nome della relazione
        riflessiva (int): per capire se la relazione e' bidirezionale
        card (int or str): identifica il numero massimo con cui la relazione puo' essere utilizzata su una singola entita'
    """
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            checkPresence = tx.run('Match (e) WHERE e.label = "' + nome + '" RETURN e') #type: ignore
            checkPresenceValues = checkPresence.values()

            if len(checkPresenceValues) == 0:
                query = (
                    "CREATE (instance:Relazione {label:'"
                    + nome
                    + "', type:'relation'}) - [:HAS] -> (:Cardinalita {label:'"
                    + str(card)
                    + "', type:'attr'}), (instance) - [:HAS] -> (:Riflessivita {label:'"
                    + str(riflessiva)
                    + "', type:'attr'}) RETURN id(instance) AS node_id"
                )
                tx.run(query) #type: ignore
            else:
                print("Metamodello relazione con nome [{}] già esistente!".format(nome))

            tx.commit()
            tx.close()

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