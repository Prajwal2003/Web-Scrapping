from pymongo import MongoClient

# Connect to the local MongoDB instance (default URI: mongodb://localhost:27017/)
client = MongoClient('mongodb://localhost:27017/')

# Access a database (it will be created if it doesn't exist)
db = client["twitter_data"]

# Access a collection (it will be created if it doesn't exist)
collection = db["trending_topics"]
trending_topic = {"topic": "#AI"}
collection.insert_one(trending_topic)
for trend in collection.find():
    print(trend["topic"])
