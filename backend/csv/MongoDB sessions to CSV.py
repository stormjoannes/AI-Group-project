# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

import datetime

print("\n### MongoDB sessions to CSV.py ###\n")

# build a new client instance of MongoClient
mongo_client = MongoClient('localhost', 27017)

# create new database and collection instance
db = mongo_client.huwebshop
col = db.profiles

cursor = col.find({}, {'_id': 1, 'buids': 1})


# extract the list of documents from cursor obj
mongo_docs = list(cursor)
mongo_docs_buids = {}

for i in mongo_docs:
    current = i.get('buids')
    id = i.get('_id')
    if current:
        for j in current:
            mongo_docs_buids[j] = str(id)


# create new database and collection instance
db = mongo_client.huwebshop
col = db.sessions
#
# make an API call to the MongoDB server
cursor = col.find({}, {'_id': 1, 'buid': 1, 'segment': 1, 'has_sale': 1, 'session_start': 1,
                       'session_end': 1,'user_agent.os.familiy': 1, 'user_agent.device.family': 1,
                       'user_agent.flags.is_mobile': 1, 'user_agent.flags.is_pc': 1, 'user_agent.flags.is_tablet': 1})
mongo_docs_raw = []
keers = 0
print('Items van find naar list')
for i in cursor:
    keers += 1
    print('\r'+str(keers), end='')
    mongo_docs_raw.append(i)


mongo_docs = []
# restrict the number of docs to export
print ("\ntotal docs:", len(mongo_docs_raw))
for times in range(2):
    print('Dicts openklappen keer {}'.format(times+1))
    counter = 0
    for i in mongo_docs_raw:
        counter += 1
        maindict = dict(i)
        for j in maindict:
            current = i.get(j)
            if type(current) is dict:
                del i[j]
                for k in current:
                    new = current.get(k)
                    i[(j+'.'+k)] = new
        if times == 1:
            buid = i.get('buid')
            start = i.get('session_start')
            end = i.get('session_end')
            if buid and start and end:
                while type(buid) is list:
                    buid = buid[0]
                profid = mongo_docs_buids.get(buid)
                if profid:
                    i['profid'] = profid
                    del i['buid']
                    if i.get('user_agent.flags.is_mobile'):
                        del i['user_agent.flags.is_mobile']
                        del i['user_agent.flags.is_pc']
                        del i['user_agent.flags.is_tablet']
                        i['devicetype'] = 'mobile'
                    elif i.get('user_agent.flags.is_pc'):
                        del i['user_agent.flags.is_mobile']
                        del i['user_agent.flags.is_pc']
                        del i['user_agent.flags.is_tablet']
                        i['devicetype'] = 'pc'
                    elif i.get('user_agent.flags.is_tablet'):
                        del i['user_agent.flags.is_mobile']
                        del i['user_agent.flags.is_pc']
                        del i['user_agent.flags.is_tablet']
                        i['devicetype'] = 'tablet'

                    diff = end - start
                    diff = diff.seconds
                    i['duration'] = diff

                    mongo_docs.append(i)

                buid = i.get('buid')
                if buid:
                    while type(buid) is list:
                        buid = buid[0]
                    profid = mongo_docs_buids.get(buid)
                    if profid:
                        start = i.get('session_start')
                        end = i.get('session_end')
                        i['profid'] = profid
                        del i['buid']
                        mongo_docs.append(i)



# create an empty DataFrame for storing documents
print('Making dataframe')
mongo_docs = list(mongo_docs)
print(len(mongo_docs))
docs = pandas.DataFrame(mongo_docs)
docs = docs[['_id', 'profid', 'segment', 'has_sale', 'session_start', 'session_end', 'duration',
             'user_agent.os.familiy', 'user_agent.device.family', 'devicetype']]
docs.head()
docs = docs.rename(columns={'_id': 'id', 'has_sale': 'sale', 'session_start': 'starttime',
                            'session_end': 'endtime', 'user_agent.os.familiy': 'os',
                            'user_agent.device.family': 'devicefamily'})

docs.to_csv('sessions.csv', index=False)

exec(open("postgreSQL setup.py").read())
