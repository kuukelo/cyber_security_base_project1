from django.urls import path

from .views import homePageView, addView, transferView, signup

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('transfer/', transferView, name='transfer'),
    path('signup/', signup, name='signup')
]
