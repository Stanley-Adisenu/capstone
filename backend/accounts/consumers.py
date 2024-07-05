import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.serializers import MessageSerializer

from rest_framework_simplejwt.tokens import AccessToken


from accounts.models import Room,Message

from django.contrib.auth import get_user_model
User = get_user_model()

def get_user(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return User.objects.get(id=user_id)
    except Exception as e:
        return None

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Extract the JWT token from the query string
        query_string = self.scope['query_string'].decode()
        token = None
        if 'token=' in query_string:
            token = query_string.split('token=')[-1]

        self.user = await sync_to_async(get_user)(token)
        if not self.user:
            await self.close()
            return

        #join room group
        try:
            self.room = await sync_to_async(Room.objects.get)(name=self.room_name)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()      
        except Room.DoesNotExist:
            await self.close()

    async def disconnect(self,close_code):
        #leave room
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)



    async def receive(self,text_data):
        #receive message from websocket in the frontend 
        data = json.loads(text_data)

        if 'message' not in data:
            await self.send(text_data=json.dumps({
                'error': "'message' key not found in data"
            }))
            return

        message = data['message']
        user = self.user
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'error': 'User is not authenticated'
            }))
            return
        user_id = user.id

        try:
            room = await sync_to_async(Room.objects.get)(name=self.room_name)
        except Room.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Room does not exist'
            }))
            return

      

        # Add user to participants
        await sync_to_async(room.participants.add)(user)

        # message = data['message']
        # name = data['name']
        # agent =data['agent']

            # Create and save message to the database
        new_message = await sync_to_async(Message.objects.create)(
            user_id=user_id,
            room=room,
            body=message
        )
       
        serialized_message = await (self.serialize_message)(new_message)



        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serialized_message['body'],
                'user': serialized_message['user']['user_name'],
                # 'time_since_updated': serialized_message['time_since_updated'],
            }
        )

        # if type == 'message':
        #     new_message =await self.create_message(name,message,agent)
        #     await self.channel_layer.group_send(
        #         self.room_group_name,{
        #             'type': 'chat_message',
        #             'message': message,
        #             'name': name,
        #             'agent': agent,
                    
        #         }
        #     )


       
        # serializer = MessageSerializer(data=type)
        # if serializer.is_valid():
        #     await sync_to_async(serializer.save())
        #     await self.channel_layer.group_send(
        #             self.room_group_name,{
        #             'type':'chat_message',
        #             'message':serializer.data
        #             }
        #     )
    
    @sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        # time_since_updated = event['time_since_updated']


        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            # 'time_since_updated': time_since_updated,
            
        }))
    # async def chat_message(self, event):
    #     message = event['message']
    #     user = event['user']

    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'user': user,
    #     }))

    # @sync_to_async
    # def  create_message(self,sent_by,message,agent):
    #     message = Message.objects.create(body=message,sent_by='')

    #     if agent:
    #         message.created_by = User.objects.get(pk=agent)
    #         message.save()

    #     self.room.messages.add(message)

    #     return message
    
    # @sync_to_async
    # def get_room(self):
        # self.room=Room.objects.get(id=self.room_name)

