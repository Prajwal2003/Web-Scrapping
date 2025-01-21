
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

uri = "mongodb+srv://admin:RtnPUAi3LSI7n7rx@twitter-scrapping.cpib0.mongodb.net/?retryWrites=true&w=majority&appName=Twitter-Scrapping"
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)