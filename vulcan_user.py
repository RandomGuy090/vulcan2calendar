
from vulcan import Vulcan
from vulcan import Account
from vulcan import Keystore

import os, datetime


class Vulcan_user(object):
	
	def __init__(self):
		print("vulcan user")
		self.account = None
		self.keystore = None
		self.client = None
		self.last_check_date = None

		self.get_account_json()
		self.get_keystore_json()
		self.get_last_check()

		self.client = Vulcan(self.keystore, self.account)


	def get_account_json(self):
		if os.path.exists('account.json'):
			with open("account.json") as f:
				self.account = Account.load(f.read())
				return self.account
		else:
			print(f"no such file: account.json")
			sys.exit(0)


	def get_keystore_json(self):
		if os.path.exists('keystore.json'):
			with open("keystore.json") as f:
				self.keystore = Keystore.load(f.read())
				return self.keystore
		else:
			print(f"no such file: keystore.json")
			sys.exit(0)



	def get_last_check(self):
		if os.path.exists('last_sync.json'):
			with open("last_sync.json") as f:
				self.last_check_date = f.read()
				try:
					self.last_check_date = datetime.datetime.strptime(self.last_check_date.rsplit(".")[0], "%Y-%m-%d %H:%M:%S")
				except: 
					self.last_check_date = ""
		else:
			print(f"no such file: last_sync.json")

	
	def save_last_check(self):
		with open("last_sync.json", "w") as f:
			f.write(str(datetime.datetime.now()))

	async def set_student(self):
		await self.client.select_student()

	async def get_exams(self):
		if self.last_check_date == None or self.last_check_date == "":
			self.last_check_date = datetime.datetime.strptime("2021-09-01 00:00:00", "%Y-%m-%d %H:%M:%S")
		else:
			self.last_check_date = datetime.datetime.now()
			
		res =  await self.client.data.get_exams(last_sync=self.last_check_date)

		self.save_last_check()

		return res


