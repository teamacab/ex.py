from ex.database import Unit
import rvengine

def callback(answer):
    print "Got answer: " + answer

u = Unit()
u.side = "WEST"
u.clazz = "C_man_1"
u.posATL = "(getPos player)"
u.loadout = '[["ItemMap","ItemCompass","ItemWatch",""],"",[],"",[],"",[],"U_C_Citizen_clothes3",[],"V_Rangemaster_belt",[],"B_AssaultPack_mcamo",[],[[],"",""],"",""]'
u.rank = "CAPTAIN"
u.skill = "0.423"
print rvengine.createUnit(u)

print rvengine.RVEngine.script("time", "ex.tests.rvengine_createUnit.callback")
