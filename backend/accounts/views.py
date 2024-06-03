from django.shortcuts import render
from .models import Topic,Room,Message
from django.db.models import Q
from .serializers import TopicSerializer,RoomSerializer,MessageSerializer,UserCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
# Endpoint tested and working 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRoom(request):
    topic_name = request.data.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room = Room.objects.create(
        host=request.user,
        topic=topic,
        name=request.data.get('name'),
        description=request.data.get('description'),
    )
    return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

# Endpoint tested and working 
@api_view(['GET'])
def home(request):
    q = request.query_params.get('q', '')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[:3]

    total_rooms = Room.objects.count()
    unique_hosts = User.objects.filter(room__in=rooms).distinct()
    
    data = {
        'rooms': RoomSerializer(rooms, many=True).data,
        'topics': TopicSerializer(topics, many=True).data,
        'room_messages': MessageSerializer(room_messages, many=True).data,
        'total_rooms': total_rooms,
        'unique_hosts': UserCreateSerializer(unique_hosts, many=True).data  # Add unique hosts to the response

    }
    return Response(data, status=status.HTTP_200_OK)


# Endpoint tested and working
@api_view(['GET', 'POST'])
def room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.data.get('body')
        )
        room.participants.add(request.user)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
    
    room_data = RoomSerializer(room).data
    # return Response(room_data, status=status.HTTP_200_OK)

    # room_data = RoomSerializer(room).data
    room_messages = Message.objects.filter(room=room)
    messages_data = MessageSerializer(room_messages, many=True).data
    response_data = {
        'room': room_data,
        'messages': messages_data
    }
    return Response(response_data, status=status.HTTP_200_OK)


# tested and working
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateRoom(request,pk):
    if request.method=='PATCH':
        room = Room.objects.get(id=pk)
        if request.user != room.host and not request.user.is_superuser:
            return Response({'detail': 'Not allowed'},status=status.HTTP_403_FORBIDDEN)
        serializer = RoomSerializer(room,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)


# Tested and working
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host and not request.user.is_superuser:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    
    room.delete()
    return Response({'detail': 'Room deleted'}, status=status.HTTP_204_NO_CONTENT)

# To be tested
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user and not request.user.is_superuser:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    
    message.delete()
    return Response({'detail': 'Message deleted'}, status=status.HTTP_204_NO_CONTENT)


# Tested and working
@api_view(['GET'])
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    data = {
        'user': UserCreateSerializer(user).data,
        'rooms': RoomSerializer(rooms, many=True).data,
        'room_messages': MessageSerializer(room_messages, many=True).data,
    }
    return Response(data, status=status.HTTP_200_OK)









# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_user_api(request):
#     user = request.user
#     serializer = UserCreateSerializer(instance=user, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def topics(request):
    q = request.query_params.get('q', '')
    topics = Topic.objects.filter(name__icontains=q)
    return Response(TopicSerializer(topics, many=True).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def activity(request):
    room_messages = Message.objects.all()
    return Response(MessageSerializer(room_messages, many=True).data, status=status.HTTP_200_OK)






@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getTopic(request):
    if request.method=='GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer= TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getRoom(request):
    if request.method=='GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
