from DbUtilities import *

#Creazione di una istanza generica
def create_instance(conn, type, attributes):
    legal_attrs = legal_attributes(conn, type, attributes)
    create_id = ""

    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if not (check_instance(conn, type, attributes)):
              create_query = tx.run("CREATE (p:" + type + " {" + stringify_attributes(legal_attrs) + ", id: timestamp()}) RETURN p.id AS node_id")
              create_id = str(create_query.single()["node_id"])
              print(str(legal_attrs) + " " + str(create_id))
              return create_id
            else:
              print("Instance already present and uniquely")

              if (check_instance(conn, type, attributes)):
                instance_query = tx.run("MATCH (instance:" + type + " {" + stringify_attributes(attributes) + "}) RETURN instance.id AS node_id")
                create_id = str(instance_query.single()["node_id"])
                return create_id

            tx.commit()
            tx.close()

#@title CREA ISTANZA CON ID MIO
def create_instance_mine(conn, type, attributes, graph, id):
    legal_attrs = legal_attributes(conn, type, attributes)
    create_id = ""

    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if not (check_instance(conn, type, attributes)):
              create_query = tx.run("CREATE (p:" + type + " {" + stringify_attributes(legal_attrs) + ", graph: " + str(graph) + ", id: " + str(id) + "}) RETURN p.id AS node_id")
              create_id = str(create_query.single()["node_id"])
              print(str(legal_attrs) + " " + str(create_id))
              return create_id
            else:
              print("Instance already present and uniquely")

              if (check_instance(conn, type, attributes)):
                instance_query = tx.run("MATCH (instance:" + type + " {" + stringify_attributes(attributes) + "}) RETURN instance.id AS node_id")
                create_id = str(instance_query.single()["node_id"])
                return create_id

            tx.commit()
            tx.close()

#Cancellazione di una istanza
def delete_instance(conn, type, attributes):
    legal_attr = legal_attributes(conn, type, attributes)

    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            if (check_instance(conn, type, attributes)):
                print("Uniquely identified instance")
                tx.run("MATCH (instance:" + type + " {" + stringify_attributes(legal_attr) + "}) DETACH DELETE instance")

                print("Instance deleted")

            tx.commit()
            tx.close()