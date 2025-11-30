# Smart Task Analyzer

A Django-based task prioritization system that helps users decide what to work on first using an intelligent scoring algorithm.

## 🎯 Project Overview

The Smart Task Analyzer is a web application that takes a list of tasks and prioritizes them based on multiple factors including urgency, importance, and effort required. It provides both comprehensive analysis and focused recommendations to help users make better decisions about task prioritization.

## 🏗️ Architecture

### Backend (Django REST API)
- **Framework**: Django 5.2.8
- **Database**: SQLite (development)
- **API**: RESTful endpoints for task analysis
- **CORS**: Custom middleware for cross-origin requests

### Frontend (Vanilla JavaScript)
- **HTML5**: Semantic structure
- **CSS3**: Responsive design
- **JavaScript**: Fetch API for backend communication

## 🧮 Algorithm Logic

The scoring algorithm considers three main factors with weighted importance:

### 1. **Urgency** (Highest Weight)
- **Overdue tasks**: +100 points (due_date < today)
- **Due within 3 days**: +50 points
- **Future tasks**: No urgency bonus

### 2. **Importance** (Medium Weight)
- Multiplies importance rating (1-10) by 5
- Range: 5-50 points
- Default: 25 points (importance = 5)

### 3. **Quick Wins** (Low Weight)
- Tasks under 2 hours: +10 points
- Encourages completion of small, manageable tasks

### Scoring Formula
```
Total Score = Urgency Points + (Importance × 5) + Quick Win Bonus
```

### Priority Categories
- **High Priority**: Score ≥ 100 (typically overdue tasks)
- **Medium Priority**: Score 50-99 (due soon or very important)
- **Low Priority**: Score < 50 (future or less critical tasks)

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Django server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Backend API: `http://127.0.0.1:8000/`
   - Frontend: Open `frontend/index.html` in your browser

## 📡 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/tasks/`

### 1. Analyze Tasks
- **Endpoint**: `POST /api/tasks/analyze/`
- **Purpose**: Analyze and prioritize all tasks
- **Request Body**:
  ```json
  {
    "tasks": [
      {
        "title": "Complete project report",
        "due_date": "2024-01-15",
        "importance": 8,
        "estimated_hours": 4
      }
    ]
  }
  ```
- **Response**:
  ```json
  {
    "tasks": [
      {
        "title": "Complete project report",
        "due_date": "2024-01-15",
        "importance": 8,
        "estimated_hours": 4,
        "score": 90
      }
    ]
  }
  ```

### 2. Get Task Suggestions
- **Endpoint**: `POST /api/tasks/suggest/`
- **Purpose**: Get top 3 task recommendations with explanations
- **Request Body**: Same as analyze endpoint
- **Response**:
  ```json
  {
    "suggestions": [
      {
        "task": {
          "title": "Complete project report",
          "due_date": "2024-01-15",
          "importance": 8,
          "estimated_hours": 4,
          "score": 90
        },
        "explanation": "Priority score: 90 - Due soon"
      }
    ]
  }
  ```

### Required Fields
- `title` (string): Task description
- `due_date` (string): Date in "YYYY-MM-DD" format

### Optional Fields
- `importance` (integer): 1-10 scale, default: 5
- `estimated_hours` (number): Time estimate, default: 1

## 💻 Usage Examples

### Example 1: Work Tasks
```json
[
  {
    "title": "Deploy production hotfix",
    "due_date": "2024-01-11",
    "importance": 10,
    "estimated_hours": 2
  },
  {
    "title": "Code review for feature X",
    "due_date": "2024-01-13",
    "importance": 7,
    "estimated_hours": 1
  },
  {
    "title": "Update documentation",
    "due_date": "2024-01-20",
    "importance": 4,
    "estimated_hours": 6
  }
]
```

### Example 2: Personal Tasks
```json
[
  {
    "title": "Pay credit card bill",
    "due_date": "2024-01-08",
    "importance": 9,
    "estimated_hours": 0.25
  },
  {
    "title": "Grocery shopping",
    "due_date": "2024-01-14",
    "importance": 5,
    "estimated_hours": 1.5
  }
]
```

## 🧪 Testing

### Manual Testing
1. Start the Django server
2. Open `frontend/index.html` in a browser
3. Enter task data in JSON format
4. Click "Analyze Tasks" or "Get Top 3 Suggestions"
5. Verify results display correctly

### API Testing with cURL
```bash
# Test analyze endpoint
curl -X POST http://127.0.0.1:8000/api/tasks/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"tasks":[{"title":"Test task","due_date":"2024-01-15","importance":7,"estimated_hours":2}]}'

# Test suggest endpoint
curl -X POST http://127.0.0.1:8000/api/tasks/suggest/ \
  -H "Content-Type: application/json" \
  -d '{"tasks":[{"title":"Test task","due_date":"2024-01-15","importance":7,"estimated_hours":2}]}'
```

## 📁 Project Structure

```
task-analyzer/
├── backend/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Django configuration
│   ├── urls.py            # Main URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── middleware.py      # Custom CORS middleware
├── tasks/                  # Django app for task management
│   ├── migrations/        # Database migrations
│   ├── __init__.py
│   ├── admin.py          # Django admin configuration
│   ├── apps.py           # App configuration
│   ├── models.py         # Database models
│   ├── scoring.py        # Task scoring algorithm
│   ├── tests.py          # Unit tests
│   ├── urls.py           # App URL routing
│   └── views.py          # API view functions
├── frontend/              # Frontend files
│   ├── index.html        # Main HTML page
│   ├── script.js         # JavaScript functionality
│   └── styles.css        # CSS styling
├── venv/                 # Virtual environment (not in git)
├── db.sqlite3           # SQLite database (not in git)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Technical Features

### Backend Features
- **RESTful API**: Clean, consistent API design
- **CORS Support**: Custom middleware for cross-origin requests
- **Input Validation**: Comprehensive error handling and validation
- **Modular Design**: Separate scoring algorithm for easy modification
- **Database Models**: Extensible task model for future enhancements

### Frontend Features
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Feedback**: Immediate error messages and results
- **JSON Validation**: Client-side JSON parsing with error handling
- **Visual Priority Indicators**: Color-coded task cards by priority level
- **Interactive Interface**: Clean, intuitive user experience

### Security Features
- **CSRF Protection**: Django's built-in CSRF middleware
- **Input Sanitization**: JSON validation and error handling
- **CORS Configuration**: Controlled cross-origin access

## 🚀 Future Enhancements

### Potential Features
- **User Authentication**: Personal task lists and preferences
- **Task Categories**: Organize tasks by project or category
- **Recurring Tasks**: Support for repeating tasks
- **Calendar Integration**: Import tasks from calendar applications
- **Mobile App**: Native mobile application
- **Team Collaboration**: Shared task lists and assignments
- **Analytics Dashboard**: Task completion statistics and insights
- **Email Notifications**: Reminders for upcoming deadlines
- **Export Functionality**: Export prioritized lists to various formats

### Technical Improvements
- **Database Optimization**: PostgreSQL for production
- **Caching**: Redis for improved performance
- **API Documentation**: Swagger/OpenAPI integration
- **Unit Testing**: Comprehensive test coverage
- **CI/CD Pipeline**: Automated testing and deployment
- **Docker Support**: Containerized deployment
- **Load Balancing**: Support for high-traffic scenarios

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure Django server is running on port 8000
   - Check that CORS middleware is properly configured
   - Verify frontend is accessing the correct API URL

2. **JSON Parse Errors**
   - Validate JSON format using online JSON validators
   - Ensure all strings use double quotes, not single quotes
   - Check for trailing commas in JSON objects

3. **Django Server Won't Start**
   - Verify virtual environment is activated
   - Check that all dependencies are installed
   - Run migrations if database errors occur

4. **Tasks Not Displaying**
   - Check browser console for JavaScript errors
   - Verify API endpoints are responding correctly
   - Ensure task data includes required fields

### Debug Mode
Enable Django debug mode by setting `DEBUG = True` in `settings.py` for detailed error messages.

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


---

**Built with ❤️ using Django and JavaScript**