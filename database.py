# mongoDB driver
from pymongo import MongoClient
import os

# connection between mongodb and database.py
client = MongoClient('mongodb+srv://code:code@cluster0.5jyfj.mongodb.net/?retryWrites=true&w=majority')

print("Connected !!!")
database = client.wellbeing

user_col = database.users
unverified_user = database.unverified_user

docs = database.docs
unverified_doc = database.unverified_doc
unverified_offline_doc = database.unverified_offline_doc

admin = database.admin


# openssl rand -hex 32

