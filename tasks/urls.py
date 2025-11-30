from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def cors_preflight(request):
    response = JsonResponse({})
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

urlpatterns = [
    path('analyze/', views.analyze_tasks, name='analyze_tasks'),
    path('suggest/', views.suggest_tasks, name='suggest_tasks'),
]