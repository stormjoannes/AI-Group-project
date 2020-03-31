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
cursor = col.find({}, {'_id': 1, 'recommendations.viewed_before': 1})

# extract the list of documents from cursor obj
mongo_docs_raw = list(cursor)

mongo_docs = []
# restrict the number of docs to export
print ("total docs:", len(mongo_docs_raw))
for i in mongo_docs_raw:
    maindict = dict(i)
    for j in maindict:
        current = i.get(j)
        if type(current) is dict:
            del i[j]
            for k in current:
                new = current.get(k)
                i[(j+'.'+k)] = new
    viewed_before = i.get('recommendations.viewed_before')
    if viewed_before:
        id = i.get('_id')
        for j in viewed_before:
            mongo_docs.append({'profid': id, 'propid': j})


# create an empty DataFrame for storing documents
print(len(mongo_docs))
docs = pandas.DataFrame(list(mongo_docs))
# docs = docs[['_id', 'latest_activity', 'recommendations.segment']]
# docs.head()
# docs = docs.rename(columns={'_id': 'id', 'latest_activity': 'latestactivity', 'recommendations.segment': 'segment'})

docs.to_csv('profiles_previously_viewed.csv', index=False)