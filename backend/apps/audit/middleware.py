import uuid
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from apps.audit.models import AuditEvent

logger = logging.getLogger(__name__)

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware to assign request_id to each incoming request
    and record audit events for API mutations (POST, PUT, PATCH, DELETE).
    """
    def process_request(self, request):
        # Generate a unique request ID
        request.request_id = str(uuid.uuid4())
        
        # Attach request_id to threading context or logs if needed
        # (This is handled by logs filters as well)
        
    def process_response(self, request, response):
        # Only audit API endpoints under /api/v1/ (excluding health/ready/csrf/login/logout directly)
        path = request.path
        if not path.startswith('/api/v1/') or 'health' in path or 'ready' in path or 'csrf' in path:
            return response

        method = request.method
        user = request.user
        
        # We only log mutating requests by authenticated users (or login attempts which are post)
        if method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Determine Action
            action = 'CREATE'
            if method == 'POST':
                if 'login' in path:
                    action = 'LOGIN'
                elif 'logout' in path:
                    action = 'LOGOUT'
                else:
                    action = 'CREATE'
            elif method in ['PUT', 'PATCH']:
                action = 'UPDATE'
            elif method == 'DELETE':
                action = 'ARCHIVE'

            # Determine entity type from URL path
            # e.g., /api/v1/properties/ -> properties
            entity_type = None
            parts = path.strip('/').split('/')
            if len(parts) >= 3:
                entity_type = parts[2] # e.g. properties, owners, repairs

            # Get client IP & User Agent
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Record event (safely ignore errors so the main request doesn't fail)
            try:
                # We only log if user is authenticated (or was authenticated during logout)
                # For login, request.user might be Anonymous before login, so check if login succeeded
                log_user = user if user and user.is_authenticated else None
                
                # Check if we can determine the created/updated record ID from response data
                record_id = None
                if isinstance(response.data, dict):
                    record_id = response.data.get('id')

                # Log to DB
                AuditEvent.objects.create(
                    user=log_user,
                    action=action,
                    ip=ip,
                    user_agent=user_agent[:500] if user_agent else '',
                    entity_type=entity_type,
                    record_id=str(record_id) if record_id else None,
                    path=path[:255],
                    method=method,
                    result='SUCCESS' if 200 <= response.status_code < 400 else 'FAILURE',
                    # Sensitive bodies are excluded.
                    prev_data=None,
                    post_data=None,
                )
            except Exception as e:
                logger.error(f"Error creating audit log event: {str(e)}")

        return response
