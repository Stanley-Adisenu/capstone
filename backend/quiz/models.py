from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model() 

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class Level(models.Model):
    year = models.CharField(max_length=50)

    def __str__(self):
        return self.year
    

    
    
class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name[0:17]
    
class Questions(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question =  models.TextField()
    

    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    questions =models.ManyToManyField(Questions)
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='QuizUser')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    started_at = models.DateTimeField( auto_now_add=True)
    completed_at = models.DateTimeField( auto_now=True)

    def time_taken(self):
        return self.completed_at - self.started_at





    
    
    
    
    
    
    

