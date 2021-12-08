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
