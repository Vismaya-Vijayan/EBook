from django.shortcuts import render

from django.views import View
from django.http import JsonResponse
import json
from .models import books



from django.shortcuts import render
from .serializers import UserRegister,UserDataSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

# Create your views here.

class register(APIView):
    
    def post(self,request,format=None):
        serializer=UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']='registered'
            data['username']=account.username
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
        else:
            data=serializer.errors
        return Response(data)
    
class welcome(APIView):
    permission_classes =(IsAuthenticated,)
    
    def get(self,request):
        content={'user':str(request.user),'userid':str(request.user.id)}
        return Response(content)
class userDetails(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
        
    def get(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        userData=self.get_object(pk)
        serializer=UserDataSerializer(userData,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.errors})
    def delete(self,request,pk,format=None):
        userData=self.get_object(pk)
        userData.delete()
        return Response({'message':"user deleted"})
   
     







class Ebook(View):
   def post(self, request):
         data = json.loads(request.body.decode("utf-8"))
         book_id=data.get('bookid')
         book_name=data.get('booktitle')
         book_author=data.get('author')
         book_genre=data.get('genre')
         book_review=data.get('review')
         book_favorite=data.get('favorite')
         
         book_data = {
            'bookid' : book_id,
            'booktitle' : book_name,
            'author' : book_author,
            'genre' : book_genre,
            'review' : book_review,
            'favorite' : book_favorite 
         }

         book_item = books.objects.create(**book_data)

         data = {
            "message": f"New item added to Cart with id: {book_item.id}"
         }
         return JsonResponse(data, status=201)
      




   def get(self, request):
      items_count = books.objects.count()
      items = books.objects.all()
      items_data = []
      for item in items:
         items_data.append({
                'bookid' : item.bookid,
                'booktitle' : item.booktitle,
                'author' : item.author,
                'genre' : item.genre,
                'review' : item.review,
                'favorite' : item.favorite, 
                 
            })
      data = {
            'items': items_data,
            'count': items_count,
         }

      return JsonResponse(data)   
                
        

        
        
            

        




class BookUpdate(View):
     def patch(self, request, item_id):
      data = json.loads(request.body.decode("utf-8"))
      item = books.objects.get(id=item_id)
      item.bookid = data['bookid']
      item.booktitle = data['booktitle']
      item.author = data['author']
      item.genre = data['genre']
      item.review = data['review']
      item.favorite = data['favorite']
      item.save()
      data = {
            'message': f'Item {item_id} has been updated'
      }
      return JsonResponse(data)
         
         
         

         

     def delete(self, request, item_id):
      item = books.objects.get(id=item_id)
      item.delete()
      data = {
            'message': f'Item {item_id} has been deleted'
      }

      return JsonResponse(data)
        
       
# Create your views here.
