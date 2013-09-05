from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *
from sqlalchemy.pool import StaticPool

Base = declarative_base()
engine = create_engine('mysql://root@localhost/ex?charset=utf8&use_unicode=0', echo=True)
DBSession = scoped_session(
	sessionmaker(
		autoflush=False,
		expire_on_commit=False,
		autocommit=True,
		bind=engine
	)
)
session = DBSession()
session.expire_on_commit=False
session.autoflush=False
session.autocommit=True

def getSession():
	return session

def getEngine():
	return engine
"""
def getSession():
	if session is None:
		initDB()
	return session
"""

	

class Model():

    '''
 
    This is a baseclass with delivers all basic database operations
     '''
 
    def save(self):
		from ex.database import getSession 
		sess = getSession()
		sess.begin(subtransactions=True)
		try:
			sess.add(self)
			sess.flush()
			sess.commit()
		except:
			sess.rollback()
			sess.begin(subtransactions=True)
			try:
				sess.add(self)
				sess.flush()
				sess.commit()
			except:
				sess.rollback()
				raise
				

		return True
		

    def saveMultiple(self,objects = []):
 		from ex.database import getSession 
		sess = getSession()
		sess.begin(subtransactions=True)
		try:
			sess.add_all(objects)
			sess.flush()
			sess.commit()
		except:
			sess.rollback()
			sess.begin(subtransactions=True)
			try:
				sess.add_all(objects)
				sess.flush()
				sess.commit()
			except:
				sess.rollback()
				raise
				

		return True
    def update(self):
		from ex.database import getSession 
		sess = getSession()
		sess.begin(subtransactions=True)
		sess.commit()
		#sess.flush()
		
    def delete(self):
 		from ex.database import getSession 
		sess = getSession()
		try:
			
			sess.delete(self)
			sess.commit()
		except:
			sess.rollback()
			raise
		
		return self
    def queryObject(self):
		from ex.database import getSession
		return getSession().query(self.__class__)



class ArmaObject(Model):
	id = Column(Integer, primary_key=True)
	netid = Column(String(255))
	varname = Column(String(255))
	clazz = Column(String(255))
	side = Column(String(255))
	posATL = Column(String(255))
	posASL = Column(String(255))
	dir = Column(String(255))
	animation = Column(String(255))
	damage = Column(String(255), default="0")
	alive = Column(String(255))
	
	
	def sqf(self):
		if self.netid is None:
			return "objNull"
		return "(objectFromNetId \"" + self.netid + "\")"
	
	def __repr__(self):
		return '(objectFromNetId "' + self.netid + '")'

class Unit(Base,ArmaObject):
	__tablename__ = 'units'
	loadout = Column(Text())
	vehicle = Column(String(255))
	vehiclePos = Column(String(255))
	variables = Column(Text())
	rank = Column(String(255))
	skill = Column(String(255))
	name = Column(String(255))
	def __repr__(self):
		return '(objectFromNetId "' + self.netid + '")'
	
class Player(Base,ArmaObject):
	__tablename__ = 'player'
	uid = Column(String(255))
	loadout = Column(Text())
	vehicle = Column(String(255))
	vehiclePos = Column(String(255))
	variables = Column(Text())
	rank = Column(String(255))
	skill = Column(String(255))
	
	def __init__(self):
		pass
	def __repr__(self):
		return '(objectFromNetId "' + self.netid + '")'	
	
## Create all Tables 
Base.metadata.create_all(engine)
