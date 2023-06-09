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

    def find_ingredient(self, ingredient_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(
                self._find_and_return_ingredient, ingredient_name
            )
            for row in result:
                print("Found ingredient: {row}".format(row=row))
        # log the error if there is one

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
    FN_ADBMS_UN = os.environ["FN_ADBMS_UN"]
    FN_ADBMS_PW = os.environ["FN_ADBMS_PW"]
    FN_ADBMS_URI = os.environ["FN_ADBMS_URI"]
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    # uri = "neo4j+s://fb87e512.databases.neo4j.io"
    # user = "neo4j"
    # password = os.environ['FN_API_KEY']
    uri = FN_ADBMS_URI
    user = FN_ADBMS_UN
    password = FN_ADBMS_PW
    print(uri, user, password)
    app = App(uri, user, password)
    # app.create_have_flavor("Apple", "Sweet")
    app.find_ingredient("Pear")
    app.close()
