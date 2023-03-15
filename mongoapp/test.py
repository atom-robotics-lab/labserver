from pymongo import MongoClient

local_client = MongoClient("mongodb://admin:admin@localhost:27017/")
db_name = 
db = local_client.list_database_names()
print(db)