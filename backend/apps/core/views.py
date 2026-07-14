from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """
    Indicates that the backend application is running.
    """
    return JsonResponse({'status': 'ok', 'message': 'Hogar Express backend is running'})

def ready_check(request):
    """
    Verifies database connectivity and basic configurations without exposing secrets.
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        return JsonResponse({
            'status': 'ready',
            'database': 'connected',
            'timezone': connection.timezone_name if hasattr(connection, 'timezone_name') else 'America/Bogota',
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'database': 'disconnected',
            'detail': str(e)
        }, status=503)
