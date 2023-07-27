# file copy_ted_neo_local.py

import requests
import json
import os
from dotenv.main import load_dotenv
import networkx as nx
from networkx.algorithms import approximation as aprx
import matplotlib.pyplot as plt
import example

load_dotenv()
API_KEY = os.environ["API_KEY"]
FN_DBMS_UN = os.environ["FN_DBMS_UN"]
FN_DBMS_PW = os.environ["FN_DBMS_PW"]

headers = {"X-API-KEY": f"{API_KEY}"}

api_url = "https://tedtalks.cognitive.city/cnapi"
api_route = "operations"
payload = {"cityNamespace": "main"}

uri = "bolt://localhost:7687"
user = f"{FN_DBMS_UN}"
password = f"{FN_DBMS_PW}"
app = example.App(uri, user, password)


def list_elements(type_name):
    return [{"type": "listElements", "where": {"typeName": f"{type_name}"}}]


def get_connected_elements(uuid):
    return [{"type": "getConnectedElements", "where": {"uuid": f"{uuid}"}}]


def response(post_type, data):
    post_type = globals()[post_type]
    r = requests.post(
        f"{api_url}/{api_route}", params=payload, headers=headers, json=post_type(data)
    )
    return r.json()["data"][0]


element_list = []
flavor_list = []

# Call api to return all flavor nodes
# Will use this data to find edges and other nodes to build the network
# ingredients = response('list_elements', 'ingredient')
flavors = response("list_elements", "flavor")

# Using data from flavors api call above, iterate through data and add each flavor as a node, and print the name of the flavor
for item in flavors:
    flavor = item["properties"]["name"]  # store the name in a variable
    flavor_uuid = item["uuid"]
    flavor_list.append(flavor_uuid)
    print(flavor.upper() + ":")
    # With each flavor, we want the edges... the edge name, and the connected element name.
    connections = response(
        "get_connected_elements", flavor_uuid
    )  # returns a list of objects

    # Using the connections object for the data, we now need to get the nodes and edges.
    # flavor_edges = connections['data'][0]   # returns a list of objects

    for edge in connections:
        node = edge["element"]["uuid"]
        name = edge["element"]["properties"]["name"]
        print(f"Creating edge between {name.capitalize()} and {flavor.capitalize()}...")

        app.create_have_flavor(name.title(), flavor.title())

app.close()

# print(flavor_network)
# print(dict(flavor_network.nodes.data()))
# comp = nx.community.girvan_newman(flavor_network, most_valuable_edge=None)
# c = nx.community.naive_greedy_modularity_communities(flavor_network)
# nx.draw(c, with_labels=True, font_weight='bold')
# plt.show()
# print(c)

# response('update_elements', element_list)

# for i, set in enumerate(c):
#     community_number = i
#     print(f"Updating community number {community_number}")
#     for uuid in set:
#         print(f"Adding Item to List: {uuid}")
#         if uuid not in flavor_list:
#             element_list.append(update_elements_list(uuid, community_number))
#     update_response('update_elements', element_list)
# # print(element_list)
