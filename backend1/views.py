from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from backend1.web_editables import (Indexer_of_Food_Menu,send_categories,
                                    create_current_food_items_in_display,delete_item)

# Create your views here.

@csrf_exempt
def lobby(request):
    if request.method == 'POST':
        index_ = json.loads(request.body)
        return JsonResponse(create_current_food_items_in_display(index_,Indexer_of_Food_Menu),safe = False)
    elif request.method == 'GET':
        return  JsonResponse(send_categories(indexer_of_food_menu=Indexer_of_Food_Menu),safe = False)

@csrf_exempt
def editables(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        return JsonResponse(delete_item(indexer_of_food_menu=Indexer_of_Food_Menu,category=data['selectedCategory'],index=data['index']),safe = False)