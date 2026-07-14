import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def global_exception_handler(exc, context):
    """
    Standardizes error responses across all API endpoints with custom validation formatting.
    """
    response = exception_handler(exc, context)
    request = context.get('request')
    request_id = getattr(request, 'request_id', '') if request else ''
    
    if response is not None:
        custom_data = {
            'code': 'api_error',
            'message': 'Ocurrió un error al procesar la solicitud.',
            'errors': {},
            'request_id': request_id
        }
        
        # Handle validation errors specifically
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_data['code'] = 'validation_error'
            custom_data['message'] = 'Los datos enviados no son válidos.'
            custom_data['errors'] = response.data
        else:
            # Handle other HTTP errors (401, 403, 404, etc.)
            custom_data['code'] = getattr(exc, 'default_code', 'error')
            custom_data['message'] = response.data.get('detail', str(exc)) if isinstance(response.data, dict) else str(response.data)
            
        response.data = custom_data
    else:
        # Handle unhandled server exceptions (500)
        logger.exception("Unhandled server exception: %s", str(exc), extra={'request_id': request_id})
        
        response = Response({
            'code': 'server_error',
            'message': 'Ocurrió un error interno en el servidor.',
            'errors': {},
            'request_id': request_id
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return response
