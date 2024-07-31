# serializers.py
from rest_framework import serializers
from .models import Department, Course, Questions, Choice, Quiz, QuizAttempt, Level
from accounts.serializers import UserProfileSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id','year']

class CourseSerializer(serializers.ModelSerializer):
   department = DepartmentSerializer() 
   level = LevelSerializer() 
   class Meta:
        model = Course
        fields = ['id','level','code','name','department']

class ChoiceSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer()
    class Meta:
        model = Choice
        fields = ['id','question','option','is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    choices = ChoiceSerializer(many=True, source='choice_set', read_only=True)

    class Meta:
        model = Questions
        fields = ['id','course','question','choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Questions.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question




class QuizSerializer(serializers.ModelSerializer):
    course= CourseSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id','questions','name','created_at','course']

   
   

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    user = UserProfileSerializer()
    time_taken = serializers.SerializerMethodField()
    class Meta:
        model = QuizAttempt
        fields =['id','user','quiz','score','completed_at','started_at','time_taken']

    def get_time_taken(self, obj):
        return obj.time_taken()



