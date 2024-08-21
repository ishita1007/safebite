from django.urls import path
from . import views

urlpatterns = [
    path('',views.hello,name='hello'),
    path('fooddir', views.fooddir, name='fooddir'),
    path('hello',views.hello, name='add'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('blogpost-like', views.BlogPostLike, name="blogpost_like"),
    path('result',views.result,name='result'),
    path('select_allergens', views.select_allergens, name='select_allergens'),

]