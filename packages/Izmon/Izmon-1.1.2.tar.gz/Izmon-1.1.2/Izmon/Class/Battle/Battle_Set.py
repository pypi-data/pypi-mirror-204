class Battle_Set:
	def count_party():
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st		
		party_num = 0
		for i in range(st.PARTY_NUM):
			if co_v.party[i] != 0:
				party_num += 1
		return party_num
	
	def select_ene():
		import random
		from ..Basic.Settings import Settings as st
		ene_num = random.randint(0,st.IZMON_P_LEN)
		ene = st.IZMON_P[ene_num]
		return ene
	
	def set(ene : int, typ : int): #各種値を設定
		from .Battle_Caluculate import Battle_Caluculate as bat_ca
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st	
		from ..Gym import Gym as gym
		import statistics
	
		tech = [["", "", "", "", "", ""],
		  		["", "", "", "", "", ""],
				["", "", "", "", "", ""],
				["", "", "", "", "", ""],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0]]
		damage_all = [[0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0]]
		data = []
		
		IZ_SET = st.IZUMON_SETTING

		for i in range(st.PARTY_NUM):
			me_num = co_v.party[i]
			if me_num == 0:
				me_com = []
			else:
				if typ == 1:
					hp = gym.hp_me[i]
				else:
					hp = bat_ca.set_hp(me_num, co_v.level[me_num])
				me_com = [IZ_SET[me_num][0], IZ_SET[me_num][1], hp, st.SPETIAL_NUM, co_v.level[me_num]]
			data.append(me_com)
			tech = bat_ca.store_tech(tech, me_num, ene, i)
		me_level = []
		for i in range(st.PARTY_NUM):
			me_num = co_v.party[i]
			if me_num == 0:
				continue
			else:
				me_level.append(co_v.level[me_num])
		if typ == 0:
			ene_level = int(statistics.median(me_level))
		else:
			ene_level = st.LEVEL_MAX[sum(co_v.badges) + 1]

		ene_com = [IZ_SET[ene][0], IZ_SET[ene][1], bat_ca.set_hp(ene, ene_level), st.SPETIAL_NUM, ene_level]
		data.append(ene_com)

		for i in range(st.PARTY_NUM):
			if co_v.party[i] != 0:
				tech, damage_all = bat_ca.calculate_damage(damage_all, tech, co_v.party[i], ene, i, ene_level)
		
		return data, damage_all, tech

	def set_ene_level(typ : int):
		from ..Basic.Settings import Settings as st
		from ..Basic.Common_Variable import Common_Variable as co_v
		import statistics

		me_level = []
		for i in range(st.PARTY_NUM):
			me_num = co_v.party[i]
			if me_num == 0:
				continue
			else:
				me_level.append(co_v.level[me_num])
		if typ == 0:
			ene_level = int(statistics.median(me_level))
			print(ene_level)
		else:
			ene_level = st.LEVEL_MAX[sum(co_v.badges) + 1]
		return ene_level