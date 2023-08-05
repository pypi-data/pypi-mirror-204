class Upload:
    def upload(u_name, pas, code):
        from .Common import Common
        from ..Basic.Common_Variable import Common_Variable as co_v

        import requests
        import json

        c = Common()
        res, name, sheet, row, pass_hash = c.get_values(u_name, pas)
        if not res:
            return False, "不正なユーザーネーム又はパスワードです。"

        url = "https://izmon-cloud-save-auv0edkp.an.gateway.dev/upload"
        data = {
        "name": str(name),
        "code": str(code),
        "sheet": str(sheet),
        "password" : pass_hash,
        "row" : str(row),
        "player_name" : str(co_v.player_name)
        }
    
        headers = {"Content-Type": "application/json"}
    
        response = requests.post(url, data=json.dumps(data), headers=headers)
        status = response.status_code
        if status == '200':
            return True, ""
        elif status == '400':
            return False, "エラーが発生しました。時間を置いて再試行してください。"
        elif status == '403':
            return False, "ユーザーネームが一致しません。"
        elif status == '405':
            return False, "パスワードが一致しません。"
    