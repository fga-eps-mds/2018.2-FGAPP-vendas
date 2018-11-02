from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

@api_view(['GET'])
def status(request):
    version = settings.VERSION
    
    return Response({
    "name":"order-microservice",
    "online": True,
    "version":version,

})