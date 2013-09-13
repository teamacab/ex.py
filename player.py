from database import Player
from database import Unit
from rvengine import RVEngine

def loadPlayer(netid, uid, varname):
	RVEngine.log("Loading Player from uid " + uid)
	qo = Player().queryObject()
	p = qo.filter(Player.uid == uid).first()
	if p is None:
		RVEngine.log("Player not found, creating.")
		p = Player()
		p.uid = uid
		p.varname = varname
		p.save()
	p.netid = netid
	p.sync = True
	p.update()
	RVEngine.log("Loading unitdata")
	RVEngine.loadPlayer(p)
	return p


def naked(player):
	pass
