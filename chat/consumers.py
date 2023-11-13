import json
from channels.generic.websocket import AsyncWebsocketConsumer
 
class chat(AsyncWebsocketConsumer):
	async def connect(self):
		login_user = self.scope['user']
		send_msg_to = self.scope["url_route"]["kwargs"]["other_user"]
		create_group_name = sorted([str(login_user).capitalize(),str(send_msg_to).capitalize()])
		self.roomGroupName = f"group_chat_{create_group_name[0]}_{create_group_name[1]}"
		
		print(self.roomGroupName)
		await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
		await self.accept()
			
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_name
        )
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		username = text_data_json['username']
		auth_username = text_data_json['auth_username']
		await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "message" : message ,
                "username" : username,
				'auth_username':auth_username
            })
		
	async def sendMessage(self, event):
		message = event["message"]
		username = event["username"]
		auth_username = event['auth_username']
		await self.send(text_data=json.dumps({
			'message': message,
			'username':username,
			'auth_username':auth_username
		}))
