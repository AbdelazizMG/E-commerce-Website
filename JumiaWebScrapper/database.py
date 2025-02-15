from pymongo import MongoClient
import json,re

connection_string = "mongodb+srv://zezomohammad502:ZRVVqZa8NEX8IfU2@cluster0.fqtfu.mongodb.net/test"

client = MongoClient(connection_string)


db = client.test
products_collection = db.products

#products_collection.insert_many(data)
#I want all products that their cost is less than 100 LE
# lt, gt , eq, gte
# Name, price
temp = products_collection.find({ "price": { "$lte": 100 } })
print(len(list(temp)))
