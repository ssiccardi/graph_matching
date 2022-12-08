import neo4j
from Functions.DbUtilities import check_instance, legal_attributes, stringify_attributes

# @title CREA ISTANZA CON ID MIO
def create_instance_mine(conn, t, attributes, graph, id):
    """Crea un'entita' con attributi dati, nel grafo dato e di tipologia data. Inoltre permette di specificare un id extra

    Args:
        conn (Connection): oggetto dedicato alla connessione a Neo4j
        t (str): tipo dell'entita'
        attributes (dict): key-value attributes
        graph (str): descrive il grafo
        id (int): identificatore aggiuntivo

    Returns:
        void: 
    """    
    legal_attrs = legal_attributes(conn, t, attributes)
    create_id = ""

    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if not (check_instance(conn, t, attributes)):
                create_query = tx.run(
                    "CREATE (p:"
                    + t
                    + " {"
                    + stringify_attributes(legal_attrs)
                    + ", graph: "
                    + str(graph)
                    + ", id: "
                    + str(id)
                    + "}) RETURN p.id AS node_id"
                )
                create_id = str(create_query.single()["node_id"])
                print(str(legal_attrs) + " " + str(create_id))
                return create_id
            else:
                print("Instance already present and uniquely")

                if check_instance(conn, type, attributes):
                    instance_query = tx.run(
                        "MATCH (instance:"
                        + str(t)
                        + " {"
                        + stringify_attributes(attributes)
                        + "}) RETURN instance.id AS node_id"
                    )
                    create_id = str(instance_query.single()["node_id"])
                    return create_id

            tx.commit()
            tx.close()
            
def delete_instance(conn, t, attributes):
    """Elimina un'entita' con attributi dati e di tipologia data. IN ENTRAMBI I GRAFI

    Args:
        conn (Connection): oggetto dedicato alla connessione a Neo4j
        t (str): tipo dell'entita'
        attributes (dict): key-value attributes

    Returns:
        void: 
    """    
    legal_attr = legal_attributes(conn, type, attributes)

    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if check_instance(conn, t, attributes):
                print("Uniquely identified instance")
                tx.run(
                    "MATCH (instance:"
                    + str(t)
                    + " {"
                    + stringify_attributes(legal_attr)
                    + "}) DETACH DELETE instance"
                )

                print("Instance deleted")

            tx.commit()
            tx.close()
