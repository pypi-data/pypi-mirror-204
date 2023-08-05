class Common:
	import datetime as dt
	from ..Basic.Common_Variable import Common_Variable as co_v
	def hash_sha1(self, password):
		import hashlib
		
		password_hash = str(hashlib.sha1(password.encode('utf-8')).hexdigest())
		password_1 = password_hash[:10]
		password_2 = password_hash[10:20]
		password_save = str(int(password_1, 16)).zfill(10) + str(int(password_2, 16)).zfill(10)
		password_save = password_save[:20]
		return password_save
	
	def regular(self, value : str):
		import re
		res = re.fullmatch(".*[0-9]{6}", value)
		if res == None:
			return False
		return True
	
	def get_values(self, u_name, pas):
		if not self.regular(u_name):
			return False, "", "", "", ""
		elif len(pas) > 20 or len(u_name) > 26:
			return False, "", "", "", ""
		name = u_name[:-6]
		sheet = int(u_name[-6:-4])
		row = int(u_name[-4:])
		pass_hash = self.hash_sha1(pas)
		return True, name, sheet, row, pass_hash
	
	def retry(self):
		now = self.dt.datetime.now()
		self.co_v.retry = now + self.dt.timedelta(seconds=15)