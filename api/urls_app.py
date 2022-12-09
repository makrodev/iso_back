from django.urls import path
from . import views


urlpatterns = [
    # Process
    path('processes/', views.ProcessAPIView.as_view()),

    # Status
    path('statuses', views.StatusAPIView.as_view()),

    # Violation
    path('violations/', views.ViolationAPIView.as_view()),
    path('violation_detail/<int:id>/', views.ViolationDetailAPIView.as_view()),
    path('violations_days/<int:days>/', views.ViolationDaysView.as_view()),

    path('regions/', views.RegionAPIView.as_view()),

    path('shops/', views.ShopAPIView.as_view()),

    path('departments/', views.DepartmentAPIView.as_view()),

    path('problems/', views.ProblemAPIView.as_view()),

    path('disparities/', views.DisparityAPIView.as_view()),

    # Admin
    path('admins/', views.AdminAPIView.as_view()),

    # Client
    path('clients/', views.ClientAPIView.as_view()),
    path('client/<int:id>/', views.ClientDetailAPIView.as_view()),

    # Login
    path('login/<int:phone>/', views.LoginAPIView.as_view()),
]
