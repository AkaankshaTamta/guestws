#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
a simple Flask example works with local (non-persistent) data store
once the service is stopped, the data will be lost

'''

import random
import boto3
from decimal import *
from flask import abort,Flask, jsonify, request
from boto3 import resource
import botocore.exceptions
app = Flask(__name__)

# a list of guests

guests = []

class Guest:
    def __init__(self, gid, first, last):
        self.gid = gid
        self.first = first
        self.last = last

def find(gid):
    for g in guests:
        if g.gid == gid:
            return g
    return None

def AsDict(guest):
    return {'id': guest.gid, 'first': guest.first, 'last': guest.last}

def get_table():
    dynamodb_resource = resource('dynamodb')
    readtable = dynamodb_resource.Table('test2')
    return readtable

@app.route("/rest/query", methods=['GET'])
def query():
    calltable = get_table()
    response = calltable.scan()
    return jsonify(response)

@app.route("/rest/update/<gid>/<first>/<last>", methods=['PUT'])
def update(gid, first, last):
    rtable = get_table()
    
    try:
            response = rtable.update_item(
                Key={'gid': Decimal(str(gid))},
                UpdateExpression="set firstname=:f, lastname=:l",
               ExpressionAttributeValues={':f': first,':l': last},
               ReturnValues="UPDATED_NEW")
            
    except botocore.exceptions.ClientError as err:
            raise
            
    return "Guest updated successfully"

@app.route("/rest/insert/<gid>/<first>/<last>", methods=['POST'])
def insert(gid, first, last):
    rtable = get_table()
    
    try:
            response = rtable.put_item(
                Item={
                    'gid': Decimal(str(gid)),
                    'first': first,
                    'last': last})
            
    except botocore.exceptions.ClientError as err:
            raise
            
    return "Guest added successfully"

@app.route("/rest/delete/<gid>", methods=['DELETE'])
def delete(gid):
    rtable = get_table()
    try:
            rtable.delete_item(Key={'gid': Decimal(str(gid))})
            
    except botocore.exceptions.ClientError as err:
            raise
            
    return "Guest successfully deleted"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)


# In[ ]:




