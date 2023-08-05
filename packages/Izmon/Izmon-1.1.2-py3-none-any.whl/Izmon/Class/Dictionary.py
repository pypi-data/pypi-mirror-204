class Dictionary:
	def dic(): #イズモン辞典を表示
		from .Basic.Common_Function import Common_Function as co_f
		from .Basic.Common_Variable import Common_Variable as co_v
		from .Basic.Settings import Settings as st
		IZ_SET = st.IZUMON_SETTING
		RACE = st.RACE
		co_f.show("=" * st.SEPALATE_LEN, 0)
		action = co_f.typing("何をするのじゃ？ 0:Myイズモン一覧を見る 1:種族値を見る",1 , 2)
		co_f.show("=" * st.SEPALATE_LEN, 0)
		if action == 0:
			for i in range(st.IZ_NUM):
				if co_v.fellows[i] == 1:
					print(IZ_SET[i][1])
					print(" | コード: %s 種族: %s HP: %d 攻撃: %d 防御: %d 特攻: %d 特防: %d" %
					(IZ_SET[i][0], RACE[IZ_SET[i][2]], IZ_SET[i][3], IZ_SET[i][4], IZ_SET[i][5], IZ_SET[i][6], IZ_SET[i][7]))
		else:
			while True:
				iz = co_f.typing("どのイズモンの種族値を見るのじゃ？",1, st.IZ_NUM + 1) - 1 #コードと番地は1ずれている
				co_f.show("=" * st.SEPALATE_LEN, 0)
				print(IZ_SET[iz][1])
				print(" | -- コード: %s 種族: %s HP: %d 攻撃: %d 防御: %d 特攻: %d 特防: %d" %
				(IZ_SET[iz][0], RACE[IZ_SET[iz][2]], IZ_SET[iz][3], IZ_SET[iz][4], IZ_SET[iz][5], IZ_SET[iz][6], IZ_SET[iz][7]))
				co_f.show("=" * st.SEPALATE_LEN, 0)
				action = co_f.typing("どうするのじゃ？ 0:戻る 1:まだ見る", 1, 2)
				if action == 0:
					break