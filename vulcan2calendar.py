
# from vulcan import Vulcan
# from vulcan import Account
# from vulcan import Keystore

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
import json, asyncio, datetime, datetime, os.path
from time import time, strftime, sleep


from google_calendar import Google_user
from vulcan_user import Vulcan_user

all_events = []

google = Google_user()
service = google.get_build()

calendar_obj = google.calendar_handler()

client = Vulcan_user()

def parse_google(elem):
	for elem in all_events:
		google.create_event(body=elem)
		# print(elem)
		pass

async def homework_loop(client):
	await client.set_student()

	while True:
		homework = await client.get_homework()

		async for work in homework:
			if work.deadline.date_time > datetime.datetime.now():

				event = {
							'summary': work.subject.name,
							'description': work.content,
							'start': {
								'dateTime': f"{str(work.deadline.date)}T00:00:00",
								'timeZone': 'Europe/Warsaw'

							},
							'end': {
								'dateTime': f"{str(work.deadline.date)}T00:00:00",
								
								'timeZone': 'Europe/Warsaw'
							},
							'reminders': {
							'useDefault': True,
							},
							 'reminders': {
						    'useDefault': False,
						    'overrides': [
						      {'method': 'popup', 'minutes': 15*60},
						    ],
						  },
						}
				print(event)
				all_events.append(event)
				parse_google(event)



	sleep(5)

async def exams_loop(client):
	await client.set_student()

	while True:

		exams = await client.get_exams()

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
							 'reminders': {
						    'useDefault': False,
						    'overrides': [
						      {'method': 'popup', 'minutes': 15*60},
						    ],
						  },
						}
					print(event)
					all_events.append(event)
					parse_google(event)
			
			
		
		except Exception as e:
			# print(f"xD ({e})")
			pass


		sleep(5)

# async def main(): 

	
	

	# await exams_loop(client)
	# await homework_loop(client)






if __name__ == "__main__":

	loop = asyncio.get_event_loop()
	loop2 = asyncio.get_event_loop()
	
	# loop.create_task(main())
	
	loop2.create_task(homework_loop(client))
	loop.create_task(exams_loop(client))
	
	loop.run_forever()
	loop2.run_forever()
	# loop.run_until_complete(main(loop))
