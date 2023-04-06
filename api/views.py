from rest_framework.response import Response
from rest_framework import viewsets
from api.serialiser import UserSerialiser,QuestionSerialiser,AnswerSerialiser
from api.models import Questions,Answers
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import action 
from rest_framework import serializers
class UserView(viewsets.ViewSet):
    def create(self,request,*a,**k):
        serialiser=UserSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(data=serialiser.data)
        else:
            return Response(data=serialiser.errors)
  
class QuestionsView(viewsets.ModelViewSet):
    serializer_class=QuestionSerialiser
    queryset=Questions.objects.all()

    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=QuestionSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

    @action(methods=["POST"],detail=True) 
    def add_answer(self,request,*a,**k):
        # self.get_object   
        id=k.get("pk")
        object=Questions.objects.get(id=id)
        serializer=AnswerSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,question=object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class AnswersView(viewsets.ModelViewSet):
    serializer_class=AnswerSerialiser
    queryset=Answers.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    # authentication_classes=[authentication.TokenAuthentication]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("method not allowed")
    
    def list(self,request,*a,**k):
        raise serializers.ValidationError("method not allowed")

    def destroy(self, request, *args, **kwargs):
        ob=self.get_object()
        if request.user == ob.user:
            ob.delete()
            return Response(data="Deleted successfully")
        else:
            raise serializers.ValidationError("Permisssion denied for this user")
    @action(methods=["POST"],detail=True)
    def add_upvote(self,request,*a,**k):
        object=self.get_object()
        user=request.user
        object.upvote.add(user)
        object.save()
        return Response(data="upvoted succesfully")