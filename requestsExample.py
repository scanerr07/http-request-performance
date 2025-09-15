import requests
import json #json.dumps(..) ile veriyi json'a çevirdim

#GET
'''
user_id = input('Enter your id: ')
get_url = f"https://jsonplaceholder.typicode.com/todos{user_id}"
get_response = requests.get(get_url)
print(get_response.json())
'''

#POST
to_do_item = {"userId" : 2, "title" : "Wake up", "completed" : True}
post_url ="https://jsonplaceholder.typicode.com/todos"
#optional header
headers = {'content-type': 'application/json'}
post_response = requests.post(post_url,data=json.dumps(to_do_item),headers=headers)
print(post_response.json())
