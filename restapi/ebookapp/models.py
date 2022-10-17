from django.db import models
 
# Create your models here.
 
class books(models.Model):
    bookid = models.AutoField(primary_key=True)
   
    booktitle = models.CharField(max_length=500, blank=True)
    author = models.CharField(max_length=500, blank=True)
    genre = models.CharField(max_length=500, blank=True)
    review =  models.PositiveIntegerField()
    favorite = models.BooleanField()
 
def _str_(self):
    return self.booktitle