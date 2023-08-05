class Common_Function:
	def show(msg : str, length = "default"): #メッセージ表示(メッセージ, 待機秒数)
		from .Common_Variable import Common_Variable as co_v
		import time
		if length == "default":
			length = co_v.show_length
		print(msg)
		time.sleep(length)
		return
	
	def typing(msg : str, ty : int, num : int = 2): #各種キーボード入力
		while True:
			if ty == 1:
				data = input(msg + " -->> ")
				if data.isdigit() and 0 <= int(data) and int(data) <= num - 1:
					data = int(data)
					break
				elif data.isdigit() == False:
					print("無効な入力じゃ")
			else:
				data = str(input(msg + " -->> "))
				if data == '':
					print("無効な入力じゃ")
					continue
				break
		return data
