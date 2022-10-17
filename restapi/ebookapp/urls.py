from django.urls import path
from .views import Ebook,BookUpdate

urlpatterns = [
    path('book-items/', Ebook.as_view()),
    path('update-item/<int:item_id>', BookUpdate.as_view()),
]