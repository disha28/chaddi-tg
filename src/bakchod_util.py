#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

import logging
import pickle
import util
from datetime import datetime, date, timezone

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Encapsulate data representing a Bakchod
class Bakchod:
  def __init__(self, id, username):
    self.id = None
    self.username = username
    self.lastseen = None
    self.rokda = 500

# Using Python pickling for data persistence
try:
    with open('resources/bakchod.pickle', 'rb') as handle:
        bakchod_dict = pickle.load(handle)
        logger.info('Loaded Bakchod pickle')
except:
    logger.info('Bakchod pickle not found... Making new one')
    bakchod_dict = {}
    with open('resources/bakchod.pickle', 'wb') as handle:
        pickle.dump(bakchod_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Get a Bakchod based on tg_id
def get_bakchod(tg_id):

    if tg_id in bakchod_dict:
        a_bakchod = bakchod_dict[tg_id]
    else:
        a_bakchod = None

    return a_bakchod

# Update Bakchod and commit to pickle
def set_bakchod(a_bakchod):

    if a_bakchod.id in bakchod_dict:
        bakchod_dict[a_bakchod.id] = a_bakchod

    with open('resources/bakchod.pickle', 'wb') as handle:
        pickle.dump(bakchod_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Update data of a Bakchod... lastseen and rokda
def bakchod_updater(from_user):

    if from_user is not None:

        if from_user['username'] is not None:
            username = "@" + from_user['username']
        else:
            username = from_user['first_name']

        tg_id = from_user['id']

        if tg_id in bakchod_dict:
            a_bakchod = bakchod_dict[tg_id]
        else:
            a_bakchod = Bakchod(tg_id, username)

        a_bakchod.lastseen = datetime.now()
        a_bakchod.rokda = a_bakchod.rokda + 1

        logger.info("Updating Bakchod for username=" + username + " rokda=" + str(a_bakchod.rokda))

        bakchod_dict[tg_id] = a_bakchod

        with open('resources/bakchod.pickle', 'wb') as handle:
            pickle.dump(bakchod_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def timesince_query(query_username):

    for bakchod in bakchod_dict.values():
        if bakchod.username == query_username:
            response = timesince_calculator(bakchod.lastseen)
            return(query_username + ' last posted ' + response + ' ago')
    else: 
        return("404")

def timesince_calculator(lastseen):

    now = datetime.now()
    td = now - lastseen
    pretty_td = util.pretty_time_delta(td.total_seconds())
    return(pretty_td)

def rokda_query(query_id):

    if query_id in bakchod_dict:
        found_bakchod = bakchod_dict[query_id]
        return("💰" + found_bakchod.username + ' has ' + str(found_bakchod.rokda) + ' ₹okda!')
    else: 
        return("404")


