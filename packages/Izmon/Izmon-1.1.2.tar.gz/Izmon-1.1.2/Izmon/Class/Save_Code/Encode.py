class Encode:
	def encode():
		from ..Basic.Settings import Settings as st
		from ..Basic.Common_Variable import Common_Variable as co_v
		import hashlib
		
		data_fellow = ''; data_level = ''; data_party = ''; data_badge = ''; hash_name = ''
		
		hash_name = hashlib.sha1(co_v.player_name.encode('utf-8')).hexdigest()
		hash_10 = str(int(hash_name, 16))
		
		for i in range(st.CODE_CAP):
			if i > st.IZ_NUM:
				data_fellow = data_fellow + '0' * (st.CODE_CAP - st.IZ_NUM - 1)
				data_level += '000' * (st.CODE_CAP - st.IZ_NUM - 1)
				break
			data_fellow += str(co_v.fellows[i])
			data_level += str(co_v.level[i]).zfill(3)
		data_fellow_10 = hash_10[30] + str(int(data_fellow, 2)).zfill(st.CODE_FELLOW_LEN)
		
		for i in range(st.PARTY_NUM):
			data_party += str(co_v.party[i]).zfill(3)
		
		for i in range(len(co_v.badges)):
			data_badge += str(co_v.badges[i])
		data_badge_10 = str(int(data_badge, 2)).zfill(3)
		
		
		data = str(hash_10[11] + data_fellow_10 + data_level + data_party + data_badge_10 + hash_10[:10])
		
		check_digit = str(int(data) % int(hash_10[20]))
		
		data += check_digit
		
		data = int(data)
		
		data_16 = format(data, 'x')
		
		return data_16