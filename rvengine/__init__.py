from textwrap import wrap, TextWrapper
class RVEngine:
	
	instance = None
	queue = []
	FrameNo = 0
	FPS = 0
	FPS_MIN = 0
	TickTime = 0
	Time = 0
	nextTransaction = 0
	log = True
	def __init__(self):
		return self
	
	@staticmethod
	def transaction():
		RVEngine.nextTransaction += 1
		return RVEngine.nextTransaction
	
	@staticmethod
	def script(code, callback=""):
		print code
		tid = RVEngine.transaction()
		n = 256
		list = [code[i:i+n] for i in range(0, len(code), n)]
		
		print list
		RVEngine.queue.append(str(tid) + ":\0000:\000:\0000:" + callback)
		for l in list:
			RVEngine.queue.append(str(tid) + ":\0000:\030:\0000:" + l)
		RVEngine.queue.append(str(tid) + ":\0000:\001:\0000:")
		return "\n".join(RVEngine.queue)
	
	@staticmethod
	def execute(code, callback=""):
		return RVEngine.script(code,callback)
		
	
	@staticmethod
	def execMP(code, callback=""):
		str = "[{" + code + "}] call EX_fnc_MPexec"
		return RVEngine.execute(str,callback)
		
	@staticmethod	
	def next():
		if len(RVEngine.queue) == 0:
			return 0
				
		return RVEngine.queue.pop(0)
	
	@staticmethod
	def log(message,file=__file__):
		if RVEngine.log:
			return RVEngine.execute('[str("' + message + '"), "' + file + '"] call EX_fnc_log;');
		else:
			return ""

	@staticmethod
	def createUnit(unit):
		code = []
		if unit.side is not None and unit.clazz is not None and unit.posATL is not None:
			code.append('_unit = (createGroup ' + unit.side + ') createUnit ["' + unit.clazz + '", ' + unit.posATL + ', [], 0, "NONE"];')
		else:
			return False # could not create unit.
		
		return RVEngine.script(" ".join(code))
	
	@staticmethod
	def loadUnit(unit):
		code = []
		
		# restore variables
		if unit.variables is not None:
			code.append('[' + str(unit) + ', ' + unit.variables + '] call EX_fnc_setAllVariables;')
			
		# restore rank
		if unit.rank is not None:
			code.append(str(unit) + ' setRank "' + unit.rank+ '";')
			
		# restore skill
		if unit.skill is not None:
			code.append(str(unit) + " setSkill " + unit.skill + ";")
			
		# restore loadout if exist
		if unit.loadout is not None:
			code.append('[' + str(unit) + ', ' + unit.loadout + '] call EX_fnc_setLoadOut;')
		
		# restore animation
		if unit.animation is not None:
			code.append(str(unit) + ' playMoveNow "' + unit.animation + '";')
			
		# restore dir
		if unit.dir is not None:
			code.append(str(unit) + " setDir " + unit.dir + ";")
				
		# restore pos
		if unit.posATL is not None:
			code.append(str(unit) + " setPosATL " + unit.posATL + ";")
		
		
		
		#RVEngine.log("Code is: " + "\n".join(code))
		return RVEngine.script(" ".join(code))
			
