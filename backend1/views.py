from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from backend1.web_editables import Indexer_of_Food_Menu, create_horizontal_list, create_current_food_items_in_display

# Create your views here.

@csrf_exempt
def lobby(request):
    if request.method == 'POST':
        index_ = json.loads(request.body)
        return JsonResponse(create_current_food_items_in_display(index_,Indexer_of_Food_Menu),safe = False)
    elif request.method == 'GET':
        return  JsonResponse(create_horizontal_list(indexer_of_food_menu=Indexer_of_Food_Menu),safe = False)