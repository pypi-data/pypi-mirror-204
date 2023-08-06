from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, HomeView


urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('register/', RegistrationView.as_view(), name="signup"),
    path('', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
