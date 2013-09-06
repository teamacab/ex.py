import os
import sys
import player

from rvengine import RVEngine

from database import Unit
from database import Player
from thread import start_new_thread
#import shortuuid

import time

#import RVEngine
#from Unit import *
#from Db import Db
#from Unit import Unit
#from ex.dbmap import Unit
#from  import RVEngine

VERSION="0.1.0"
allUnits = {}
players = {}
inArma = False
running = True
uuidIndex = 0
RVEngine.log("Loading EXPY Python Interface " + VERSION);

def createUnit(netid):
	RVEngine.log("Creating unit for netid " + netid)
	u = Unit()
	u.netid = netid
	allUnits.update({ netid : u })
	return u

def getUnit(netid,varname):
	qo = Unit().queryObject()
	u = qo.filter(Unit.varname == varname).first()
	if u is None:
		RVEngine.log("Creating new unit")
		u = Unit()
		u.varname = varname
		u.save()
	u.netid = netid
	return u

def loadUnit(netid,varname):
	RVEngine.log("Loading " + varname)
	u = getUnit(netid,varname)
	#RVEngine.loadUnit(u)
	allUnits.update({ netid : u })
	return u

def loadPlayer(netid,uid):
	p = player.loadPlayer(netid,uid)
	players.update({ uid : p})
	return p

def getPlayer(uid):
	return players.get(uid)
	
		
def savePlayers():
	qo = Player().queryObject()
	for p in qo.all():
		RVEngine.log("Updating " + str(p.varname))
		p.update()
		
	return True

def saveUnits():
	qo = Unit().queryObject()
	for u in qo.all():
		RVEngine.log("Updating " + str(u.varname))
		u.update()
		
	return True
		
def version():
	return VERSION
	

def getArmaDir():
	return os.path.abspath(os.getcwd() + "\\..\\")

def uuid():
	return int(time.time()+300)

	
	
def status():
	return sys.path
	
def updateNetId(ref, netid):
	qo = Unit().queryObject()
	x = qo.filter(Unit.ref==ref).first()
	if qo is None:
		x = qo.filter(Player.ref==ref).first()
	
	if x is not None:
		x.netid = netid
		x.update()
		x.sync = True
	
	return x


def loadWorld():
	RVEngine.log("Restoring world... this may take a while.")
	# restore all units
	qo = Unit().queryObject()
	for u in qo.all():
		RVEngine.createUnit(u)
	return True

def saveThread():
	from ex.database import getSession
	RVEngine.log("Starting saveThread")
	while running:
		time.sleep(10)
		#RVEngine.log("Saving", __file__)
		savePlayers()
		saveUnits()
		RVEngine.log("Flushing database.")
		getSession().flush()

		
start_new_thread(saveThread, ())
	