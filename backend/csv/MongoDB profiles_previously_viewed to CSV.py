# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

# build a new client instance of MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and collection instance
db = mongo_client.huwebshop
col = db.profiles

print("\n### MongoDB profiles_previously_viewed to CSV.py ###\n")

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

col = db.products
#
# make an API call to the MongoDB server
cursor = col.find({}, {'_id': 1})

raw_products = list(cursor)

whitelist = []

for i in raw_products:
    whitelist.append(i.get("_id"))


mongo_docs_new = []
count = 0
for i in mongo_docs:
    count += 1
    print("\r" + str(count), end="")
    if i.get("propid") in whitelist:
        mongo_docs_new.append(i)

print()

# create an empty DataFrame for storing documents
print(len(mongo_docs_new))
docs = pandas.DataFrame(list(mongo_docs_new))

docs.to_csv('profiles_previously_viewed.csv', index=False)

exec(open("MongoDB sessions to CSV.py").read())
