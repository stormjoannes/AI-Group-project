# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

# build a new client instance of MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and collection instance
db = mongo_client.huwebshop
col = db.profiles

# make an API call to the MongoDB server
cursor = col.find()

# extract the list of documents from cursor obj
mongo_docs = list(cursor)

# restrict the number of docs to export
print ("total docs:", len(mongo_docs))

# create an empty DataFrame for storing documents
docs = pandas.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate(mongo_docs):

    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

    # get document _id from dict
    doc_id = doc["_id"]

    # create a Series obj from the MongoDB dict
    series_obj = pandas.Series( doc, name=doc_id )

    # append the MongoDB Series obj to the DataFrame obj
    docs = docs.append(series_obj)

    # only print every 10th document
    if num % 10 == 0:
        print('\r' + str(num), end='')

# export MongoDB documents to a CSV file
docs.to_csv("profiles.csv", ",") # CSV delimited by commas

# export MongoDB documents to CSV
csv_export = docs.to_csv(sep=",") # CSV delimited by commas
print ("\nCSV data:", csv_export)