from django.conf.urls import url
from .views import UserRegistrationView, UserLoginView , AddAdvisorView, AdvisorListView , CallBookView, CallBookListView
from django.urls import path,include

urlpatterns = [
    path('user/register', UserRegistrationView.as_view()),
    path('user/login',UserLoginView.as_view()),
    path('admin/advisor',AddAdvisorView.as_view()),
    path('user/<int:user_id>/advisor',AdvisorListView.as_view()),
    path('user/<int:user_id>/advisor/<int:advisor_id>',CallBookView.as_view()),
    path('user/<int:user_id>/advisor/booking',CallBookListView.as_view()),
    ]