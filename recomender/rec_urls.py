from django.urls import path
from recomender.views import Recommender

urlpatterns = [ 
    path('recommended',Recommender,name = 'recommender')
               
]