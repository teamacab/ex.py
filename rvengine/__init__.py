from textwrap import wrap, TextWrapper
import time
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
		list = [code[i:i + n] for i in range(0, len(code), n)]

		print list
		RVEngine.queue.append(str(tid) + ":\0000:\000:\0000:" + callback)
		for l in list:
			RVEngine.queue.append(str(tid) + ":\0000:\030:\0000:" + l)
		RVEngine.queue.append(str(tid) + ":\0000:\001:\0000:")
		return "\n".join(RVEngine.queue)

	@staticmethod
	def execute(code, callback=""):
		return RVEngine.script(code, callback)


	@staticmethod
	def execMP(code, callback=""):
		str = "[{" + code + "}] call EX_fnc_MPexec"
		return RVEngine.execute(str, callback)

	@staticmethod
	def next():
		if len(RVEngine.queue) == 0:
			return 0

		return RVEngine.queue.pop(0)

	@staticmethod
	def log(message, file=__file__):
		if RVEngine.log:
			# return RVEngine.execute('[str("' + message + '"), "' + file + '"] call EX_fnc_log;');
			return RVEngine.execute('diag_log "' + message + '"')
		else:
			return ""

	@staticmethod
	def createUnit(unit):
		code = []
		# code.append('private "_unit";')
		if unit.side is not None and unit.clazz is not None and unit.posATL is not None:
			code.append('_unit = (createGroup WEST) createUnit ["' + unit.clazz + '", ' + unit.posATL + ', [], 0, "NONE"];')
			code.append('_unit setVariable["pyjarma", true, true];')
			# code.append('_py=format["ex.updateNetId(""' + unit.ref + '"", ""%1"")", netid _unit];')
			# code.append('[_py] call EX_fnc_PY;')
			# code.append("sleep 0.02;")

		else:
			return False  # can not create unit.

		# if varname
		if unit.varname is not None:
			code.append('_unit setVehicleVarName "' + unit.varname + '";')
			code.append(unit.varname + ' = _unit;');
			code.append('publicVariable "' + unit.varname + '";')

		# restore variables
		if unit.variables is not None:
			code.append('[_unit, ' + unit.variables + '] call EX_fnc_setAllVariables;')

		# restore rank
		if unit.rank is not None:
			code.append('_unit setRank "' + unit.rank + '";')

		# restore skill
		if unit.skill is not None:
			code.append('_unit setSkill ' + unit.skill + ';')

		# restore loadout if exist
		if unit.loadout is not None:
			code.append('[_unit, ' + unit.loadout + '] call EX_fnc_setLoadOut;')

		# restore animation
		if unit.animation is not None:
			code.append('_unit playMoveNow "' + unit.animation + '";')

		# restore dir
		if unit.dir is not None:
			code.append('_unit setDir ' + unit.dir + ";")

		# restore pos
		if unit.posATL is not None:
			code.append('_unit setPosATL ' + unit.posATL + ";")

		# run init
		if unit.init is not None:
			code.append('_unit call compile format["' + unit.init + '"];');

		# RVEngine.log("Code is: " + "\n".join(code))
		RVEngine.script(" ".join(code))
		return " ".join(code)

	@staticmethod
	def loadPlayer(unit):
		code = []
		code.append('private ["_unit"]; _unit = ' + unit.varname + ';')
		# restore variables
		if unit.variables is not None:
			code.append('[_unit, ' + unit.variables + '] call EX_fnc_setAllVariables;')

		# restore rank
		if unit.rank is not None:
			code.append('_unit setRank "' + unit.rank + '";')

		# restore skill
		if unit.skill is not None:
			code.append('_unit setSkill ' + unit.skill + ';')

		# restore loadout if exist
		if unit.loadout is not None:
			code.append('[_unit, ' + unit.loadout + '] call EX_fnc_setLoadOut;')

		# restore animation
		if unit.animation is not None:
			code.append('_unit playMoveNow "' + unit.animation + '";')

		# restore dir
		if unit.dir is not None:
			code.append('_unit setDir ' + unit.dir + ";")

		# restore pos
		if unit.posATL is not None:
			code.append('_unit setPosATL ' + unit.posATL + ";")

		# run init
		if unit.init is not None:
			code.append('_result = _unit call compile ' + unit.init);

		RVEngine.log("Code is: " + "\n".join(code))
		RVEngine.script(" ".join(code))
		return " ".join(code)

