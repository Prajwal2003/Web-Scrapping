from pymongo import MongoClient
import yaml

# Connect to the local MongoDB instance (default URI: mongodb://localhost:27017/)
client = MongoClient('mongodb+srv://admin:RtnPUAi3LSI7n7rx@twitter-scrapping.cpib0.mongodb.net/?retryWrites=true&w=majority&appName=Twitter-Scrapping')

with open("creds.yaml", "r") as file:
    creds = yaml.safe_load(file)

dbname = creds['dbname']
collection = creds['collection']
trending_topic = {"topic": "#AI"}
collection.insert_one(trending_topic)
for trend in collection.find():
    print(trend["topic"])
