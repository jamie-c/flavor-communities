# file neo4j_gds_community_detection.py

from neo4j import GraphDatabase
import os
from dotenv.main import load_dotenv
import time


class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def find_ingredient(self, ingredient_name):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_read(
                self._find_and_return_ingredient, ingredient_name
            )
            for row in result:
                print("Found ingredient: {row}".format(row=row))
        # log the error if there is one

    def get_flavors(self):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_read(self._find_and_return_all_flavors)
            return result

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

    # define a function to project a graph and run louvain community detection
    def projected_graph(self, graph_name):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_read(self._projected_graph, graph_name)
            return result

    def drop_graph(self, graph_name):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_write(self._drop_graph, graph_name)
            return result

    def louvain_community_detection(self, graph_name):
        with self.driver.session(database="exaptive") as session:
            result = session.execute_read(self._louvain_community_detection, graph_name)
            return result

    @staticmethod
    def _drop_graph(tx, graph_name):
        query = "CALL gds.graph.drop($graphName)"
        result = tx.run(query, graphName=graph_name)
        return result

    @staticmethod
    def _find_and_return_flavor(tx, flavor_name):
        query = (
            "MATCH (f:Flavor) " "WHERE f.name = $flavor_name " "RETURN f.name AS name"
        )
        result = tx.run(query, flavor_name=flavor_name)
        return [row["name"] for row in result]

    @staticmethod
    def _find_and_return_all_flavors(tx):
        print("Getting flavors...")
        query = "MATCH (f:Flavor) " "RETURN f.name AS name"
        result = tx.run(query)
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

    @staticmethod
    def _projected_graph(tx, graph_name):
        query = "CALL gds.graph.project($graphName, ['Ingredient', 'Flavor'], 'HAVE') "
        result = tx.run(query, graphName=graph_name)
        return [row for row in result]

    @staticmethod
    def _louvain_community_detection(tx, graph_name):
        query = (
            "CALL gds.louvain.stream($graphName) "
            "YIELD nodeId, communityId "
            "RETURN gds.util.asNode(nodeId).name AS name, communityId "
            "ORDER BY communityId ASC "
        )
        result = tx.run(query, graphName=graph_name)
        return [row for row in result]


if __name__ == "__main__":
    load_dotenv()
    # retrieve values from .env file
    FN_DBMS_UN = os.environ["FN_DBMS_UN"]
    FN_DBMS_PW = os.environ["FN_DBMS_PW"]
    FN_DBMS_URI = "bolt://localhost:7687"

    uri = FN_DBMS_URI
    user = FN_DBMS_UN
    password = FN_DBMS_PW

    # instantiate App class
    app = App(uri, user, password)

    flavor_graph = app.projected_graph("flavor_graph")

    print("Running Louvain Community Detection using neo4j Graph Data Science...")

    start = time.time()  # start timer
    # traverse the graph and get all flavor nodes
    # flavors = app.get_flavors()
    communities = app.louvain_community_detection("flavor_graph")
    end = time.time()  # end timer

    print("Results: ")
    print(f"Time elapsed: {round((end - start) * 1000)} milliseconds")

    # create a list of all the communities from the result only listing each community once
    communityIds = []
    for community in communities:
        if community["communityId"] not in communityIds:
            communityIds.append(community["communityId"])

    for id in communityIds:
        # print the communities in this format: Community CommunityId: name, name, name, ets...
        print(f"Community {id}: ", end="")
        names = []
        for community in communities:
            if community["communityId"] == id:
                names.append(community["name"])
        print(", ".join(names))

    app.drop_graph("flavor_graph")

    # close connection
    app.close()
