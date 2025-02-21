from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
db_password = os.environ.get("MONGODB_PASSWORD") 

connection_string = f"mongodb+srv://adhamallahwany:{db_password}@cluster0.hwvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)


db = client['e_commerce']

