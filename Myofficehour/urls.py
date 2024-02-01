from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path('mgmt/api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('mgmt/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('mgmt/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('mgmt/api/officehour/', views.OfficehourListCreateAPIView.as_view()),
    path('mgmt/api/officehour/<int:pk>/', views.OfficehourListDetailAPIView.as_view()),
]