from django.urls import path
from users.api import views


urlpatterns = [
    path('signup/', views.SignupAPIView.as_view())
]
