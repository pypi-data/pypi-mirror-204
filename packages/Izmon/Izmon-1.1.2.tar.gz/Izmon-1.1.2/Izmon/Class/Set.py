class Set:
    from .Basic.Common_Function import Common_Function as co_f
    from .Basic.Common_Variable import Common_Variable as co_v
    from .Save_Code.Encode import Encode as encode
    from .Save_Code.Decode import Decode as decode

    from .Basic.Settings import Settings as st

    def main(self):
        print("=" * self.st.SEPALATE_LEN)
        while True:
            action = self.co_f.typing("何をしますか？ 0:データコード名前変更 1:表示秒数変更 2:プレイヤー名変更 3:やめる", 1, 4)
            if action == 0:
                self.change_name_code()
            elif action == 1:
                self.change_show_length()
            elif action == 2:
                self.change_name_v()
            else:
                break
            print("-" * self.st.SEPALATE_LEN)
        print("=" * self.st.SEPALATE_LEN)
        return
    
    def change_name_v(self):
        self.co_v.player_name = self.co_f.typing("新しいプレイヤー名", 0)
        print("変更しました。")

    def change_name_code(self):
        tmp_fellow = self.co_v.fellows
        tmp_party = self.co_v.party
        tmp_level = self.co_v.level
        tmp_badges = self.co_v.badges
        tmp_name = self.co_v.player_name
        self.co_f.show("データコードに保存されているプレイヤー名を変更します。", 2) 
        code = self.co_f.typing("データコード", 0)
        self.co_v.player_name = self.co_f.typing("名前", 0)
        self.decode.dncode(code)
        code_new = self.encode.encode()
        self.co_v.fellows = tmp_fellow
        self.co_v.party = tmp_party
        self.co_v.level= tmp_level
        self.co_v.badges = tmp_badges
        self.co_v.player_name = tmp_name
        del tmp_badges, tmp_fellow, tmp_level, tmp_party, tmp_name
        print("変更しました。")
        print(f"新しいコード: {code_new}")
        return
    
    def change_show_length(self):
        length = self.co_f.typing("表示秒数を入力してください(最長10秒)", 1, 10)
        self.co_v.show_length = length
        print("設定しました。")
        return
