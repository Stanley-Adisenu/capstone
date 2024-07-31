from .models import Department,Course,Quiz,QuizAttempt,Level
from .serializers import DepartmentSerializer,CourseSerializer,QuizSerializer,QuizAttemptSerializer,UserProfileSerializer,QuestionSerializer,LevelSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
from django.db.models import Sum
from accounts.serializers import LeaderboardSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def department_list(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_list(request):
    if request.method == 'GET':
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_list_detail(request, pk):
    if request.method == 'GET':
        quiz = get_object_or_404(Quiz, id=pk)
        questions = list(quiz.questions.all())
        random_questions = random.sample(questions, min(len(questions), 3))  # Select 3 random questions
        quiz_data = {
            'id': quiz.id,
            'course': CourseSerializer(quiz.course).data,
            'questions': QuestionSerializer(random_questions, many=True).data,
            'name': quiz.name,
            'created_at': quiz.created_at
        }
        return Response(quiz_data)
    

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_attempt(request):
    if request.method == 'GET':
        quizzes = QuizAttempt.objects.all()
        serializer = QuizAttemptSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    # if request.method=='POST':
    #     serializer = QuizAttemptSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_attempt_detail(request,pk):
    if request.method == 'GET':
        quizzes = get_object_or_404(QuizAttempt,id=pk)
        serializer = QuizAttemptSerializer(quizzes)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quiz_attempt(request):
    quiz_id = request.data.get('quiz')
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = request.data.get('score')

    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score
    )

    # Update total points in User model
    request.user.total_points += score
    request.user.save()

   

    return Response(QuizAttemptSerializer(quiz_attempt).data, status=status.HTTP_201_CREATED)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard_view(request):
    users = User.objects.all().order_by('-total_points')
    serializer = LeaderboardSerializer(users, many=True)
    return Response(serializer.data) 



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    # Fetching departments and levels
    departments = Department.objects.all()
    levels = Level.objects.all()

    # Filtering quizzes
    quizzes = Quiz.objects.all()
    department_id = request.GET.get('department')
    level_id = request.GET.get('level')
    search_query = request.GET.get('search')

    if department_id:
        quizzes = quizzes.filter(course__department_id=department_id)
    if level_id:
        quizzes = quizzes.filter(course__level_id=level_id)
    if search_query:
        quizzes = quizzes.filter(name__icontains=search_query)

    # Serializing data
    department_serializer = DepartmentSerializer(departments, many=True)
    level_serializer = LevelSerializer(levels, many=True)
    quiz_serializer = QuizSerializer(quizzes, many=True)

    data = {
        'departments': department_serializer.data,
        'levels': level_serializer.data,
        'quizzes': quiz_serializer.data
    }

    return Response(data) 


