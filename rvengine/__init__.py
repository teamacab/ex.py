from textwrap import wrap, TextWrapper


def createUnit(unit):
	code = []
	if unit.side is not None and unit.clazz is not None and unit.posATL is not None:
		code.append('_unit = (createGroup ' + unit.side + ') createUnit ["' + unit.clazz + '", ' + unit.posATL + ', [], 0, "NONE"];')
	else:
		return False # could not create unit.
	
	# restore rank
	if unit.rank is not None:
		code.append('_unit setRank "' + unit.rank+ '";')
		
	# restore skill
	if unit.skill is not None:
		code.append("_unit setSkill " + unit.skill + ";")
		
	# restore loadout if exist
	if unit.loadout is not None:
		code.append('[_unit, ' + unit.loadout + '] call EX_fnc_restoreLoadOut;')
		
	
	return RVEngine.script(" ".join(code))

class RVEngine:
	
	instance = None
	queue = []
	FrameNo = 0
	FPS = 0
	FPS_MIN = 0
	TickTime = 0
	Time = 0
	nextTransaction = 0
	
	def __init__(self):
		return self
	
	@staticmethod	
	def splitCount(s, count):
		return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]
	
	@staticmethod
	def transaction():
		RVEngine.nextTransaction += 1
		return RVEngine.nextTransaction
	
	@staticmethod
	def script(code, callback=""):
		print code
		tid = RVEngine.transaction()
		wrapper = TextWrapper(break_long_words=False,break_on_hyphens=False,width=10)
		list = wrapper.wrap(code)
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
			return "['',nil]"
				
		return RVEngine.queue.pop(0)
	
	@staticmethod
	def log(message,file=__file__):
		return RVEngine.execute('[str("' + message + '"), "' + file + '"] call EX_fnc_log');
		