from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .scoring import calculate_task_score

def add_cors_headers(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@csrf_exempt
def analyze_tasks(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Analyze endpoint is working. Use POST with task data.'})
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
        
    try:
        if not request.body:
            return JsonResponse({'error': 'No data provided'}, status=400)
            
        data = json.loads(request.body)
        tasks = data.get('tasks', [])
        
        if not tasks:
            return JsonResponse({'error': 'No tasks provided'}, status=400)
        
        # Calculate scores and sort
        for task in tasks:
            # Validate required fields
            if 'title' not in task or 'due_date' not in task:
                return JsonResponse({'error': 'Missing required fields: title, due_date'}, status=400)
            task['score'] = calculate_task_score(task)
        
        sorted_tasks = sorted(tasks, key=lambda x: x['score'], reverse=True)
        return JsonResponse({'tasks': sorted_tasks})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
def suggest_tasks(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Suggest endpoint is working. Use POST with task data.'})
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
        
    try:
        if not request.body:
            return JsonResponse({'error': 'No data provided'}, status=400)
            
        data = json.loads(request.body)
        tasks = data.get('tasks', [])
        
        if not tasks:
            return JsonResponse({'error': 'No tasks provided'}, status=400)
        
        # Get top 3 tasks
        for task in tasks:
            if 'title' not in task or 'due_date' not in task:
                return JsonResponse({'error': 'Missing required fields: title, due_date'}, status=400)
            task['score'] = calculate_task_score(task)
        
        top_tasks = sorted(tasks, key=lambda x: x['score'], reverse=True)[:3]
        
        suggestions = []
        for task in top_tasks:
            explanation = f"Priority score: {task['score']} - "
            if task['score'] >= 100:
                explanation += "Overdue task!"
            elif task['score'] >= 50:
                explanation += "Due soon"
            else:
                explanation += "Important task"
            
            suggestions.append({
                'task': task,
                'explanation': explanation
            })
        
        return JsonResponse({'suggestions': suggestions})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)