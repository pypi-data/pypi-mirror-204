class End:
	from ..Basic.Common_Function import Common_Function as co_f
	from ..Basic.Common_Variable import Common_Variable as co_v
	from ..Basic.Settings import Settings as st
	import datetime as dt
	import time
	
	def main(self): #データをセーブする		
		ty = self.co_f.typing("データをセーブしますか？ 0:する 1:しない", 1, 2)
		print("~" * self.st.SEPALATE_LEN)
		if ty == 0:
			self.save()
		else:
			ty = self.co_f.typing("本当にしないでよろしいですか? 0:する 1:しない", 1, 2)
			print("~" * self.st.SEPALATE_LEN)
			if ty == 0:
				self.save
		print("=" * self.st.SEPALATE_LEN)
		return
	
	def save(self):
		from ..Save_Code.Encode import Encode
		from ..CloudSave.Upload import Upload as u
		code = Encode.encode()
		rem = 0
		ty = self.co_f.typing("クラウドセーブを利用しますか？(事前登録が必要です) 0:利用する 1:利用しない", 1, 2)
		print("~注意事項~")
		print("データは上書きされます。上書きしたくない場合は新たにアカウントを作成してください。")
		if ty == 0:
			while True:
				if self.co_v.retry != 0:
					rem = rem - self.dt.datetime.now()
					rem = int(rem.total_seconds() + 0.5)
				else:
					rem = 0
				u_name = self.co_f.typing("ユーザー名", 0)
				pas = self.co_f.typing("パスワード", 0)
				print("~" * self.st.SEPALATE_LEN)

				self.time.sleep(rem) #待機時間
				if rem != 0:
						print(f"再試行されるまで{rem}秒お待ちください。")
				res = u.upload(u_name, pas, code)
				
				if res[0]:
					print("正常に保存されました。")
					break
				else:
					print(res[1])
					ty = self.co_f.typing("再試行しますか？ 0:する 1:しない(コードは表示されます)", 1, 2)
					print("~" * self.st.SEPALATE_LEN)
					if ty == 0:
						now = self.dt.datetime.now()
						rem = now + self.dt.timedelta(seconds=self.st.RETRY)
					else:
						print("-" * self.st.SEPALATE_LEN)
						print("プレイヤー名と共に保管してください。")
						print(f"コード: {code}")
						print(f"プレイヤー名: {self.co_v.player_name}")