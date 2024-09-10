from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from backend1.web_editables import Editables


# Create your views here.

@csrf_exempt
def editables(request):
    match request.method:
        case 'POST':
            return JsonResponse(Editables(json.loads(request.body)).process_request(),safe=False)

