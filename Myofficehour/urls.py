from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("management",views.OfficehourListView.as_view()),
    path('management/<int:pk>/', views.OfficehourDetailView.as_view()),

]