# file test_update.py

import requests
import json
import os
from dotenv.main import load_dotenv
import networkx as nx
from networkx.algorithms import approximation as aprx
import matplotlib.pyplot as plt

load_dotenv()
API_KEY = os.environ['API_KEY']

headers = {
       "X-API-KEY": f"{API_KEY}"
       }

api_url = "https://tedtalks.cognitive.city/cnapi"
api_route = "operations"
payload = {'cityNamespace': 'main'}

def list_elements(type_name):
    
    return [{
    "type": "listElements",
    "where": {
        "typeName": f"{type_name}"
    }
}]

def get_connected_elements(uuid):
    
    return [{
    "type": "getConnectedElements",
    "where": {
        "uuid": f"{uuid}"
    }
}]

def update_elements_list(uuid, community):

    communities = [
        (0, ""),
        (1, "#FF0000"),
        (2, "#0000FF"),
        (3, "#00FF00"),
        (4, "#"),
        (5, "#")
        ]
    

    return {
                "target": {
                    "uuid": f"{uuid}",
                    "typeName": "ingredient"
                },
                "data": {
                    "properties": {
                        "Community_Number": communities[community][0],
                        "Community_Color": communities[community][1]
                    }
                }
            }

def update_elements(elements_list):

    return [{
        "type": "updateManyElements",
        "mergeProperties": "true",
        "syncInBackground": "false",
        "elements": elements_list
        }]
    

def response(post_type, data):
    
    post_type = globals()[post_type]
    r = requests.post(f"{api_url}/{api_route}", params=payload, headers=headers, json=post_type(data))
    return r.json()['data'][0]
        
#if __name__ == "__main__":
#    api_call = MakeApiCall(f"{api_url}/{api_route}")

community_info = {
    'sweet': 2,
    'acid': 3,
    'umami': 4,
    'fat': 1,
    'salt': 5
    }

# element_list = []

# Initialize flavor network
flavor_network = nx.Graph()

# Call api to return all flavor nodes
# Will use this data to find edges and other nodes to build the network
# ingredients = response('list_elements', 'ingredient')
flavors = response('list_elements', 'flavor')

# Print the word Ingredients:
print("Ingredients:")

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
       
# Print the word Flavors:
print("Flavors:")

# Using data from flavors api call above, iterate through data and add each flavor as a node, and print the name of the flavor
for item in flavors: 

    flavor = item['properties']['name'] # store the name in a variable
    flavor_network.add_node(f"{flavor}")       # add node to flavor network
    print(item['properties']['name'])   # print the flavor name

    # With each flavor, we want the edges... the edge name, and the connected element name.
    connections = response('get_connected_elements', item['uuid'])  # returns a list of objects

    # Using the connections object for the data, we now need to get the nodes and edges.
    # flavor_edges = connections['data'][0]   # returns a list of objects

    for edge in connections:
        node = edge['element']['properties']['name']
        c_color = edge['element']['properties']['Community_Color']
        c_number = edge['element']['properties']['Community_Number']

        flavor_network.add_node(f"{node}")
        flavor_network.add_edge(f"{flavor}", f"{node}")

    # Iterate through the data and add to the flavor network


print(flavor_network)
print(dict(flavor_network.nodes.data()))
# comp = nx.community.girvan_newman(flavor_network, most_valuable_edge=None)
c = nx.community.naive_greedy_modularity_communities(flavor_network)
# nx.draw(c, with_labels=True, font_weight='bold')
# plt.show()
print(c)

# response('update_elements', element_list)

