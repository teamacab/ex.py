import os
import sys
import player

from rvengine import RVEngine

from database import Unit
from database import Player
from thread import start_new_thread

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
	
def longtest(prefix):
	i = 0
	list = []
	x = None
	while i < 100:
		num = prefix + i
		p = Player()
		p.uid = num
		list.append(p)
		x = p
		i += 1
	Player().saveMultiple(list)
	return test()
	
def xtr():
	longtest(123)
	longtest(1232)
	longtest(12311)
	longtest(1233231)
	longtest(1233222)
	return test()

def test():
	x = Player()
	qa = x.queryObject()
	return qa.all()
	
def a(b):
	return b

def loadUnit(netid,varname):
	RVEngine.log("Loading " + varname)
	u = getUnit(netid,varname)
	RVEngine.loadUnit(u)
	allUnits.update({ netid : u })
	return u

def loadPlayer(netid,uid):
	p = player.loadPlayer(netid,uid)
	players.update({ uid : p})
	return p
"""
def createPlayer(uid,netid):
	RVEngine.log("Creating player for uid " + uid)
	p = Player(uid)
	players.update( { uid : p } )
	allUnits.update( { netid : p } )
	return p
	
def getPlayer(uid,netid=None):
	p = players.get(uid)
	if p is None and netid is not None:
		p = createPlayer(uid,netid)
	return p
	
def loadPlayer(uid,netid):
	return 0
"""	
def getPlayer(uid):
	return players.get(uid)
	
		
def savePlayers():
	for uid, p in players.items():
		p.update()
		
	return True

def saveUnits():
	for netid, p in allUnits.items():
		p.update()
		
	return True
		
def version():
	return VERSION
	

def getArmaDir():
	return os.path.abspath(os.getcwd() + "\\..\\")
	
def test1(a):
	RVEngine.execute("hint 'hihihihih: " + a + "'")
	return a
	

	
	
def status():
	return sys.path
	
	
def saveThread():
	from ex.database import getSession
	RVEngine.log("Starting saveThread")
	while running:
		#RVEngine.log("Saving", __file__)
		savePlayers()
		saveUnits()
		RVEngine.log("Flushing database.")
		getSession().flush()
		time.sleep(10)
		
start_new_thread(saveThread, ())
	