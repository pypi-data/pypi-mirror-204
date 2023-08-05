class Gym:
	from .Basic.Settings import Settings as st
	from .Basic.Common_Function import Common_Function as co_f
	from .Basic.Common_Variable import Common_Variable as co_v
	from .Battle.Battle import Battle as bat
	from .Battle.Battle_Set import Battle_Set as bat_s

	hp_me = [0, 0, 0, 0, 0, 0]
	
	def create_party(self):
		party_num = []
		num = 0
		nums = []
		action = self.co_f.typing("どうするのじゃ？ 0:削除 1:追加 2:全削除", 1, 3)
		if action == 0:
			print("現在のパーティー一覧")
			print("~" * self.st.SEPALATE_LEN)
			for i in range(self.st.PARTY_NUM):
				party_num.append(self.co_v.party[i])
				if self.co_v.party[i] == 0:
					continue
				print(i, ":", self.st.IZUMON_SETTING[party_num[i]][1])
			print("~" * self.st.SEPALATE_LEN)
			kind = self.co_f.typing("どれを削除しますか？", 1, self.st.PARTY_NUM)
			party_num[kind] = 0
			self.co_v.party[kind] = 0
			for i in range(self.st.PARTY_NUM - 1):
				if party_num[i] == 0:
					party_num[i] = party_num[i + 1]
					party_num[i + 1] = 0
		elif action == 1:
			nums = []; num = 0
			print("~" * self.st.SEPALATE_LEN)
			print("手持ちのイズモン一覧")
			for i in range(self.st.IZ_NUM):
				if self.co_v.fellows[i] == 1:
					print(" | --", num, self.st.IZUMON_SETTING[i][1])
					nums.append(self.st.IZUMON_SETTING[i][0] - 1)
					num += 1
			print("~" * self.st.SEPALATE_LEN)
			action = self.co_f.typing("どれを追加するのじゃ?", 1, num)
			iz = nums[action]
			if iz in self.co_v.party:
				print("もうパーティーにおるぞ")
			else:
				self.co_v.party[self.bat_s.count_party()] = iz
				print("追加したぞ")
		elif action == 2:
			for i in range(self.st.PARTY_NUM):
				self.co_v.party[i] = 0
			print("全部削除したぞ")
		return
	
	def battle_by_code(self):
		return
	
	def battle_by_default(self):
		leadar_len = len(self.st.GYM_DEFAULT_NAME)
		print("ジムリーダー一覧")
		print("~" * self.st.SEPALATE_LEN)

		for i in range(leadar_len):
			print(f" | -- {i} :{self.st.GYM_DEFAULT_NAME[i][0]} ( {self.st.GYM_DEFAULT_NAME[i][1]} )")
		
		print("~" * self.st.SEPALATE_LEN)
		action = self.co_f.typing(f"どのジムリーダーと戦うのじゃ？( {str(leadar_len)} でやめる)", 1, leadar_len)
		if action == leadar_len:
			self.co_f.show("やめるのじゃな")
			return
		leadar = self.st.GYM_DEFAULT[action]
		gym_num = len(leadar)
		for i in range(gym_num):
			self.hp_me[i] = self.st.IZUMON_SETTING[self.co_v.party[i]][3]
		for i in range(gym_num):
			
			res = self.bat.battle(leadar[i] - 1, 1)
			if res == 0:
				self.co_f.show("またチャレンジするんじゃぞ")
				break
			elif res == 1 and i != gym_num:
				print("=" * self.st.SEPALATE_LEN)
			elif res == 1 and i == gym_num:
				self.co_f.show("チャンレンジ成功")
				self.co_f.show("よく倒したな")
				self.get_badge(action)
			elif res == 2:
				self.co_f.show("チャレンジ失敗")
				self.co_f.show("またチャレンジするんじゃぞ")
				break
		return
	
	def gym_main(self):
		print("=" * self.st.SEPALATE_LEN)
		self.co_f.show("イズモンジムにようこそ!")
		while True:
			self.co_f.show("何をするのじゃ？", 0)
			action = self.co_f.typing("0:パーティーを変える 1:ジムリーダーと戦う 2:バッジ一覧を見る 3:ジムを出る", 1, 4)
			if action == 0:
				self.create_party()
			elif action == 1:
				if self.bat_s.set_ene_level(1) < self.st.LEVEL_MAX[max(0, sum(self.co_v.badges) - 1)]:
					self.co_f.show(f"パーティーのレベルが低すぎるぞ(あと{self.st.LEVEL_MAX[max(0, sum(self.co_v.badges) - 1)] - self.bat_s.set_ene_level(1)}レベル)")
					self.co_f.show("もう少しバトルでイズモンを強くしてから来るのじゃ")
					continue
				if sum(self.co_v.party) != 0:
					self.battle_by_default()
				else:
					self.co_f.show("パーティーにイズモンがいないぞ")
					self.co_f.show("イズモンなしでは戦えんぞ")
					continue
			elif action == 2:
				self.show_badge()
			else:
				if sum(self.co_v.party) != 0:
					self.co_f.show("また来るのじゃぞ")
					break
				else:
					self.co_f.show("パーティーにイズモンがいないぞ")
			print("-" * self.st.SEPALATE_LEN)
		for i in range(self.st.PARTY_NUM):
			self.hp_me[i] = 0
		print("=" * self.st.SEPALATE_LEN)
		return
	
	def get_badge(self, leader : int):
		self.co_v.badges[leader] = 1
		self.co_f.show("バッジを獲得したぞ")
		return
	
	def show_badge(self):
		print("手持ちのバッジ一覧")
		print("~" * self.st.SEPALATE_LEN)
		for i in range(len(self.co_v.badges)):
			if self.co_v.badges[i] == 1:
				print(f"{self.st.GYM_DEFAULT_NAME[i][0]} ( {self.st.GYM_DEFAULT_NAME[i][1]}")
		print("~" * self.st.SEPALATE_LEN)
		return
