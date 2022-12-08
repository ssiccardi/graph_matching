import neo4j

# @title util to create istanze
def check_metamodello(conn, t, key):
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            node_attribute_check = tx.run(
                "MATCH (n) WHERE exists((:"
                + str(t)
                + ") - [:HAS] -> (n:"
                + key
                + ")) RETURN labels(n) AS node_label",
                key=key,
            )
            node_attribute_record = node_attribute_check.single()

            if node_attribute_record != None:
                attribute_key = node_attribute_record["node_label"][0]

                if attribute_key == key:
                    return True

            else:
                return False

            tx.commit()
            tx.close()


def legal_attributes(conn, t, attributes):
    legal_attributes = {}

    for key in attributes:
        if check_metamodello(conn, t, key):
            legal_attributes[key] = attributes[key]

    if "id" in attributes:
        legal_attributes["id"] = attributes["id"]

    return legal_attributes


def check_instance(conn, t, attributes):
    legal_attributes = {}

    for key in attributes:
        if check_metamodello(conn, t, key):
            legal_attributes[key] = attributes[key]

    if check_identifiable(conn, t, attributes):
        with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
            with session.begin_transaction() as tx:
                tx.run(
                    "MATCH (instance:"
                    + str(t)
                    + " {"
                    + stringify_attributes(legal_attributes)
                    + "}) RETURN instance"
                )

                tx.commit()
                tx.close()
    return False
    # return instance_found


def check_identifiable(conn, t, attributes):
    legal_attr = legal_attributes(conn.driver, t, attributes)

    identifiable_attributes = get_identifiable_attributes(conn.driver, t)

    for el in identifiable_attributes:
        count = 0

        for attr in el:
            if attr in legal_attr:
                count += 1

        if count == len(el):
            return True

    return False


def stringify_attributes(attributes):
    attributes_string = ""

    counter = 1
    for key in attributes:
        if counter == len(attributes):
            if key == "id":
                attributes_string += key + " : " + str(attributes[key]).strip() + " "
            else:
                attributes_string += key + " : '" + str(attributes[key]).strip() + "'"
        elif key == "id":
            attributes_string += key + " : " + str(attributes[key]).strip() + ", "
        else:
            attributes_string += key + " : '" + attributes[key].strip() + "', "
        counter += 1

    return attributes_string


def get_identifiable_attributes(conn, t):
    identifiable_attributes = []
    with conn.driver.session(default_access_mode=neo4j.WRITE_ACCESS) as session:
        with session.begin_transaction() as tx:
            iden_nodes_query = tx.run(
                "MATCH (i:Identifier) - [] - (:" + str(t) + ") RETURN id(i)"
            )

            for el in iden_nodes_query.values():
                attributes = []

                if el != None:
                    identifiable_attributes_query = tx.run(
                        "MATCH (attr) - [:IDENTIFIED_BY] - (i:Identifier) WHERE id(i) = $node_id RETURN attr",
                        node_id=el[0],
                    )

                    for el in identifiable_attributes_query.values():
                        attributes.append(el[0].get("label"))

                identifiable_attributes.append(attributes)

            tx.commit()
            tx.close()

    return identifiable_attributes
