class Download:
	def download(u_name, pas):
		from .Common import Common
		import requests
		import json
		c = Common()
		
		res, name, sheet, row, pass_hash = c.get_values(u_name, pas)
		
		if not res:
			return False, "不正なユーザーネーム又はパスワードです。", ""
		url = "https://izmon-cloud-save-auv0edkp.an.gateway.dev/download"
		data = {
		"name": name,
		"sheet": str(sheet),
		"password" : pass_hash,
		"row" : str(row)
		}
	
		headers = {"Content-Type": "application/json"}
		code = ""; name = ""
		response = requests.post(url, data=json.dumps(data), headers=headers)
		status = response.status_code
		
		if status == '400':
			return False, "エラーが発生しました。時間を置いて再試行してください。", ""
		elif status == '403':
			return False, "ユーザーネームが一致しません。", ""
		elif status == '405':
			return False, "パスワードが一致しません。", ""
		
		response_json = response.json()
		name = response_json['name']
		code = response_json['code']

		return True, code, name
	