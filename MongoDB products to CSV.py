# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

# build a new client instance of MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and collection instance
db = mongo_client.huwebshop
col = db.products
#
# make an API call to the MongoDB server
cursor = col.find({}, {'_id': 1, 'name': 1, 'brand': 1, 'properties.soort': 1, 'category': 1, 'sub_category': 1,
                       'sub_sub_category': 1, 'properties.doelgroep': 1, 'price.mrsp': 1, 'price.discount': 1, 'price.selling_price': 1,
                       'properties.discount': 1, 'description': 1})

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
docs = docs[['_id', 'name', 'brand', 'properties.soort', 'category', 'sub_category', 'sub_sub_category', 'properties.doelgroep',
             'price.mrsp', 'price.discount', 'price.selling_price', 'properties.discount', 'description']]
docs.head()
docs = docs.rename(columns={'_id': 'id', 'properties.soort': 'type', 'sub_category': 'subcategory',
                            'sub_sub_category': 'subsubcategory', 'properties.doelgroep': 'targetaudience',
                            'price.mrsp': 'mrsp', 'price.discount': 'discount', 'price.selling_price': 'sellingprice',
                            'properties.discount': 'deal'})

docs.to_csv('products.csv', index=False)