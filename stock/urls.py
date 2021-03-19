from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('top50gain/', views.top50gain, name='top50gain'),
  path('top50loss/', views.top50loss, name='top50loss'),
  path('top50pe/', views.top50pe, name='top50pe'),
  path('all/', views.all, name='all'),
  path('compare/', views.compare, name='compare'),
]