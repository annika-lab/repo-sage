from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_write(self, query, params=None):
        with self.driver.session() as session:
            session.execute_write(lambda tx: tx.run(query, params or {}))