from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Questions,Answers

class UserSerialiser(serializers.ModelSerializer):
     class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
     def create(self, validated_data):
         return User.objects.create_user(**validated_data)



#TOKENAUTHIACTION
#SOCIALNETWORK:MODELS-POSTS,COMMENTS

class AnswerSerialiser(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    question=serializers.CharField(read_only=True)
    upvote=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    count_upvote=serializers.CharField(read_only=True)
    class Meta:
        model=Answers
        fields="__all__"

class QuestionSerialiser(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    question_answer= AnswerSerialiser(read_only=True,many=True)
    class Meta:
        model=Questions
        fields="__all__"