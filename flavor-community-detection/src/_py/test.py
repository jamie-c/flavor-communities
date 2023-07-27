def update_elements_list(uuid, community):

     communities = [
         (0, "#00FFFF"),                                                                                                                                                                 
         (1, "#FF0000"),
         (2, "#0000FF"),
         (3, "#00FF00"),
         (4, "#FFFF00"),
         (5, "#FF00FF")
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
          
# def response(post_type, data):
#     post_type = globals()[post_type]
#     if type(data) is 'list':
#         element = post_type(*data)
#     else:
#         element = post_type(data)
#     print(element)

# for i, set in enumerate(data):
#     community_number = i + 1
#     print(community_number)
#     for name in set: 
#         print(name)

# response('update_elements_list', ['uuid-to-print', 2])

the_thing = [0, 1]

print(type(the_thing))

if type(the_thing) == list:
    print("It's a list.")
else: 
    print("nope")
