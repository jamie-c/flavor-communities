from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import os
from dotenv.main import load_dotenv


class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_have_flavor(self, ingredient_name, flavor_name):
        with self.driver.session(database="exaptive") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_and_return_flavorship, ingredient_name, flavor_name
            )
            for row in result:
                print("Created edge between: {i}, {f}".format(i=row["i"], f=row["f"]))

    @staticmethod
    def _create_and_return_flavorship(tx, ingredient_name, flavor_name):
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MERGE (i:Ingredient { name: $ingredient_name }) "
            "MERGE (f:Flavor { name: $flavor_name }) "
            "MERGE (i)-[:HAVE]->(f) "
            "RETURN i, f"
        )
        result = tx.run(query, ingredient_name=ingredient_name, flavor_name=flavor_name)
        try:
            return [{"i": row["i"]["name"], "f": row["f"]["name"]} for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error(
                "{query} raised an error: \n {exception}".format(
                    query=query, exception=exception
                )
            )
            raise

    def find_flavor(self, flavor_name):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_read(self._find_and_return_flavor, flavor_name)
            for row in result:
                print("Found flavor: {row}".format(row=row))

    def find_ingredient(self, ingredient_name):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_read(
                self._find_and_return_ingredient, ingredient_name
            )
            for row in result:
                print("Found ingredient: {row}".format(row=row))

    @staticmethod
    def _find_and_return_flavor(tx, flavor_name):
        query = (
            "MATCH (f:Flavor) " "WHERE f.name = $flavor_name " "RETURN f.name AS name"
        )
        result = tx.run(query, flavor_name=flavor_name)
        return [row["name"] for row in result]

    @staticmethod
    def _find_and_return_ingredient(tx, ingredient_name):
        query = (
            "MATCH (i:Ingredient) "
            "WHERE i.name = $ingredient_name "
            "RETURN i.name AS name"
        )
        result = tx.run(query, ingredient_name=ingredient_name)
        return [row["name"] for row in result]


if __name__ == "__main__":
    load_dotenv()
    FN_DBMS_UN = os.environ["FN_DBMS_UN"]
    FN_DBMS_PW = os.environ["FN_DBMS_PW"]
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    # uri = "neo4j+s://fb87e512.databases.neo4j.io"
    # user = "neo4j"
    # password = os.environ['FN_API_KEY']
    uri = "bolt://localhost:7687"
    user = FN_DBMS_UN
    password = FN_DBMS_PW
    print(user, password)
    app = App(uri, user, password)
    # app.create_have_flavor("Apple", "Sweet")
    # app.find_flavor('Sweet')
    app.close()
