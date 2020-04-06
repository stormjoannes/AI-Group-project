from flask import Flask
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from backend.create_connnection import create_connection

app = Flask(__name__)
api = Api(app)

db = create_connection()
cur = db[0]
conn = db[1]
cur = conn.cursor()

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
if os.getenv(envvals[0]) is not None:
    envvals = list(map(lambda x: str(os.getenv(x)), envvals))
    client = MongoClient(dbstring.format(*envvals))
else:
    client = MongoClient()
database = client.huwebshop 


class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, prodid, count, page):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        prodids = []

        if page == 'category':
            query = """SELECT catrecommend, subcatrecommend, subsubcatrecommend FROM profile_recommendations WHERE id = %s"""
            data = cur.execute(query, (profileid, ))
        elif page == 'detail':
            query = """SELECT catrecommend, subcatrecommend, subsubcatrecommend, namerecommend FROM products WHERE id = %s"""
            data = cur.execute(query, (prodid, ))
        elif page == 'shoppingcart':
            query = """SELECT recommendation_1, recommendation_2, recommendation_3, recommendation_4 FROM all_prof_rec WHERE id_ = %s"""
            data = cur.execute(query, (profileid, ))

        ids = cur.fetchall()
        for i in ids:
            for x in i:
                prodids.append(x)

        return prodids, 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.

api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:prodid>/<string:page>")