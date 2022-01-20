# aggregation_test
Repository for test aggregations system

1. Create .env files from .env.example in root directory and api
2. Build images and run containers docker-compose up --build -d
3. In api container execute ```python manage.py makemigrations```
4. If you want test data for last hour and minute execute in api container ```python manage.py generate_events```

Endpoints:
1. http://localhost:8000/api/aggregator/crud/ - CRUD operations on event table
2. http://localhost:8000/api/aggregator/counter/ - Count endpoint from test requirements
3. http://localhost:8000/api/aggregator/statistics/ - Statistics endpoint from test requirements
