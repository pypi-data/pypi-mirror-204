class Battle_Caluculate:
	def calculate_damage(damage_all:list, tech:list, me:int, ene:int, i:int, ene_level:int):
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st
		from .Battle_Set import Battle_Set as ba_s
		IZ_SET = st.IZUMON_SETTING; IZ_FIG = st.SETS_FIGHT
		num = [me, ene]
		level = [co_v.level[me], ene_level]
		for j in range(2):
			me_kind = IZ_SET[num[j]][2]
			ene_kind = IZ_SET[num[j - 1]][2]
			attack_normal = (IZ_SET[num[j]][4] * 2 + 30) * level[j] / 100
			attack_spetial = (IZ_SET[num[j]][6] * 2 + 30) * level[j] / 100
			protect_normal = (IZ_SET[num[j - 1]][5] * 2 + 30) * level[j - 1] / 100
			protect_spetial = (IZ_SET[num[j - 1]][7] * 2 + 30) * level[j - 1] / 100
			tech_nomal = (tech[4][i] * 2 + 30) * level[j] / 100
			tech_spetial = (tech[6][i] * 2 + 30) * level[j] / 100
			damage_nomal = ((22 * tech_nomal * attack_normal / protect_normal) * 0.02 + 2) * IZ_FIG[me_kind][ene_kind]
			damage_spe = ((22 * tech_spetial * attack_spetial / protect_spetial) * 0.02 + 2) * IZ_FIG[me_kind][ene_kind]
			if ene_kind == 5:
				damage_all[j][i] = int(damage_nomal * 1.5 + 0.5)
				damage_all[2 + j][i] = int(damage_spe * 1.5 + 0.5)
			else:
				damage_all[j][i] = int(damage_nomal * 2 + 0.5)
				damage_all[2 + j][i] = int(damage_spe * 2 + 0.5)
			expect = (st.ESCAPE_P * 2 + 30) * level[j]
			tech[8 + j][i] = damage_nomal / expect # 命中率を設定
			tech[10 + j][i] = damage_spe / expect

		return tech, damage_all
	
	def store_tech(tech : list, me : int, ene : int, i : int):
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st
		IZ_SET = st.IZUMON_SETTING; TH_NOM = st.TECH_NOMAL; TH_SPE = st.TECH_SPETIAL
		TH_IND = st.TECH_INDIVIDUAL
		
		kind = [IZ_SET[me][2], IZ_SET[ene][2]]
		num = [me, ene]
		for j in range(2):
			if IZ_SET[num[j]][9] == 0:
				tech[j][i] = TH_NOM[0][kind[j]] #技名を格納
				tech[2 + j][i] = TH_SPE[0][kind[j]]
				tech[4 + j][i] = TH_NOM[1][kind[j]]
				tech[6 + j][i] = TH_SPE[1][kind[j]]
			else:
				num_tech = IZ_SET[num[j]][9] - 1 #技番号
				tech[j][i] = TH_IND[0][num_tech]
				tech[2 + j][i] = TH_IND[1][num_tech]
				tech[4 + j][i] = TH_IND[2][num_tech]
				tech[6 + j][i] = TH_IND[3][num_tech]
			
			if "%" in tech[0][i]: #"%"のユーザー名を置き換える
				tech[j][i] = tech[0 + j][i].replace("%", co_v.player_name)
			if "%" in tech[2][i]:
				tech[2 + j][i] = tech[2 + j][i].replace("%", co_v.player_name)
		return tech
	
	def set_hp(izmon : int, level : int):
		from ..Basic.Settings import Settings as st
		hp = (st.IZUMON_SETTING[izmon][3] * 2 + 30) * level / 100 + level + 10
		return int(hp)
