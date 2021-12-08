
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
