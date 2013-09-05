import os
import sys
import player

from rvengine import RVEngine

from database import Unit
from database import Player

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


RVEngine.log("Loading EXPY Python Interface " + VERSION);

def createUnit(netid):
	RVEngine.log("Creating unit for netid " + netid)
	u = Unit()
	u.netid = netid
	allUnits.update({ netid : u })
	return u

def getUnit(varname):
	qo = Unit().queryObject()
	u = qo.filter(Unit.varname == varname).first()
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
	

def loadPlayer(netid,uid):
	return player.loadPlayer(netid,uid)
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
def version():
	return VERSION
	

def getArmaDir():
	return os.path.abspath(os.getcwd() + "\\..\\")
	
def test1(a):
	RVEngine.execute("hint 'hihihihih: " + a + "'")
	return a
	

	
	
def status():
	return sys.path
	
	
	
	