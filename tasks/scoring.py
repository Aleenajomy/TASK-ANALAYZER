from datetime import date

def calculate_task_score(task_data):
    score = 0
    today = date.today()
    
    # Parse due_date if it's a string
    due_date = task_data['due_date']
    if isinstance(due_date, str):
        due_date = date.fromisoformat(due_date)
    
    days_until_due = (due_date - today).days
    
    # Urgency
    if days_until_due < 0:
        score += 100
    elif days_until_due <= 3:
        score += 50
    
    # Importance
    score += task_data.get('importance', 5) * 5
    
    # Quick wins
    if task_data.get('estimated_hours', 1) < 2:
        score += 10
    
    return score