# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

# build a new client instance of MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and collection instance
db = mongo_client.huwebshop
col = db.profiles
#
# make an API call to the MongoDB server
cursor = col.find({}, {'_id': 1, 'latest_activity': 1, 'recommendations.segment': 1})

# extract the list of documents from cursor obj
mongo_docs = list(cursor)

# restrict the number of docs to export
print ("total docs:", len(mongo_docs))
for i in mongo_docs:
    maindict = dict(i)
    for j in maindict:
        current = i.get(j)
        if type(current) is dict:
            del i[j]
            for k in current:
                new = current.get(k)
                i[(j+'.'+k)] = new

# create an empty DataFrame for storing documents
docs = pandas.DataFrame(list(mongo_docs))
docs = docs[['_id', 'latest_activity', 'recommendations.segment']]
docs.head()
docs = docs.rename(columns={'_id': 'id', 'latest_activity': 'latestactivity', 'recommendations.segment': 'segment'})

docs.to_csv('profiles.csv', index=False)
