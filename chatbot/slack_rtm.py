#connect to slack view the RTM API
SLACK_BOT_TOKEN = "xoxb-318657942753-jM9wMoJzhKMCtMgeCaFaTkCO"
import time
from slackclient import SlackClient


chatlioBot = 'U98PFTATW'
sc = SlackClient(SLACK_BOT_TOKEN)
sc_rtm = sc.rtm_connect()
#rtm_events = SlackClient.
def connect_test():
	sc = SlackClient(SLACK_BOT_TOKEN)
	#connect to the real time messaging API
	if sc.rtm_connect():
		while True:
			print sc.rtm_read()
			print sc.api_call('auth.test')['user_id']
			time.sleep(1)
		else:
			print 'connection failed'
	
connect_test()