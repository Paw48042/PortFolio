import json 
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
class LocationTrack(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["number"]
        self.room_group_name = f"mission_{self.room_name}"
        self.user_id = self.scope['user'].username

        # Join room group 
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )

        await self.accept() 
        # send a success message
        print("Congratulations! It's now connected")
    
    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_send(self.room_group_name,{
            "type" : "user.disconnect",
            "user_id" : self.user_id,
        })

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Print disconnect message on the backend
        print('User Disconnected')

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Text process
        text_data_json = json.loads(text_data)
        
        # Send message to room chat 
        await self.channel_layer.group_send(self.room_group_name,{
            "type": "location.point",
            "message": text_data_json['message'],
            "latitude" : text_data_json['latitude'],
            "longtitude" : text_data_json['longtitude'],
            "accuracy" : text_data_json['accuracy'],
            "user_id" : text_data_json['user_id'],
            "full_name" : text_data_json['full_name'],
        })

    # Receive message from room group
    async def location_point(self, event):
        message = event["message"]
        latitude = event["latitude"]
        longtitude = event["longtitude"]
        accuracy = event["accuracy"]
        user_id = event["user_id"]
        full_name = event["full_name"] 
        

        # Send message to WebSocket
        #await self.send(text_data=json.dumps({"message": message}))
        await self.send(text_data = json.dumps({
            "type" : "location_point",
            "message" : message,
            "latitude" : latitude,
            "longtitude" : longtitude,
            "accuracy" : accuracy,
            "user_id" : user_id,
            "full_name" : full_name,
        }))
    
    async def user_disconnect(self, event):
        user_id = event["user_id"]

        await self.send(text_data = json.dumps({
            "type" : "user_disconnect",
            "user_id" : user_id,
        }))