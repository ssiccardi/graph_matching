import neo4j
from Functions.DbUtilities import check_instance, legal_attributes, stringify_attributes

# Creazione di una istanza generica
def create_instance(conn, t, attributes):
    legal_attrs = legal_attributes(conn, t, attributes)
    create_id = ""

    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if not (check_instance(conn, type, attributes)):
                create_query = tx.run(
                    "CREATE (p:"
                    + str(t)
                    + " {"
                    + stringify_attributes(legal_attrs)
                    + ", id: timestamp()}) RETURN p.id AS node_id"
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


# @title CREA ISTANZA CON ID MIO
def create_instance_mine(conn, t, attributes, graph, id):
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


# Cancellazione di una istanza
def delete_instance(conn, t, attributes):
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
