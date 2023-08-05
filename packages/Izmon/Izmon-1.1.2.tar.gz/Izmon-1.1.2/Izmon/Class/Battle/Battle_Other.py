class Battle_Other:
	def comp(self): #コンプリートしたとき
		import time
		print('全てのイズモンを獲得した!')
		time.sleep(1)
		return
	
	def set_turn(self):
		turn = 0
		return turn
		
	def get(self, ene : int): #獲得処理
		from ..Basic.Common_Function import Common_Function as co_f
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st
		import random
		IZ_SET = st.IZUMON_SETTING
		prob = IZ_SET[ene][8] #獲得率
		if random.random() <= prob:
			before = sum(co_v.fellows) #獲"得前の数
			print(IZ_SET[ene][1], "を獲得した!")
			print("種族: %s HP: %d 攻撃: %d 防御: %d 特攻: %d 特防: %d" %
			(st.RACE[IZ_SET[ene][2]], IZ_SET[ene][3], IZ_SET[ene][4], IZ_SET[ene][5], IZ_SET[ene][6], IZ_SET[ene][7]))
			co_v.fellows[ene] = 1
			if sum(co_v.fellows) == st.IZ_NUM and before == st.IZ_NUM - 1: #初めてコンプリートした時のみ実行
				self.comp()
		else:
			co_f.show("逃げられた…")
		return
		
	def turn_change(self, turn : int): #ターンを切り替える
		if turn == 1:
			return 0
		else:
			return 1
		
	def change_izmon(self, party_num, typ):
		from ..Basic.Common_Function import Common_Function as co_f
		from ..Basic.Common_Variable import Common_Variable as co_v
		from .Battle_Caluculate import Battle_Caluculate as ba_c
		from ..Basic.Settings import Settings as st
		from ..Gym import Gym
		gym = Gym()

		print("~" * st.SEPALATE_LEN)
		print("パーティー一覧")
		if typ == 1:
			for i in range(st.PARTY_NUM):
				if co_v.party[i] != 0:
					print(i, ":", st.IZUMON_SETTING[co_v.party[i]][1], "HP:", gym.hp_me[i])
		else:
			for i in range(st.PARTY_NUM):
				if co_v.party[i] != 0:
					print(i, ":", st.IZUMON_SETTING[co_v.party[i]][1], "HP:", ba_c.set_hp(co_v.party[i], co_v.level[i]))
		print("~" * st.SEPALATE_LEN)
		me_sub = co_f.typing("どれを出す？", 1, party_num)
		sub = [me_sub, 0]
		return me_sub, sub
	
	def level_up(self, me):
		from ..Basic.Common_Function import Common_Function as co_f
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st
		level_before = co_v.level[me]
		level_max = st.LEVEL_MAX[sum(co_v.badges)]
		co_v.num_killed += 1
		if level_before == level_max:
			co_f.show("レベルが上限じゃぞ")
			co_f.show("ジムでもっと鍛えるのじゃ")
		else:
			if co_v.num_killed == st.LEVELUP_NUM:
				co_f.show("レベルアップした!")
				co_v.level[me] += 1
				co_v.num_killed = 0
			else:
				print("倒した数")
				co_f.show(str(co_v.num_killed) + '/' + str(st.LEVELUP_NUM))
		return