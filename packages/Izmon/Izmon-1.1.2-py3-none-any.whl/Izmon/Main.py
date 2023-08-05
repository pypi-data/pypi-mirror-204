def main():
	# from Class.Basic.Common_Function import Common_Function as co_f
	# from Class.Gym import Gym
	# from Class.Dictionary import Dictionary as dic
	# from Class.Events.Events_Latest import Events_Latest as ev
	# from Class.Start_End.Start import Start
	# from Class.Start_End.End import End
	# from Class.Set import Set
	# from Class.Battle.Battle_Set import Battle_Set as bat_s
	# from Class.Battle.Battle import Battle as ba
	from Izmon.Class.Basic.Common_Function import Common_Function as co_f
	from Izmon.Class.Gym import Gym
	from Izmon.Class.Dictionary import Dictionary as dic
	from Izmon.Class.Events.Events_Latest import Events_Latest as ev
	from Izmon.Class.Start_End.Start import Start
	from Izmon.Class.Start_End.End import End
	from Izmon.Class.Set import Set
	from Izmon.Class.Battle.Battle_Set import Battle_Set as bat_s
	from Izmon.Class.Battle.Battle import Battle as ba
	gym = Gym(); start = Start(); end = End(); set = Set()
	start.set_up()
	while True:
		action = co_f.typing("どうしますか? 0:バトルする 1:ジムに行く 2:イズモン辞典 3:イベント 4:設定 5:やめる", 1, 6)
		if action == 0:
			enemy = bat_s.select_ene()
			ba.battle(enemy, 0)
		elif action == 1:
			gym.gym_main()
		elif action == 2:
			dic.dic()
		elif action == 3:
			ev.events()
		elif action == 4:
			set.main()
		elif action ==5:
			action = co_f.typing("本当にやめますか? 0:やめる 1:続ける", 1, 2)
			if action == 0:
				break
			else:
				continue
	end.main()
main()