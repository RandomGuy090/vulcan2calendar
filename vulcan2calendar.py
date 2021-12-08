
from vulcan import Vulcan
from vulcan import Account
from vulcan import Keystore

import json, asyncio, datetime
import datetime
from time import time, strftime, sleep
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials





class Google_user(object):

	def __init__(self):
		self.SCOPES = ['https://www.googleapis.com/auth/calendar']
		self.cal_name = "Vulcan"
		self.creds = None
		self.service = None
		self.calendar_id = None
		self.token = None
		self.timezone = strftime("%Z %z")
		self.page_token = None
		self.create_cal = True
		print("google user")
		self.load_credentials()


	def load_credentials(self):
		if os.path.exists('token.json'):
			self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', self.SCOPES)
				self.creds = flow.run_local_server(port=0)
			with open('token.json', 'w') as token:
				token.write(self.creds.to_json())

	def get_build(self):
		self.service = build('calendar', 'v3', credentials=self.creds)

		return self.service

	def calendar_handler(self):
		while True:
			calendar_list = self.get_calendar_list(self.page_token)

			for calendar_list_entry in calendar_list['items']:

				if calendar_list_entry["summary"] == self.cal_name:
					self.calendar_id = calendar_list_entry["id"]
					self.create_cal = False
			
			self.page_token = calendar_list.get('nextPageToken')
			if not self.page_token:
				break

		if self.create_cal:
			created_calendar = self.create_calendar()
			self.calendar_id = created_calendar["id"]
			print(f"new calendar id: {self.calendar_id}")
			return self.service.calendars().get(calendarId=self.calendar_id).execute()

		else:
			return self.service.calendars().get(calendarId=self.calendar_id).execute()



	def get_calendar_list(self, token):
		return self.service.calendarList().list(pageToken=token).execute()

	def create_calendar(self, calendar=None):
		print("creating new calendar")
		if calendar == None:
			calendar = {
			'summary': self.cal_name,
			'timeZone': "Europe/Warsaw"
			}

		return self.service.calendars().insert(body=calendar).execute()

	def get_calendar(self, cal_id=None):
		if cal_id == None:
			cal_id = self.calendar_id

		return self.service.calendars().get(calendarId=cal_id).execute()

	def create_event(self, body, cal_id=None):
		if cal_id == None:
			cal_id = self.calendar_id

		return self.service.events().insert(calendarId=cal_id, body=body).execute()


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







async def main(loop): 


	google = Google_user()
	service = google.get_build()


	calendar_obj = google.calendar_handler()

	client = Vulcan_user()
	await client.set_student()

	while True:

		exams = await client.get_exams()

		all_events = []
		try:
			async for elem in exams:
				if elem.deadline.date_time > datetime.datetime.now():
					event = {
							'summary': elem.subject.name,
							'description': elem.topic,
							'start': {
								'dateTime': f"{str(elem.deadline.date)}T00:00:00",
								'timeZone': 'Europe/Warsaw'

							},
							'end': {
								'dateTime': f"{str(elem.deadline.date)}T00:00:00",
								
								'timeZone': 'Europe/Warsaw'
							},
							'reminders': {
							'useDefault': True,
							},
						}
					print(event)
					all_events.append(event)
		except:
			print("xD")

		for elem in all_events:

			google.create_event(body=elem)

		sleep(5)






if __name__ == "__main__":

	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop))
