from neo4j import GraphDatabase
import pandas as pd
class Connection:

    def __init__(self, uri: str, user: str, password: str):
        gDB = GraphDatabase()
        self.driver = gDB.driver(uri, auth=(user, password))# type: ignore
            
    def query(self, query: str, db=None):
        """Permette di interrogare il database, senza controlli in input

        Args:
            query (str): query\n
            db (str, optional): In caso di piu' DB. Defaults to None.

        Returns:
            Neo4jRecord: In base alla query
        """
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.driver.session(database=db) if db is not None else self.driver.session() 
            response = list(session.run(query)) # type: ignore
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
    
    def close(self):
        self.driver.close()