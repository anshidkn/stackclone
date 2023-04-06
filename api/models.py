from django.db import models
from django.contrib.auth.models import User
class Questions(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    descrption=models.CharField(max_length=300)
    date=models.DateField(auto_now_add=True)
    image=models.ImageField(upload_to='images',null=True)
    def __str__(self) :
        return self.title
    @property
    def question_answer(self):
        return self.answers_set.all()

class Answers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=300)
    upvote=models.ManyToManyField(User,related_name="upvotes")
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.answer
    
    @property
    def count_upvote(self):
        return self.upvote.all().count()