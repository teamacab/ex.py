import os
import sys
import player

from rvengine import RVEngine

from database import Unit
from database import Player
from thread import start_new_thread
# import shortuuid

import logging
import time

# import RVEngine
# from Unit import *
# from Db import Db
# from Unit import Unit
# from ex.dbmap import Unit
# from  import RVEngine

VERSION = "0.1.0"
allUnits = {}
players = {}
inArma = False
running = True
uuidIndex = 0
RVEngine.log("Loading EXPY Python Interface " + VERSION);

logging.basicConfig(filename='expy.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
preloadBuffer = []
updateQueue = {}
dbCommit = True
def createUnit(netid):
	RVEngine.log("Creating unit for netid " + netid)
	u = Unit()
	u.netid = netid
	allUnits.update({ netid : u })
	return u

def getUnit(netid, varname):
	qo = Unit().queryObject()
	u = qo.filter(Unit.varname == varname).first()
	if u is None:
		RVEngine.log("Creating new unit")
		u = Unit()
		u.varname = varname
		u.save()
	u.netid = netid
	return u


def preloadUnit(netid, varname, clazz):
	u = Unit()
	u.varname = varname
	u.netid = netid
	u.clazz = clazz
	# u.save()
	preloadBuffer.append(u);
	return u

def preloadUnitThread():
	from ex.database import getSession
	while running:
		time.sleep(0.5)
		for u in preloadBuffer:
			RVEngine.log("Preloading " + u.varname)
			u.save()
			preloadBuffer.remove(u)

def loadUnit(netid, varname):
	RVEngine.log("Loading " + varname)
	u = getUnit(netid, varname)
	# RVEngine.loadUnit(u)
	allUnits.update({ netid : u })
	return u

def updateUnitT():
	RVEngine.log("Starting updateUnitT")
	time.sleep(10)
	while True:
		time.sleep(0.5)
		qo = Unit().queryObject()
		# RVEngine.log("update unit data")
		for u in qo.all():
			# RVEngine.log("Working on " + u.varname)
			d = updateQueue.get(u.varname)
			if d is not None:
				try:
				# 	RVEngine.log("Having unit " + u.varname + " netid " + u.netid)
					u.netid = d.get('netid')
					u.posATL = d.get('posATL')
					u.posASL = d.get('posASL')
					u.loadout = d.get('loadout')
					u.damage = d.get('damage')
					u.animation = d.get('animation')
					u.side = d.get('side')
					u.skill = d.get('skill')
					u.alive = d.get('alive')
					updateQueue.pop(u.varname, 0)
				except Exception, e:
					logger.error("Error while updating " + u.varname + ": " + str(e))
			# else:
				# RVEngine.log("No dict for " + u.varname + " in " + str(updateQueue))

			time.sleep(0.01)



def updateUnit(netid, varname, posATL, posASL, loadout, damage, anim, side, rank, skill, alive):
	data = {
		'netid' : netid,
		'posATL' : posATL,
		'posASL' : posASL,
		'loadout' : loadout,
		'damage' : damage,
		'animation' : anim,
		'side' : side,
		'rank' : rank,
		'skill' : skill,
		'alive' : alive
		}
	updateQueue.update({ varname : data })
	return str(data)

def loadPlayer(netid, uid):
	p = player.loadPlayer(netid, uid)
	players.update({ uid : p})
	return p

def getPlayer(varname):
	return getPlayerByVarname(varname)

def getPlayerByVarname(varname):
	qo = Player().queryObject()
	p = qo.filter(Player.varname == varname).first()
	return p

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
	return int(time.time() + 300)



def status():
	return sys.path

def updateNetId(ref, netid):
	qo = Unit().queryObject()
	x = qo.filter(Unit.ref == ref).first()
	if qo is None:
		x = qo.filter(Player.ref == ref).first()

	if x is not None:
		x.netid = netid
		x.update()
		x.sync = True

	return x


def loadWorldT():
	time.sleep(10)
	RVEngine.log("Restoring world... this may take a while.")
	# restore all units
	qo = Unit().queryObject()
	for u in qo.all():
		RVEngine.log("Loading unit " + u.varname)
		RVEngine.createUnit(u)

def loadWorld():
	start_new_thread(loadWorldT, ())
	return True


def saveWorld():
	from ex.database import getSession
	# savePlayers()
	# saveUnits()
	sess = getSession()  # .begin(subtransactions=True)
	try:
		RVEngine.log("Flushing database.")
		sess.flush()
		# sess.commit()
		RVEngine.log("Flushed")

	except Exception, e:
		try:
			logger.error("Error Rolling back: '" + str(e) + "'")
			sess.rollback()
			sess = getSession()  # .begin(subtransactions=True)
			logger.error("Error Reflushing database.")
			sess.flush()
			logger.error("Error Recommiting database.")
			# sess.commit()

		except Exception, e:
			logger.error("Aborting: " + str(e))
			sess.rollback()
			raise

def saveThread():
	RVEngine.log("Starting saveThread")
	while running:
		time.sleep(10)
		try:
			saveWorld()
		except Exception, e:
				logger.error("Error in saveThread: " + str(e))

		# RVEngine.log("Saving", __file__)



start_new_thread(saveThread, ())
start_new_thread(preloadUnitThread, ())
start_new_thread(updateUnitT, ())
