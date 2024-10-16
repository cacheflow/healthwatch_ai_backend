"""
URL configuration for healthwatch_ai_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from healthwatch_ai_app.models.medical_request import MedicalRequest
from django.urls import path
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from healthwatch_ai_app.views import MedicalRequestAPIView, LoginAPIView
from django.urls import path


router = routers.DefaultRouter()

urlpatterns = [
    path('api/medical-requests', MedicalRequestAPIView.as_view(), name='medical-requests'),
    path('api/medical-requests', MedicalRequestAPIView.as_view(), name='medical-requests'),
    path('api/auth/login/', LoginApiView.as_view(), name='login'),
]
