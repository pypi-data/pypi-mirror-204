class Battle:
	def battle(ene : int, typ : int): #typ 0:通常 1:ジム
		import random
		from .Battle_Set import Battle_Set as bat_s
		from .Battle_Other import Battle_Other
		from ..Basic.Common_Function import Common_Function as co_f
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st
		from ..Gym import Gym

		gym = Gym(); bat_o = Battle_Other()

		data , damage_all, tech = [], [], []
		party_num = bat_s.count_party()
		
		turn = bat_o.set_turn()
		print("=" * st.SEPALATE_LEN)
		ene_data = st.IZUMON_SETTING[ene]
		if typ == 0:
			co_f.show("野生の" + ene_data[1] + "が現れた! (種族:" + st.RACE[ene_data[2]] + "）")
		elif typ == 1:
			co_f.show(ene_data[1] + "が現れた!（種族:" + st.RACE[ene_data[2]] + "）")
		ene_data = None
		me_sub, sub = bat_o.change_izmon(party_num, typ)

		data_all, damage_all, tech = bat_s.set(ene, typ)
		while True:
			data = [data_all[me_sub], data_all[st.PARTY_NUM]]
			data_all[me_sub] = data[0]
			data_all[st.PARTY_NUM] = data[1]
			print(data[turn][1], "のターン（HP:",data[turn][2], "）")
			if turn == 0:
				while True:
					ty = co_f.typing("行動を選択 0:攻撃 1:特攻（残り" +str(data[0][3])+ "回）", 1, 2)
					if data[0][3] == 0 and ty == 1:
						print("残り回数がないぞ")
						continue
					elif ty == 1:
						data[0][3] -= 1
						break
					else:
						break
			else: #敵の行動を選択
				if data[1][3] == 0:
					ty = 1
				else:
					ty = random.randint(0, 1)
					data[1][3] -= 1
					
			co_f.show(data[turn][1] + " の 攻撃", )
			co_f.show(data[turn][1] + " の " + tech[ty * 2 + turn][sub[turn]] + " !")
			print("-" * st.SEPALATE_LEN)
			#命中判定
			if tech[8 + turn + ty * 2][sub[turn]] <= random.random():
				co_f.show(data[turn - 1][1] + "は" + str(int(damage_all[ty * 2 + turn][sub[turn]])) + "のダメージを受けた!")
				data[turn - 1][2] -= int(damage_all[ty * 2 + turn][sub[turn]]) #ダメージ分減らす
				if data[turn - 1][2] <= 0:
					data[turn - 1][2] = 0
				if typ == 1:
					gym.hp_me[me_sub] = data[me_sub][2]
			else:
				if turn == 0:
					co_f.show("避けられた!")
				else:
					co_f.show("避けた!")

			co_f.show(data[abs(turn - 1)][1] + " の 残り HP :" + str(data[turn - 1][2]))
			print('-' * st.SEPALATE_LEN)

			if data[0][2] <= 0:
				party_num -= 1
				co_f.show("HPが0になってしまった。")
				if party_num == 0:
					if typ == 0:
						co_f.show(co_v.player_name + " は目の前が真っ暗になった")
						return
					else:
						return 2
				me_sub, sub = bat_o.change_izmon(party_num, typ)
				turn = bat_o.turn_change(turn)
				continue

			if data[1][2] <= 0:
				co_f.show(data[1][1] + " を倒した!")
				if typ == 0:
					bat_o.get(ene)
					bat_o.level_up(me_sub)
					break
				else:
					return 1
			if typ == 0 and turn == 1:
				action = co_f.typing("どうする? 0:続ける 1:交代する 2:逃げる", 1, 3)
				if action == 2 and random.random() >= st.ESCAPE_P:
					co_f.show("逃げられなかった")
					turn = bat_o.turn_change(turn)
					print("-" * st.SEPALATE_LEN)
					continue
				elif action == 2:
					co_f.show("逃げられた!")
					print("-" * st.SEPALATE_LEN)
					break
				elif action == 1:
					me_sub, sub = bat_o.change_izmon(party_num, typ)
					turn = bat_o.turn_change(turn)
					continue
			elif typ == 1 and turn == 0:
				action = co_f.typing("どうする？ 0:続ける 1:やめる(次挑戦するときは最初からになります) 2:交代する", 1, 3)
				if action == 0:
					continue
				elif action == 1:
					return 0
				else:
					me_sub, sub = bat_o.change_izmon(party_num, typ)
			turn = bat_o.turn_change(turn)
		return
