
from flask import Blueprint
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

load_dotenv()


mongo = Blueprint("mongo",__name__)

cluster = MongoClient(os.getenv("FLASK_MONGO_URL"),tlsCAFile=certifi.where())

db = cluster["mongodata"]
collection = db["mongo"]


@mongo.route('/create/<string:email>/<string:password>', methods = ['GET','POST'])
def create(email, password):
  try:
    data = collection.find_one({
      "_id" : email
    })
    if data == None:
      collection.insert_one({
          "_id" : email,
          "password" : password
        })
      return {'valid':True, 'status':'success'}
        
    else:
      return {'valid':False, 'status':'success'}
  except:
    return  {'status':'error'}


@mongo.route('/read/<string:email>/<string:password>')
def read(email,password):
  try:
    data = collection.find_one({
      "_id" : email
    })
    if data == None:
      return {'valid':False,'status':'success'}
    elif data['password'] == password:
      return {'valid':True,'status':'success'}
    else:
      return {'valid':False,'status' : 'success'}
  except:
    return {'status':'error'}

