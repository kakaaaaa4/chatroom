from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        ip_city = text_data_json['ip_city']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                "ip_city": ip_city,
                'message': message
            }
       )

    async def chat_message(self,event):
        message = event['message']
        ip_city = event['ip_city']
        await self.send(text_data = json.dumps({
            'message':ip_city + ':' + message
        }))