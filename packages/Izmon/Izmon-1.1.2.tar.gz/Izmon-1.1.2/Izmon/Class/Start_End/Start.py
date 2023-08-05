class Start:
	from ..Basic.Common_Function import Common_Function as co_f
	from ..Basic.Common_Variable import Common_Variable as co_v
	from ..Basic.Settings import Settings as st
	from ..Battle.Battle_Caluculate import Battle_Caluculate
	from ..Gym import Gym
	import datetime as dt
	import time

	gym = Gym(); bat_cal = Battle_Caluculate
	
	MSG_SELECT = ["イズットモンスターの世界へ ようこそ！ わしの名前は オーキ二 みんなからは イズモン はかせと 慕われておるよ ",
	"イズットモンスター………イズモン この 世界には イズットモンスターと 呼ばれる いきもの達が いたる所に 住んでいる! ",
	"人は イズモンたちと 仲良く遊んだり 一緒に戦ったり………… 助け合いながら 暮らしているのじゃ ",
	"しかし わしらは イズモンの全てを 知っている 訳ではない イズモンの 秘密は まだまだ いっぱい ある！ ",
	"わしは それを 解き明かすために 毎日 イズモンの 研究を 続けている という わけじゃ！ ",
	"さて…… そろそろ 君の 名前を 教えてもらおう！",
	" よ イズモンを1匹も持っていないだと? しかたがない この3匹から1匹選ぶのじゃ",
	"3匹のイズモンから好きなものを選ぶのじゃ",
	"じゃな。 わかったぞ",
	" ! 準備は いいかな？ いよいよ これから きみの 物語が 始まる！ ",
	"楽しいことも 苦しいことも いっぱい きみを 待っているだろう！ 夢と 冒険と！ ",
	"イズットモンスターの 世界へ！ レッツ ゴー"]

	def set_up(self): #開始する
		from ..Save_Code.Decode import Decode
		from ..CloudSave.Download import Download as d
		rem = 0
		print("イズットモンスター(Ver", self.st.VERSION, ")")
		ty = self.co_f.typing("0:はじめから 1:続きから", 1, 2)
		self.co_f.show("=" * self.st.SEPALATE_LEN, 0)
		if ty == 0:
			self.select_izmon()
		else:
				ty = self.co_f.typing("クラウドからロードしますか？ 0:する 1:しない", 1, 2)
				if ty == 0:
					while True:
						print("~" * self.st.SEPALATE_LEN)
						if rem != 0:
							rem = rem - self.dt.datetime.now()
							rem = int(rem.total_seconds() + 0.5)
						else:
							rem = 0
						print(rem)
						u_name = self.co_f.typing("ユーザー名", 0)
						pas = self.co_f.typing("パスワード", 0)
						print("~" * self.st.SEPALATE_LEN)

						if rem != 0:
							print(f"再試行されるまで{rem}秒お待ちください。")
						self.time.sleep(rem) #待機時間

						res, code, name = d.download(u_name, pas)
						if res:
							print("正常にダウンロードされました。")
							self.co_v.player_name = name
							res = Decode.decode(code)
							if res == 1:
								print("~" * self.st.SEPALATE_LEN)
								print("無効なコードじゃ。不正はダメじゃぞ")
								continue
							else:
								print("~" * self.st.SEPALATE_LEN)
								print("データを読み込みました。")
								break
						else:
							print(code)
							print("~" * self.st.SEPALATE_LEN)
							ty = self.co_f.typing("再試行しますか？ 0:する 1:しない(手動でロードできます)", 1, 2)
							print("~" * self.st.SEPALATE_LEN)
							if ty == 0:
								now = self.dt.datetime.now()
								rem = now + self.dt.timedelta(seconds=self.st.RETRY)
								continue
							else:
								self.manual()
				else:
					self.manual()
					
	def select_izmon(self): #開始時のイズモンを選択
		for i in range(6):
			self.co_f.show(self.MSG_SELECT[i])
		player = self.co_f.typing("名前", 0)
		self.co_v.player_name = player
		self.co_f.show(player + self.MSG_SELECT[6])
		self.co_f.show(self.MSG_SELECT[7])
		poc = self.co_f.typing("0:バニージャンプ 1:テクノドラゴン 2:ナイトライダー", 1, 3)
		if poc == 0:
			code = 19 - 1
		elif poc == 1:
			code = 33 - 1
		else:
			code = 36 - 1
		self.co_v.fellows[code] = 1
		self.co_v.party[0] = code
		self.gym.hp_me[0] = self.bat_cal.set_hp(code, 1)
		self.co_f.show(self.st.IZUMON_SETTING[code][1] + self.MSG_SELECT[8])
		self.co_f.show("では " + player + self.MSG_SELECT[9])
		self.co_f.show(self.MSG_SELECT[10])
		self.co_f.show(self.MSG_SELECT[11])
		self.co_f.show("=" * self.st.SEPALATE_LEN, 5)
		return

	def manual(self):
		from ..Save_Code.Decode import Decode
		while True:
			player = self.co_f.typing("君の名前を教えるのじゃ（セーブデータコードを持っているならその時の名前を教えるのじゃ）：", 0)
			self.co_v.player_name = player
			play_type = self.co_f.typing(player + " よ、セーブデータコードは持っておるか？ 0:ある 1:ない", 1, 2)
			if play_type == 0:
				print("=" * self.st.SEPALATE_LEN)
				code = self.co_f.typing("セーブデータコード：",0)
				print("=" * self.st.SEPALATE_LEN)
				res = Decode.decode(code)
				if res == 1:
					print("無効なコードじゃ。不正はダメじゃぞ")
				else:
					print("データを読み込みました。")
					break
			else:
				self.co_f.show("コードがないのなら初めから始めるぞ")
				self.co_f.show("=" * self.st.SEPALATE_LEN, 0)
				self.select_izmon()
				break
		return