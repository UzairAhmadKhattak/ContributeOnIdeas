import json
from channels.generic.websocket import AsyncWebsocketConsumer
 
class notification(AsyncWebsocketConsumer):
	async def connect(self):
		self.auth_user = str(self.scope["user"])
		self.idea_id = self.scope["url_route"]["kwargs"]["idea_id"]
		self.roomGroupName = f"notification_ideaID_{self.idea_id}"
		
		print(f'\nAuth user {self.auth_user} is connected to {self.roomGroupName} room.\n')
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
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message 
			})
			
	async def sendMessage(self, event):
		message = event['message']
		await self.send(text_data=json.dumps({
			'message': message,
		}))
