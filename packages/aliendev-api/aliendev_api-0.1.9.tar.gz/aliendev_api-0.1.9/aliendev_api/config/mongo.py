import pymongo
import configparser

def connect():
    # Membaca konfigurasi dari file config.ini
    # config = configparser.ConfigParser()
    # config.read("config.ini")

    # Mendapatkan konfigurasi koneksi ke MongoDB dari file config.ini
    # mongodb_uri = config.get("MONGODB", "uri")
    mongodb_uri = 'mongodb://root:UtyCantik12@203.194.113.203:27017'
    # mongodb_database = config.get("MONGODB", "database")
    mongodb_database = 'alienpdev'

    # Membuat koneksi ke MongoDB
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_database]

    return client,db