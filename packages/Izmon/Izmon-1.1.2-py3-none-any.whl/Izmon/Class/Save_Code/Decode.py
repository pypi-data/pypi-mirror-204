class Decode:
	def decode(code):
		from ..Basic.Settings import Settings as st
		from ..Basic.Common_Variable import Common_Variable as co_v
		import hashlib
		
		code_in = code
		
		code_10 = str(int(code_in, 16))
		
		has = hashlib.sha1(co_v.player_name.encode('utf-8')).hexdigest()
		hash_10 = str(int(has, 16))
		del has
		
		if not (int(code_10[:-1]) % int(hash_10[20])) == int(code_10[-1]):
			return 1
		code_remove_digit = code_10[:-1]
		del code_10
		
		if not (code_remove_digit[-10:] == hash_10[:10]):
			return 1
		if not (code_remove_digit[0] == hash_10[11]):
			return 1
		if not (code_remove_digit[1] == hash_10[30]):
			return 1
		code_remove_hash = code_remove_digit[2:-10]
		del code_remove_digit
		
		data_fellow = code_remove_hash[:st.CODE_FELLOW_LEN]
		code_removed = code_remove_hash[st.CODE_FELLOW_LEN:]
		data_badge = code_removed[-3:]
		code_removed = code_removed[:-3]
		data_party = code_removed[-(st.PARTY_NUM * 3):]
		data_level = code_removed[:-(st.PARTY_NUM * 3)]
		
		data_fellow_2 = str(format(int(data_fellow), 'b')).zfill(st.CODE_CAP)
		data_badge_10 = str(format(int(data_badge), 'b')).zfill(st.PARTY_NUM)
		for i in range(st.CODE_CAP):
			co_v.fellows[i] = int(data_fellow_2[i])
			co_v.level[i] = int(data_level[(i * 3):(i * 3 + 3)])
			
		for i in range(st.PARTY_NUM):
			co_v.party[i] = int(data_party[(i * 3):(i * 3 + 3)])
			
		for i in range(len(co_v.badges)):
			co_v.badges[i] = int(data_badge_10[i])
		del code_remove_hash; del data_fellow; del code_removed; del data_badge
		del data_level; del data_party; del data_badge_10; del data_fellow_2
		return 0