#! /usr/local/bin/python3.11
# file test_update.py

import requests
import json
import os
from dotenv.main import load_dotenv
import networkx as nx
from networkx.algorithms import approximation as aprx
import matplotlib.pyplot as plt
import time

load_dotenv()
API_KEY = os.environ["API_KEY"]

headers = {"X-API-KEY": f"{API_KEY}"}

api_url = "https://tedtalks.cognitive.city/cnapi"
api_route = "operations"
payload = {"cityNamespace": "main"}


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


community_info = {"sweet": 2, "acid": 3, "umami": 4, "fat": 1, "salt": 5}

element_list = []
flavor_list = []

# Initialize flavor network
flavor_network = nx.Graph()

# Call api to return all flavor nodes
# Will use this data to find edges and other nodes to build the network
# ingredients = response('list_elements', 'ingredient')
flavors = response("list_elements", "flavor")


# Using data from ingredients api call above, iterate trough data and print ingredient name, and add ingredient as a node.
# Will comment this section out as the network can be built from the flavor nodes and connections
# for item in ingredients:

#     # iterate through a list and use each uuid (item['uuid']) to update the community (update_elements())
#     name = item['properties']['name']
#     flavor_network.add_node(name)
#     print(item['properties']['name'])

#     # Get connected elements using uuid
#     connected_elements = response('get_connected_elements', item['uuid'])

#     conn_name = connected_elements[0]['element']['properties']['name']

#     # Set community number and color based on connection name
#     element_list.append(update_elements_list(item['uuid'], community_info[conn_name]))


# Using data from flavors api call above, iterate through data and add each flavor as a node, and print the name of the flavor
for item in flavors:
    # print(f"Adding flavor: {item['properties']['name']}")
    flavor = item["properties"]["name"]  # store the name in a variable
    flavor_uuid = item["uuid"]
    flavor_list.append(flavor)
    flavor_network.add_node(f"{flavor}")  # add node to flavor network
    # print(flavor)  # print the flavor uuid

    # With each flavor, we want the edges... the edge name, and the connected element name.
    connections = response(
        "get_connected_elements", flavor_uuid
    )  # returns a list of objects

    # Using the connections object for the data, we now need to get the nodes and edges.
    # flavor_edges = connections['data'][0]   # returns a list of objects

    for edge in connections:
        node = edge["element"]["properties"]["name"]
        # c_color = edge['element']['properties']['Community_Color']
        # c_number = edge['element']['properties']['Community_Number']

        flavor_network.add_node(f"{node}")
        flavor_network.add_edge(f"{flavor}", f"{node}")

    # Iterate through the data and add to the flavor network


# print(f"Created {flavor_network}")
# print(dict(flavor_network.nodes.data()))
# comp = nx.community.girvan_newman(flavor_network, most_valuable_edge=None)

# print("Running community detection using Naive Greedy Modularity Maximization")
# print("Running Louvain Community Detection using networkx louvain_communities...")

# log the time it takes to run the community detection algorithm
start = time.time()  # start the timer
l = nx.community.louvain_communities(flavor_network)
# c = nx.community.naive_greedy_modularity_communities(flavor_network)
end = time.time()  # end the timer

# nx.draw(c, with_labels=True, font_weight='bold')
# plt.show()

# print the results
# print(f"Results:")
# print the time in milliseconds
# print(f"Time elapsed: {round((end - start) * 1000)} milliseconds")

# generate json object for the louvain community detection results
data = {
    "name": "louvain",
    "method": "networkX",
    "time_elapsed": round((end - start) * 1000),
}

# loop through community detection results and print the community
for i, community in enumerate(l):
    # print(f"Community {i}: ", end="")
    data[f"community_{i}"] = []
    # print the values of the set, separated by a comma and a space, and capitalize each word
    # print(", ".join(community).title())
    # enumerate through the community and add each community to the json object
    for item in community:
        data[f"community_{i}"].append(item)

json_data = json.dumps(data)

print(json_data)
