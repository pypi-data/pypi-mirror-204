from random import randint
from ArverRubika.ArverMaker import makers
from colorama import Fore
__version__,__maker__,__channel__="1.0.0","Abolfazl Mirzai","@ArverTeam"
def text_flush(text):
	for txt in text:
		from time import sleep
		print(txt,end='',flush=True)
		sleep(0.035)
text_flush("Library ArverRubika "+Fore.CYAN+__version__+Fore.WHITE+"\n\tMaker "+Fore.YELLOW+__maker__+Fore.WHITE+"\n\t\tCannel Rubika "+Fore.RED+__channel__+Fore.WHITE+"\n\n")
text_flush("----------------------------------------------------\n\n")
class ArverBot:
	def __init__(self,token):
		self.auth = token
		self.method = makers(token).method
	def send_message(self,guid,text,message_id=None):
		date={
            'object_guid': guid,
            'rnd': str(randint(10000000, 999999999)),
            'text': text,
            'reply_to_message_id': message_id,
        }
		return self.method('sendMessage',date)
	def get_info_username(self,username):
		date={
		'username' : username,
		}
		return self.method('getObjectByUsername',date)
	def forward_message(self,from_guid,message_ids,to_guid):
		date={
		'from_object_guid': from_guid,
		'message_ids': [message_ids],
		'rnd': str(randint(10000000, 999999999)),
		'to_object_guid': to_guid
		}
		return self.method('forwardMessages',date)
	def get_all_chats(self,start_id=None):
		date={
		'start_id':start_id
		}
		return self.method('getChats',date)