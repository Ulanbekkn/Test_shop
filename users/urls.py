from django.urls import path, include
from users.views import RegisterAPIView, ConfirmCodeAPIView, LoginAPIView, FavoriteAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('confirm/', ConfirmCodeAPIView.as_view(), name='confirm'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('favorites/', FavoriteAPIView.as_view(), name='favorites'),
]


