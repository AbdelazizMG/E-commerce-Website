from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
db_password = os.environ.get("MONGODB_PASSWORD") 

#connection_string = "mongodb+srv://zezomohammad502:ZRVVqZa8NEX8IfU2@cluster0.fqtfu.mongodb.net/test"
connection_string = f"mongodb+srv://adhamallahwany:{db_password}@cluster0.hwvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)


#db = client['test']
db = client['e_commerce']

#dbs = client.list_database_names()
#test_db = client.test
#print(dbs)
#print(client.test.list_collection_names())

# test_doc = {
#     'name' : 'mobile',
#     'price': 150,
#     'type' : 'electronics'
# }
# test_db.test.insert_one(test_doc)